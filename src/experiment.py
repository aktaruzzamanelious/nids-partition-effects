"""Block 3 experiment pipeline. Four protocol arms, ten untuned classifiers.

Every encoder and scaler is fitted on the training portion of one cell and
nothing else. Smoke and probe output goes to results/smoke/, full-run output to
results/raw/, and the two are never mixed. Usage:
  python src/experiment.py --mode {smoke,probe,full} [--dataset {unsw,nslkdd}]
"""
import os

for _lib in ("OMP", "OPENBLAS", "MKL", "NUMEXPR"):
    os.environ[f"{_lib}_NUM_THREADS"] = "2"

import argparse
import gc
import hashlib
import json
import resource
import socket
import sys
import time
import traceback
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import (AdaBoostClassifier, ExtraTreesClassifier,
                              HistGradientBoostingClassifier, RandomForestClassifier)
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.metrics import (accuracy_score, average_precision_score,
                             balanced_accuracy_score, confusion_matrix, f1_score,
                             matthews_corrcoef, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import RepeatedStratifiedKFold, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
RAW, LOGS, SEP = "data/raw", "logs", "\x1f"
RSS_ABORT_MB, RARE_THRESHOLD, OTHER = 2500.0, 0.001, "__other__"
SEEDS = [11, 22, 33, 44, 55, 66, 77, 88, 99, 110]
SEEDS_B = [11, 22, 33, 44, 55]
SMOKE_MODELS = ["M01", "M03", "M05", "M09", "M10"]
ALL_MODELS = [f"M{i:02d}" for i in range(1, 11)]
PROTOCOLS = ["A", "B", "C-naive", "C-group"]
PIPELINE = ["src/verify.py", "src/preprocess.py", "src/experiment.py"]

# Validated against data/raw/KDDTrain+.txt on 2026-09-05, decision P10.
NSL_COLUMNS = """
duration protocol_type service flag src_bytes dst_bytes land wrong_fragment urgent hot
num_failed_logins logged_in num_compromised root_shell su_attempted num_root
num_file_creations num_shells num_access_files num_outbound_cmds is_host_login
is_guest_login count srv_count serror_rate srv_serror_rate rerror_rate srv_rerror_rate
same_srv_rate diff_srv_rate srv_diff_host_rate dst_host_count dst_host_srv_count
dst_host_same_srv_rate dst_host_diff_srv_rate dst_host_same_src_port_rate
dst_host_srv_diff_host_rate dst_host_serror_rate dst_host_srv_serror_rate
dst_host_rerror_rate dst_host_srv_rerror_rate attack_name difficulty_level""".split()

FILES = {"unsw": ("UNSW_NB15_training-set.csv", "UNSW_NB15_testing-set.csv"),
         "nslkdd": ("KDDTrain+.txt", "KDDTest+.txt")}
SIZES = {"unsw": (175341, 82332), "nslkdd": (125973, 22544)}
CATEGORICAL = {"unsw": ["proto", "service", "state"],
               "nslkdd": ["protocol_type", "service", "flag"]}
DROP_COLS = {"unsw": ["id", "attack_cat", "label"],
             "nslkdd": ["attack_name", "difficulty_level", "label"]}
CAT_LABEL = {"unsw": "attack_cat", "nslkdd": "attack_name"}
EXP_FEATURES_A = {"unsw": 69, "nslkdd": 106}
# Measured over seeds 11 to 55 in Blocks 1B and 1C. Outside this window the
# split code is not reproducing the earlier measurement.
CNAIVE_LEAK_RANGE = {"unsw": (44.0740, 44.5027), "nslkdd": (0.7984, 0.9359)}

MODEL_SPEC = {
    "M01": (GaussianNB, dict(var_smoothing=1e-9)),
    "M02": (LogisticRegression, dict(solver="lbfgs", max_iter=500, C=1.0, n_jobs=2)),
    "M03": (RidgeClassifier, dict(alpha=1.0, solver="auto")),
    "M04": (DecisionTreeClassifier, dict(criterion="gini", max_depth=None,
                                         min_samples_split=2)),
    "M05": (RandomForestClassifier, dict(n_estimators=100, max_depth=None, n_jobs=2)),
    "M06": (ExtraTreesClassifier, dict(n_estimators=100, max_depth=None, n_jobs=2)),
    "M07": (AdaBoostClassifier, dict(n_estimators=100, learning_rate=1.0)),
    "M08": (HistGradientBoostingClassifier, dict(max_iter=200, learning_rate=0.1,
                                                 max_leaf_nodes=31, early_stopping=False)),
    "M09": (XGBClassifier, dict(tree_method="hist", n_estimators=200, max_depth=6,
                                learning_rate=0.3, n_jobs=2, eval_metric="logloss")),
    "M10": (LGBMClassifier, dict(n_estimators=200, num_leaves=31, learning_rate=0.1,
                                 n_jobs=2, verbose=-1)),
}
MODEL_NAMES = {k: v[0].__name__ for k, v in MODEL_SPEC.items()}

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def rss_mb():
    with open("/proc/self/status") as fh:
        for line in fh:
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) / 1024.0
    return -1.0

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def write_json(path, payload):
    with open(path + ".tmp", "w") as fh:
        json.dump(payload, fh, indent=2, default=str)
    os.replace(path + ".tmp", path)

def peak_rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0  # kB to MB

def preflight(mode):
    from importlib.metadata import version
    st = os.statvfs(os.path.expanduser("~"))
    free_gb = st.f_bavail * st.f_frsize / 2 ** 30
    if free_gb < 1.0:
        sys.exit(f"free disk {free_gb:.2f} GB is under 1 GB")
    mi = dict(l.split(":", 1) for l in open("/proc/meminfo"))
    cpu = [l for l in open("/proc/cpuinfo") if l.startswith("model name")]
    rec = {"mode": mode, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "free_disk_gb": round(free_gb, 2),
           "mem_total_mb": round(int(mi["MemTotal"].split()[0]) / 1024.0, 1),
           "mem_available_mb": round(int(mi["MemAvailable"].split()[0]) / 1024.0, 1),
           "hostname": socket.gethostname(),
           "cpu_model": cpu[0].split(":", 1)[1].strip() if cpu else "",
           "cpu_count": os.cpu_count(), "python": sys.version.split()[0],
           "versions": {d: version(d) for d in ("scikit-learn", "xgboost", "lightgbm",
                        "scipy", "pandas", "numpy", "matplotlib")},
           "threads": {f"{k}_NUM_THREADS": os.environ.get(f"{k}_NUM_THREADS")
                       for k in ("OMP", "OPENBLAS", "MKL", "NUMEXPR")},
           "rss_mb_sampled": round(rss_mb(), 1)}
    os.makedirs(LOGS, exist_ok=True)
    write_json(f"{LOGS}/preflight.json", rec)
    return rec

def make_model(mid, seed):
    cls, kw = MODEL_SPEC[mid]
    # M01 is the only model here that does not accept random_state.
    return cls(**kw) if mid == "M01" else cls(random_state=seed, **kw)

# ---- data loading and keys ----
def load_pool(ds):
    tr_name, te_name = FILES[ds]
    if ds == "unsw":
        tr = pd.read_csv(os.path.join(RAW, tr_name), low_memory=False)
        te = pd.read_csv(os.path.join(RAW, te_name), low_memory=False)
    else:
        tr, te = [pd.read_csv(os.path.join(RAW, n), header=None, names=NSL_COLUMNS,
                              low_memory=False) for n in (tr_name, te_name)]
        for d in (tr, te):
            d["label"] = (d["attack_name"] != "normal").astype(np.int8)
    if (len(tr), len(te)) != SIZES[ds]:
        sys.exit(f"{ds}: expected rows {SIZES[ds]}, got {(len(tr), len(te))}")
    return pd.concat([tr, te], ignore_index=True), len(tr)

def row_keys(df, cols):
    # String join under \x1f then factorize. Not a numeric hash: a collision
    # would be invisible and would corrupt every group and leakage count.
    s = df[cols[0]].astype(str)
    for c in cols[1:]:
        s = s + SEP + df[c].astype(str)
    return pd.factorize(s)[0]

def column_sets(ds, cols):
    if ds == "unsw":
        csb = [c for c in cols if c not in ("id", "attack_cat", "label")]
        return {"CS-A": [c for c in cols if c != "id"], "CS-B": csb, "CS-C": csb + ["label"]}
    csb = [c for c in NSL_COLUMNS if c not in ("attack_name", "difficulty_level")]
    return {"CS-A": list(NSL_COLUMNS), "CS-B": csb, "CS-C": csb + ["label"]}

def feature_frame(pool, ds):
    X = pool.drop(columns=[c for c in DROP_COLS[ds] if c in pool.columns])
    left = [c for c in DROP_COLS[ds] if c in X.columns]
    if left:
        sys.exit(f"{ds}: {left} survived into the feature matrix")
    return X

# ---- preprocessing, fitted on the training portion of one cell ----
def build_matrices(X, y, tr_idx, te_idx, ds):
    cats = [c for c in CATEGORICAL[ds] if c in X.columns]
    nums = [c for c in X.columns if c not in cats]
    Xtr, Xte = X.iloc[tr_idx], X.iloc[te_idx]
    keep = {}
    for c in cats:
        freq = Xtr[c].value_counts() / len(Xtr)
        keep[c] = set(freq[freq >= RARE_THRESHOLD].index)
    cat_tr = pd.DataFrame({c: Xtr[c].where(Xtr[c].isin(keep[c]), OTHER).astype(str)
                           for c in cats})
    cat_te = pd.DataFrame({c: Xte[c].where(Xte[c].isin(keep[c]), OTHER).astype(str)
                           for c in cats})
    enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False, dtype=np.float32)
    enc_tr, enc_te = enc.fit_transform(cat_tr), enc.transform(cat_te)
    scaler = StandardScaler()
    num_tr = scaler.fit_transform(Xtr[nums].to_numpy(dtype=np.float32))
    num_te = scaler.transform(Xte[nums].to_numpy(dtype=np.float32))
    out_tr = np.hstack([num_tr, enc_tr]).astype(np.float32)
    out_te = np.hstack([num_te, enc_te]).astype(np.float32)
    names = list(nums) + list(enc.get_feature_names_out(cats))
    if out_tr.shape[1] != out_te.shape[1] or len(names) != out_tr.shape[1]:
        sys.exit(f"column mismatch within cell: train {out_tr.shape[1]}, "
                 f"test {out_te.shape[1]}, names {len(names)}")
    return out_tr, out_te, y[tr_idx], y[te_idx], out_tr.shape[1]

# ---- splits ----
def split_cgroup(y, gid, ds, seed):
    n_train_target, test_target = SIZES[ds]
    sizes = np.bincount(gid)
    n_att = np.bincount(gid, weights=(y == 1)).astype(np.int64)
    n_nor = sizes - n_att
    attack_target = int(round(test_target * float((y == 1).mean())))
    normal_target = test_target - attack_target
    p_test = test_target / y.shape[0]
    rng = np.random.RandomState(seed)
    multi = np.flatnonzero(sizes > 1)
    rng.shuffle(multi)
    in_test = np.zeros(sizes.shape[0], dtype=bool)
    got_a = got_n = 0
    g_defl = r_defl = 0
    for g in multi:
        if rng.random_sample() >= p_test:  # one draw per group, order unchanged
            continue
        if got_a + n_att[g] <= attack_target and got_n + n_nor[g] <= normal_target:
            in_test[g] = True
            got_a, got_n = got_a + int(n_att[g]), got_n + int(n_nor[g])
        else:
            g_defl, r_defl = g_defl + 1, r_defl + int(sizes[g])
    single = np.flatnonzero(sizes == 1)
    s_att, s_nor = single[n_att[single] == 1], single[n_nor[single] == 1]
    rng.shuffle(s_att)
    rng.shuffle(s_nor)
    need_a, need_n = attack_target - got_a, normal_target - got_n
    if need_a > s_att.shape[0] or need_n > s_nor.shape[0]:
        sys.exit(f"{ds} seed {seed}: group split shortfall, attack short by "
                 f"{need_a - s_att.shape[0]}, normal short by {need_n - s_nor.shape[0]}")
    in_test[np.concatenate([s_att[:need_a], s_nor[:need_n]])] = True
    mask = in_test[gid]
    te_idx, tr_idx = np.flatnonzero(mask), np.flatnonzero(~mask)
    leak = int(np.isin(gid[te_idx], np.unique(gid[tr_idx])).sum())
    both = np.intersect1d(np.unique(gid[tr_idx]), np.unique(gid[te_idx])).shape[0]
    for name, exp, act in [("train size", n_train_target, tr_idx.shape[0]),
                           ("test size", test_target, te_idx.shape[0]),
                           ("test attacks", attack_target, int((y[te_idx] == 1).sum())),
                           ("CS-B leakage", 0, leak), ("groups on both sides", 0, both)]:
        if exp != act:
            sys.exit(f"{ds} seed {seed} C-group {name}: expected {exp}, got {act}")
    return tr_idx, te_idx, {"groups_deflected_by_capacity": g_defl,
                            "rows_deflected_by_capacity": r_defl}

def split_iter(ds, protocol, y, gid, seeds, n_repeats):
    if protocol == "B":
        rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=11)
        for i, (tr_idx, te_idx) in enumerate(rskf.split(np.zeros(y.shape[0]), y)):
            rep, fold = divmod(i, 5)
            if rep >= n_repeats:
                return
            yield rep, fold, f"r{rep}f{fold}", tr_idx, te_idx, None
        return
    for seed in seeds:
        defl = None
        if protocol == "A":
            tr_idx, te_idx = np.arange(SIZES[ds][0]), np.arange(SIZES[ds][0], y.shape[0])
        elif protocol == "C-naive":
            tr_idx, te_idx = train_test_split(
                np.arange(y.shape[0]), train_size=SIZES[ds][0], test_size=SIZES[ds][1],
                stratify=y, random_state=seed, shuffle=True)
        else:
            tr_idx, te_idx, defl = split_cgroup(y, gid, ds, seed)
        yield seed, None, f"{seed}", tr_idx, te_idx, defl

# ---- metrics and one fit ----
def metrics(y_true, y_pred, y_score):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {"accuracy": float(accuracy_score(y_true, y_pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
            "precision_attack": float(precision_score(y_true, y_pred, pos_label=1)),
            "recall_attack": float(recall_score(y_true, y_pred, pos_label=1)),
            "f1_attack": float(f1_score(y_true, y_pred, pos_label=1)),
            "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
            "mcc": float(matthews_corrcoef(y_true, y_pred)),
            "roc_auc": float(roc_auc_score(y_true, y_score)),
            "average_precision": float(average_precision_score(y_true, y_score)),
            "false_alarm_rate": float(fp) / float(fp + tn) if (fp + tn) else 0.0,
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}

def fit_predict(mid, seed, Xtr, ytr, Xte):
    model = make_model(mid, seed)
    t0 = time.time()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        model.fit(Xtr, ytr)
    fit_s = time.time() - t0
    seen = list(dict.fromkeys(str(w.message) for w in caught))
    warn = {"warnings_count": len(caught), "warnings_text": "; ".join(seen)[:500]}
    t0 = time.time()
    y_pred = model.predict(Xte)
    if mid == "M03":
        score, source = model.decision_function(Xte), "decision_function"
    else:
        score, source = model.predict_proba(Xte)[:, 1], "predict_proba"
    pred_s = time.time() - t0
    sampled = rss_mb()
    del model
    return (np.asarray(y_pred).astype(np.uint8), np.asarray(score, dtype=np.float32),
            fit_s, pred_s, source, sampled, peak_rss_mb(), warn)

# ---- records ----
def split_record(ds, protocol, sor, fold, tr_idx, te_idx, pool, gids, n_feat, defl=None):
    y, cat = pool["label"].to_numpy(), pool[CAT_LABEL[ds]].to_numpy()
    rec = {"dataset": ds, "protocol": protocol, "seed_or_repeat": sor, "fold": fold,
           "n_train": int(tr_idx.shape[0]), "n_test": int(te_idx.shape[0]),
           "train_attack_n": int((y[tr_idx] == 1).sum()),
           "train_attack_rate": float((y[tr_idx] == 1).mean()),
           "test_attack_n": int((y[te_idx] == 1).sum()),
           "test_attack_rate": float((y[te_idx] == 1).mean()),
           "train_category_counts": {str(k): int(v) for k, v in
                                     pd.Series(cat[tr_idx]).value_counts().items()},
           "test_category_counts": {str(k): int(v) for k, v in
                                    pd.Series(cat[te_idx]).value_counts().items()},
           "n_features_fitted": int(n_feat)}
    for key in ("a", "b", "c"):
        g = gids["CS-" + key.upper()]
        for part, ix in (("train", tr_idx), ("test", te_idx)):
            rec[f"dup_{part}_cs{key}"] = int(ix.shape[0] - np.unique(g[ix]).shape[0])
    gb = gids["CS-B"]
    hit = np.isin(gb[te_idx], np.unique(gb[tr_idx]))
    rec["leak_csb_rows"] = int(hit.sum())
    rec["leak_csb_rate"] = 100.0 * float(hit.sum()) / te_idx.shape[0]
    rec["leak_csb_attack_rows"] = int((y[te_idx][hit] == 1).sum())
    rec["achieved_size_deviation"] = None if protocol == "B" else {
        "train": int(tr_idx.shape[0] - SIZES[ds][0]),
        "test": int(te_idx.shape[0] - SIZES[ds][1])}
    rec.update(defl or {})
    return rec

def cell_record(ds, protocol, sor, fold, mid, sizes, rates, source, m, fit_s, pred_s,
                sampled, peak, hashes, warn=None):
    out = {"dataset": ds, "protocol": protocol, "seed_or_repeat": sor, "fold": fold,
           "model_id": mid, "model_name": MODEL_NAMES[mid], "n_train": sizes[0],
           "n_test": sizes[1], "n_features_fitted": sizes[2],
           "train_attack_n": rates[0], "train_attack_rate": rates[1],
           "test_attack_n": rates[2], "test_attack_rate": rates[3],
           "score_source": source}
    out.update(m)
    out.update({"fit_seconds": fit_s, "predict_seconds": pred_s, "peak_rss_mb": peak,
                "rss_mb_sampled": sampled, "pipeline_sha256": hashes,
                "warnings_count": (warn or {}).get("warnings_count"),
                "warnings_text": (warn or {}).get("warnings_text"),
                "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S")})
    return out

# ---- out of fold assembly for Protocol B ----
def fill_oof(oof, mid, n, te_idx, y_pred, y_score):
    if mid not in oof:
        oof[mid] = {"pred": np.zeros(n, dtype=np.uint8),
                    "score": np.zeros(n, dtype=np.float32),
                    "seen": np.zeros(n, dtype=bool)}
    oof[mid]["pred"][te_idx] = y_pred
    oof[mid]["score"][te_idx] = y_score
    oof[mid]["seen"][te_idx] = True

def write_oof(ds, outdir, rep, oof, y, models, hashes):
    for mid in models:
        if mid not in oof or not oof[mid]["seen"].all():
            log(f"{ds} B repeat {rep} {mid}: out of fold vector incomplete, not written")
            continue
        m = metrics(y, oof[mid]["pred"], oof[mid]["score"])
        rates, src = ((None, None, int((y == 1).sum()), float((y == 1).mean())),
                      "decision_function" if mid == "M03" else "predict_proba")
        write_json(f"{outdir}/cells/{ds}__B__r{rep}oof__{mid}.json",
                   cell_record(ds, "B", rep, None, mid, (None, int(y.shape[0]), None),
                               rates, src, m, None, None, rss_mb(), peak_rss_mb(), hashes))
        np.savez_compressed(f"{outdir}/preds/{ds}__B__r{rep}oof__{mid}.npz",
                            y_pred=oof[mid]["pred"], y_score=oof[mid]["score"])
        log(f"{ds} B repeat {rep} {mid} out of fold mcc {m['mcc']:.4f}")

# ---- the cell loop ----
def run_dataset(ds, outdir, models, seeds, n_repeats, hashes, protocols, probe=None):
    pool, n_tr = load_pool(ds)
    y = pool["label"].to_numpy().astype(np.int8)
    cs = column_sets(ds, list(pool.columns))
    gids = {k: row_keys(pool, v) for k, v in cs.items()}
    X = feature_frame(pool, ds)
    log(f"{ds}: pool {len(pool)} rows, {len(cs['CS-B'])} CS-B columns, rss {rss_mb():.0f}MB")
    for protocol in protocols:
        oof = {}
        for sor, fold, token, tr_idx, te_idx, defl in split_iter(
                ds, protocol, y, gids["CS-B"], seeds, n_repeats):
            Xtr, Xte, ytr, yte, n_feat = build_matrices(X, y, tr_idx, te_idx, ds)
            if protocol == "A" and n_feat != EXP_FEATURES_A[ds]:
                sys.exit(f"{ds} protocol A fitted columns: expected "
                         f"{EXP_FEATURES_A[ds]}, got {n_feat}")
            rec = split_record(ds, protocol, sor, fold, tr_idx, te_idx, pool, gids,
                               n_feat, defl)
            if protocol == "C-naive" and sor in SEEDS_B:
                lo, hi = CNAIVE_LEAK_RANGE[ds]
                if not lo <= round(rec["leak_csb_rate"], 4) <= hi:
                    sys.exit(f"{ds} C-naive seed {sor}: measured leakage "
                             f"{rec['leak_csb_rate']:.4f} outside {lo} to {hi}")
            sp = f"{outdir}/splits/{ds}__{protocol}__{token}"
            write_json(sp + ".json", rec)
            np.savez_compressed(sp + ".npz", train_idx=tr_idx.astype(np.int32),
                                test_idx=te_idx.astype(np.int32),
                                y_true=yte.astype(np.uint8))
            sizes = (int(tr_idx.shape[0]), int(te_idx.shape[0]), int(n_feat))
            rates = (rec["train_attack_n"], rec["train_attack_rate"],
                     rec["test_attack_n"], rec["test_attack_rate"])
            for mid in models:
                cell = f"{outdir}/cells/{ds}__{protocol}__{token}__{mid}.json"
                pred_path = f"{outdir}/preds/{ds}__{protocol}__{token}__{mid}.npz"
                if probe is None and os.path.exists(cell):
                    if protocol == "B":
                        z = np.load(pred_path)
                        fill_oof(oof, mid, y.shape[0], te_idx, z["y_pred"], z["y_score"])
                    continue
                if rss_mb() > RSS_ABORT_MB:
                    log(f"SKIP {ds} {protocol} {token} {mid}: rss {rss_mb():.0f}MB "
                        f"above {RSS_ABORT_MB}MB")
                    continue
                seed = SEEDS_B[sor] if protocol == "B" else sor
                try:
                    (y_pred, y_score, fit_s, pred_s, source, sampled, peak,
                     warn) = fit_predict(mid, seed, Xtr, ytr, Xte)
                except Exception:
                    with open(f"{LOGS}/errors.log", "a") as fh:
                        fh.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {ds} {protocol} "
                                 f"{token} {mid}\n{traceback.format_exc()}\n")
                    log(f"ERROR {ds} {protocol} {token} {mid}, cell skipped")
                    continue
                m = metrics(yte, y_pred, y_score)
                if probe is None:
                    write_json(cell, cell_record(ds, protocol, sor, fold, mid, sizes,
                                                 rates, source, m, fit_s, pred_s,
                                                 sampled, peak, hashes, warn))
                    np.savez_compressed(pred_path, y_pred=y_pred, y_score=y_score)
                    if protocol == "B":
                        fill_oof(oof, mid, y.shape[0], te_idx, y_pred, y_score)
                else:
                    probe.append({"model_id": mid, "model_name": MODEL_NAMES[mid],
                                  "dataset": ds, "n_train": sizes[0], "n_test": sizes[1],
                                  "fit_seconds": round(fit_s, 3),
                                  "predict_seconds": round(pred_s, 3),
                                  "rss_mb_sampled": round(sampled, 1),
                                  "peak_rss_mb": round(peak, 1),
                                  "warnings_count": warn["warnings_count"],
                                  "mcc": round(m["mcc"], 6)})
                log(f"{ds} {protocol} {token} {mid} mcc {m['mcc']:.4f} fit {fit_s:.1f}s "
                    f"predict {pred_s:.1f}s rss {sampled:.0f}MB peak {peak:.0f}MB")
                del y_pred, y_score
                gc.collect()

            del Xtr, Xte, ytr, yte
            gc.collect()
            if protocol == "B" and fold == 4 and probe is None:
                write_oof(ds, outdir, sor, oof, y, models, hashes)
                oof = {}
    del pool, X, gids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["smoke", "probe", "full"])
    ap.add_argument("--dataset", choices=["unsw", "nslkdd"])
    args = ap.parse_args()
    datasets = [args.dataset] if args.dataset else ["unsw", "nslkdd"]
    outdir = "results/raw" if args.mode == "full" else "results/smoke"  # never mixed
    for sub in ("cells", "preds", "splits"):
        os.makedirs(f"{outdir}/{sub}", exist_ok=True)
    pf, started = preflight(args.mode), time.strftime("%Y-%m-%dT%H:%M:%S")
    hashes = {f: sha256(f) for f in PIPELINE}

    if args.mode == "probe":
        rows = []
        for ds in datasets:
            run_dataset(ds, outdir, ALL_MODELS, [11], 0, hashes, ["A"], probe=rows)
        pd.DataFrame(rows).to_csv("results/smoke/timing_probe.csv", index=False)
        log(f"wrote results/smoke/timing_probe.csv, {len(rows)} rows")
    else:
        models = SMOKE_MODELS if args.mode == "smoke" else ALL_MODELS
        seeds = [11] if args.mode == "smoke" else SEEDS
        n_repeats = 1 if args.mode == "smoke" else 5
        log(f"mode {args.mode}, {len(os.listdir(f'{outdir}/cells'))} cell files already "
            f"present, those cells are skipped")
        for ds in datasets:
            run_dataset(ds, outdir, models, seeds, n_repeats, hashes, PROTOCOLS)

    write_json(f"{outdir}/manifest.json", {
        "mode": args.mode, "started_at": started,
        "ended_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "hostname": pf["hostname"], "python": pf["python"], "datasets": datasets,
        "cpu": pf["cpu_model"], "versions": pf["versions"], "threads": pf["threads"],
        "preflight": pf, "pipeline_sha256": hashes,
        "data_sha256": {f: sha256(os.path.join(RAW, f)) for f in sorted(os.listdir(RAW))}})
    log("manifest written")


if __name__ == "__main__":
    main()
