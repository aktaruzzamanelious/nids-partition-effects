"""Block 5 analysis. Runs the Stage 0 gate and every pre-declared statistic, 5.1 to 5.8.

Reads results/raw/ only. Writes results/analysis.json at full precision; the tables
are built from it by src/tables.py.
Usage: python src/analyze.py
"""
import os

for _lib in ("OMP", "OPENBLAS", "MKL", "NUMEXPR"):
    os.environ[f"{_lib}_NUM_THREADS"] = "2"

import glob
import hashlib
import itertools
import json
import shutil
import time
from collections import Counter

import numpy as np
import pandas as pd
from scipy import stats

RAW, OUT_JSON = "results/raw", "results/analysis.json"
EXP_HASH = "26294dba0d452fc58e774420b3faa11281c5a3ae240cd7b07cc5b0a0fa2a8ee7"
FROZEN = {"src/verify.py": "4e0f2b14a6b7505105f0512fc43d0f0090bb5f1da6e6c82cfd1a22705c65cd6c",
          "src/preprocess.py": "5340d364711d354640c0c97c07cf23cd3398b0e0af5e88d6c2dac0030b061068"}
DATASETS = ["unsw", "nslkdd"]
ARMS = ["A", "B", "C-naive", "C-group"]
SEEDS = [11, 22, 33, 44, 55, 66, 77, 88, 99, 110]
REPEATS = [0, 1, 2, 3, 4]
MODELS = [f"M{i:02d}" for i in range(1, 11)]
SEVEN = MODELS[3:]
METRICS = ["mcc", "accuracy", "macro_f1"]
CONTRASTS = [("A", "C-naive"), ("C-naive", "C-group"), ("B", "C-naive"), ("A", "B")]
N_BOOT, BOOT_SEED, BOOT_LIMIT_S = 2000, 11, 1800.0
A_NOTE = ("Protocol A: Friedman and Wilcoxon not run. Seven models (M01, M02, M03, M07, M08, "
          "M09, M10) give identical predictions at every seed under the fixed split; within-A "
          "separability comes from the bootstrap intervals on each model's metric.")
ID_NOTE = ("chi-square equals its maximum N(k-1); every block ranks the ten models "
           "identically, so the Iman-Davenport F is infinite in the limit and its p-value is 0")
TAU_P_LABEL = ("p-value of scipy.stats.kendalltau under the null that the two rankings are "
               "independent; not the test of any hypothesis in this study")


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_cells():
    rows = []
    for path in sorted(glob.glob(f"{RAW}/cells/*.json")):
        with open(path) as fh:
            rec = json.load(fh)
        rec["token"] = os.path.basename(path).split("__")[2]
        rec["oof"] = rec["token"].endswith("oof")
        rec["exp_hash"] = rec["pipeline_sha256"]["src/experiment.py"]
        rows.append(rec)
    return pd.DataFrame(rows)


def stage0(cells):
    checks = []

    def add(name, expected, actual):
        checks.append({"check": name, "expected": str(expected), "actual": str(actual),
                       "pass": str(expected) == str(actual)})

    fitted, oof = cells[~cells["oof"]], cells[cells["oof"]]
    add("results/raw/cells/ file count", 1200, len(os.listdir(f"{RAW}/cells")))
    add("of which fitted cells", 1100, len(fitted))
    add("of which out of fold aggregates", 100, len(oof))
    add("results/raw/preds/ file count", 1200, len(os.listdir(f"{RAW}/preds")))
    sp = os.listdir(f"{RAW}/splits")
    add("results/raw/splits/ file count (json, npz)", "220 (110, 110)",
        f"{len(sp)} ({sum(f.endswith('.json') for f in sp)}, "
        f"{sum(f.endswith('.npz') for f in sp)})")
    man = f"{RAW}/manifest.json"
    mode = json.load(open(man)).get("mode") if os.path.exists(man) else "missing"
    add("results/raw/manifest.json exists, mode", "full", mode)
    hashes = sorted(fitted["exp_hash"].unique())
    add("distinct src/experiment.py hash across fitted cells", 1, len(hashes))
    add("that hash", EXP_HASH, hashes[0] if len(hashes) == 1 else hashes)
    for path, h in FROZEN.items():
        add(f"{path} hash", h, sha256(path))
    for ds in DATASETS:
        for arm, n in zip(ARMS, (100, 250, 100, 100)):
            add(f"{ds} fitted cells, arm {arm}", n,
                int(((fitted["dataset"] == ds) & (fitted["protocol"] == arm)).sum()))
        sub = oof[oof["dataset"] == ds]
        add(f"{ds} out of fold records (models x repeats)", "50 (10 x 5)",
            f"{len(sub)} ({sub['model_id'].nunique()} x {sub['seed_or_repeat'].nunique()})")
    free_gb = shutil.disk_usage(os.path.expanduser("~")).free / 2 ** 30
    add("free disk at least 5 GB", True, free_gb >= 5.0)
    checks[-1]["actual"] += f" ({free_gb:.1f} GB)"
    return checks


def instances(arm):
    return REPEATS if arm == "B" else SEEDS


def ranked_records(cells, ds, arm):
    sub = cells[(cells["dataset"] == ds) & (cells["protocol"] == arm)]
    sub = sub[sub["oof"]] if arm == "B" else sub
    return sub.set_index(["seed_or_repeat", "model_id"])


def metric_matrix(recs, arm, col):
    return np.array([[recs.loc[(i, m), col] for m in MODELS] for i in instances(arm)],
                    dtype=np.float64)


def rank_rows(mat):
    return stats.rankdata(-mat, method="average", axis=1)


def summary(vals):
    v = np.asarray(vals, dtype=np.float64)
    return {"mean": float(v.mean()), "min": float(v.min()), "max": float(v.max()),
            "p5": float(np.percentile(v, 5)), "n_pairs": int(v.size)}


def ci(vals):
    lo, hi = np.percentile(np.asarray(vals, dtype=np.float64), [2.5, 97.5])
    return [float(lo), float(hi)]


def pair_stats(ra, rb, within, cols=None):
    cols = slice(None) if cols is None else cols
    pairs = (itertools.combinations(range(len(ra)), 2) if within
             else itertools.product(range(len(ra)), range(len(rb))))
    taus, rhos, ps = [], [], []
    for i, j in pairs:
        a, b = ra[i][cols], (ra if within else rb)[j][cols]
        t = stats.kendalltau(a, b, variant="b")
        r = stats.spearmanr(a, b)
        if not (np.isfinite(t.statistic) and np.isfinite(r.statistic)):
            raise RuntimeError(f"nan tau or rho for rank vectors {a.tolist()} and {b.tolist()}")
        taus.append(float(t.statistic))
        rhos.append(float(r.statistic))
        ps.append(float(t.pvalue))
    return taus, rhos, ps


def load_codes(ds, arm):
    # Code c = 2 * y_true + y_pred, so bincount order is tn, fp, fn, tp.
    if arm == "B":
        # Pool y_true is reassembled from each repeat's five test folds.
        y = None
        for rep in REPEATS:
            folds = [np.load(f"{RAW}/splits/{ds}__B__r{rep}f{f}.npz") for f in range(5)]
            yr = np.full(sum(z["test_idx"].shape[0] for z in folds), 255, dtype=np.uint8)
            for z in folds:
                yr[z["test_idx"]] = z["y_true"]
            if (yr == 255).any() or (y is not None and not np.array_equal(y, yr)):
                raise RuntimeError(f"{ds} B repeat {rep}: pooled y_true incomplete or differs")
            y = yr
        ys = {rep: y for rep in REPEATS}
        pred_tok = {rep: f"r{rep}oof" for rep in REPEATS}
    else:
        ys = {s: np.load(f"{RAW}/splits/{ds}__{arm}__{s}.npz")["y_true"] for s in SEEDS}
        pred_tok = {s: str(s) for s in SEEDS}
    out = []
    for i in instances(arm):
        out.append([2 * ys[i] + np.load(f"{RAW}/preds/{ds}__{arm}__{pred_tok[i]}__{m}.npz")
                    ["y_pred"] for m in MODELS])
    return np.array(out, dtype=np.uint8)


def counts(codes, w):
    k, m, n = codes.shape
    flat = codes.reshape(k * m, n)
    return np.array([np.bincount(c, weights=w, minlength=4) for c in flat]).reshape(k, m, 4)


def metrics_from_counts(cnt):
    tn, fp, fn, tp = (cnt[..., i] for i in range(4))
    n = tn + fp + fn + tp
    with np.errstate(divide="ignore", invalid="ignore"):
        den = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
        mcc = np.where(den > 0, (tp * tn - fp * fn) / den, 0.0)
        f1p = np.where(2 * tp + fp + fn > 0, 2 * tp / (2 * tp + fp + fn), 0.0)
        f1n = np.where(2 * tn + fp + fn > 0, 2 * tn / (2 * tn + fp + fn), 0.0)
    return {"mcc": mcc, "accuracy": (tp + tn) / n, "macro_f1": (f1p + f1n) / 2.0}


def mean_pair_stats(ra, rb, cache):
    taus, rhos = [], []
    for a, b in itertools.product(ra, rb):
        key = a.tobytes() + b.tobytes()
        if key not in cache:
            t = stats.kendalltau(a, b, variant="b").statistic
            r = stats.spearmanr(a, b).statistic
            if not (np.isfinite(t) and np.isfinite(r)):
                raise RuntimeError(f"nan in bootstrap for {a.tolist()} and {b.tolist()}")
            cache[key] = (float(t), float(r))
        taus.append(cache[key][0])
        rhos.append(cache[key][1])
    return float(np.mean(taus)), float(np.mean(rhos))


def bootstrap(ds, codes):
    rng = np.random.default_rng(BOOT_SEED)
    model_means = {arm: np.zeros((N_BOOT, len(METRICS), 10)) for arm in ARMS}
    tau = {c: np.zeros((N_BOOT, len(METRICS))) for c in CONTRASTS}
    rho = {c: np.zeros((N_BOOT, len(METRICS))) for c in CONTRASTS}
    t0 = time.time()
    for it in range(N_BOOT):
        ranks, cache = {}, {}
        for arm in ARMS:
            n_eval = codes[arm].shape[2]
            idx = rng.integers(0, n_eval, size=n_eval)
            w = np.bincount(idx, minlength=n_eval).astype(np.float64)
            met = metrics_from_counts(counts(codes[arm], w))
            for k, mname in enumerate(METRICS):
                model_means[arm][it, k] = met[mname].mean(axis=0)
                ranks[(arm, mname)] = rank_rows(met[mname])
        for c in CONTRASTS:
            for k, mname in enumerate(METRICS):
                tau[c][it, k], rho[c][it, k] = mean_pair_stats(
                    ranks[(c[0], mname)], ranks[(c[1], mname)], cache)
        if it == 19:
            proj = (time.time() - t0) / 20 * N_BOOT
            log(f"{ds} bootstrap projection {proj / 60:.1f} min for 2000 resamples")
            if proj > BOOT_LIMIT_S:
                raise SystemExit(f"STOP: {ds} bootstrap projects {proj / 60:.1f} min, "
                                 f"above the 30 minute limit. Resample count not reduced.")
        if (it + 1) % 250 == 0:
            log(f"{ds} bootstrap {it + 1}/{N_BOOT}, {(time.time() - t0) / 60:.1f} min")
    return model_means, tau, rho, {"projected_s": proj, "actual_s": time.time() - t0}


def holm(p):
    p = np.asarray(p, dtype=np.float64)
    order = np.argsort(p)
    adj = np.empty_like(p)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(p) - rank) * p[i]))
        adj[i] = running
    return adj


def friedman(mat):
    n_blocks, k = mat.shape
    res = stats.friedmanchisquare(*[mat[:, j] for j in range(k)])
    chi2, p_chi2 = float(res.statistic), float(res.pvalue)
    if not (np.isfinite(chi2) and np.isfinite(p_chi2)):
        raise RuntimeError(f"Friedman returned nan for input {mat.tolist()}")
    df1, df2 = k - 1, (k - 1) * (n_blocks - 1)
    out = {"N": n_blocks, "k": k, "chi2": chi2, "p_chi2": p_chi2, "df1": df1, "df2": df2}
    if n_blocks * (k - 1) - chi2 <= 1e-9:
        out.update({"F_F": "inf", "p_F": 0.0, "F_F_note": ID_NOTE})
    else:
        ff = (n_blocks - 1) * chi2 / (n_blocks * (k - 1) - chi2)
        out.update({"F_F": float(ff), "p_F": float(stats.f.sf(ff, df1, df2))})
    out["disagree_at_0.05"] = (p_chi2 < 0.05) != (out["p_F"] < 0.05)
    mean_rank = rank_rows(mat).mean(axis=0)
    order = [MODELS[j] for j in np.argsort(mean_rank, kind="stable")]
    out["mean_rank"] = dict(zip(MODELS, mean_rank.tolist()))
    out["wilcoxon_ran"] = out["p_F"] < 0.05
    if out["wilcoxon_ran"]:
        rows = []
        for a, b in zip(order[:-1], order[1:]):
            xa, xb = mat[:, MODELS.index(a)], mat[:, MODELS.index(b)]
            r = stats.wilcoxon(xa, xb, method="exact")
            if not np.isfinite(r.pvalue):
                raise RuntimeError(f"Wilcoxon nan for {a} {xa.tolist()} and {b} {xb.tolist()}")
            rows.append({"pair": f"{a} vs {b}", "statistic": float(r.statistic),
                         "p": float(r.pvalue)})
        for row, padj in zip(rows, holm([r["p"] for r in rows])):
            row["p_holm"] = float(padj)
        out["wilcoxon"] = rows
    return out


def top_set(mean_rank, k):
    order = np.argsort(mean_rank, kind="stable")
    cut = mean_rank[order[k - 1]]
    tied = bool(k < len(mean_rank) and mean_rank[order[k]] == cut)
    return [MODELS[j] for j in order[:k]], tied


def split_records():
    recs = []
    for path in sorted(glob.glob(f"{RAW}/splits/*.json")):
        with open(path) as fh:
            recs.append(json.load(fh))
    return recs


def classifier_facts(cells, codes_a):
    fitted = cells[~cells["oof"]]
    rows = {}
    for j, m in enumerate(MODELS):
        sub = fitted[fitted["model_id"] == m]
        det = all(bool((codes_a[ds][:, j] == codes_a[ds][0, j]).all()) for ds in DATASETS)
        rows[m] = {"class": sub["model_name"].iloc[0],
                   "score_source": ";".join(sorted(sub["score_source"].unique())),
                   "deterministic_under_fixed_split_measured": det,
                   "n_fits": len(sub), "warnings_total": int(sub["warnings_count"].sum()),
                   "warning_texts": " | ".join(sorted(set(sub["warnings_text"]) - {""}))}
    return rows


def main():
    t_start = time.time()
    cells = load_cells()
    gate = stage0(cells)
    for c in gate:
        log(f"{'PASS' if c['pass'] else 'FAIL'}  {c['check']}: expected {c['expected']}, "
            f"actual {c['actual']}")
    if not all(c["pass"] for c in gate):
        raise SystemExit("STOP: Stage 0 failed. Nothing computed.")
    res = {"stage0": gate, "rank_vectors": {}, "within_arm": {}, "between_arm": {},
           "bootstrap": {}, "friedman": {}, "top_k": {}, "criteria": {}, "weak_check": {},
           "per_model": {}, "mean_rank": {}, "leakage": {}, "tau_p_value_label": TAU_P_LABEL}
    splits = split_records()
    codes_a = {}
    for ds in DATASETS:
        recs = {arm: ranked_records(cells, ds, arm) for arm in ARMS}
        mats = {(arm, m): metric_matrix(recs[arm], arm, m) for arm in ARMS for m in METRICS}
        ranks = {k: rank_rows(v) for k, v in mats.items()}
        res["rank_vectors"][ds] = {arm: {m: dict(zip(map(str, instances(arm)),
                                                     ranks[(arm, m)].tolist()))
                                         for m in METRICS} for arm in ARMS}
        log(f"{ds}: loading prediction codes")
        codes = {arm: load_codes(ds, arm) for arm in ARMS}
        codes_a[ds] = codes["A"]
        for arm in ARMS:
            cnt = counts(codes[arm], np.ones(codes[arm].shape[2]))
            want = np.stack([metric_matrix(recs[arm], arm, c)
                             for c in ("tn", "fp", "fn", "tp")], axis=-1)
            if not np.array_equal(cnt, want):
                raise SystemExit(f"STOP: {ds} {arm} counts from codes differ from cells")
            got = metrics_from_counts(cnt)
            for m in METRICS:
                if np.abs(got[m] - mats[(arm, m)]).max() > 1e-12:
                    raise SystemExit(f"STOP: {ds} {arm} {m} from counts differs from cells")
        log(f"{ds}: codes reproduce every stored confusion matrix and metric")

        wa = res["within_arm"][ds] = {}
        for arm in ARMS:
            wa[arm] = {}
            for m in METRICS:
                taus, _, _ = pair_stats(ranks[(arm, m)], None, True)
                wa[arm][m] = {**summary(taus), "taus": taus}
        ba = res["between_arm"][ds] = {}
        for a, b in CONTRASTS:
            key = f"{a} vs {b}"
            ba[key] = {}
            for label, cols in (("ten", None), ("seven", slice(3, 10))):
                ba[key][label] = {}
                for m in METRICS:
                    taus, rhos, ps = pair_stats(ranks[(a, m)], ranks[(b, m)], False, cols)
                    ba[key][label][m] = {"tau_b": summary(taus), "rho": summary(rhos),
                                         "tau_b_p_values": ps}

        log(f"{ds}: bootstrap starting, {N_BOOT} resamples, seed {BOOT_SEED}")
        mm, btau, brho, timing = bootstrap(ds, codes)
        del codes
        bs = res["bootstrap"][ds] = {"timing": timing, "contrasts": {}, "model_ci": {}}
        for a, b in CONTRASTS:
            bs["contrasts"][f"{a} vs {b}"] = {m: {
                "tau_b_ci": ci(btau[(a, b)][:, k]), "rho_ci": ci(brho[(a, b)][:, k]),
                "tau_b_dist": btau[(a, b)][:, k].tolist(),
                "rho_dist": brho[(a, b)][:, k].tolist()} for k, m in enumerate(METRICS)}
        for arm in ARMS:
            bs["model_ci"][arm] = {m: {mid: ci(mm[arm][:, k, j]) for j, mid in enumerate(MODELS)}
                                   for k, m in enumerate(METRICS)}

        pm = res["per_model"][ds] = {}
        for arm in ARMS:
            pm[arm] = {}
            for j, mid in enumerate(MODELS):
                row = {"dataset": ds, "arm": arm, "model_id": mid}
                for m in METRICS:
                    v = mats[(arm, m)][:, j]
                    row[f"{m}_mean"], row[f"{m}_sd"] = float(v.mean()), float(v.std(ddof=1))
                row["mcc_mean_rank"] = float(ranks[(arm, "mcc")][:, j].mean())
                for m in ("balanced_accuracy", "roc_auc", "average_precision",
                          "false_alarm_rate"):
                    row[f"{m}_mean"] = float(metric_matrix(recs[arm], arm, m)[:, j].mean())
                pm[arm][mid] = row

        mean_rank = {arm: ranks[(arm, "mcc")].mean(axis=0) for arm in ARMS}
        res["mean_rank"][ds] = {arm: mean_rank[arm].tolist() for arm in ARMS}

        tk = res["top_k"][ds] = {"within": {}, "across": {}}
        for arm in ARMS:
            r = ranks[(arm, "mcc")]
            tops = [MODELS[int(np.argmin(v))] for v in r]
            ties = int(sum((v == v.min()).sum() > 1 for v in r))
            modal, cnt = Counter(tops).most_common(1)[0]
            tk["within"][arm] = {"modal_top": modal, "count": cnt, "of": len(r),
                                 "instances_with_tied_top": ties}
        for a, b in CONTRASTS:
            (ta, tia), (tb, tib) = top_set(mean_rank[a], 1), top_set(mean_rank[b], 1)
            (sa, sia), (sb, sib) = top_set(mean_rank[a], 3), top_set(mean_rank[b], 3)
            tk["across"][f"{a} vs {b}"] = {
                "top_a": ta[0], "top_b": tb[0], "same_top": ta[0] == tb[0],
                "top3_a": sa, "top3_b": sb, "top3_intersection": len(set(sa) & set(sb)),
                "tie_at_cut": bool(tia or tib or sia or sib)}

        wc = res["weak_check"][ds] = {}
        for arm in ARMS:
            wc[arm] = {}
            for m in METRICS:
                r = ranks[(arm, m)]
                mr = r.mean(axis=0)
                # MODELS order puts M01, M02, M03 in columns 0 to 2.
                bottom3 = sorted(MODELS[j] for j in np.argsort(mr)[-3:])
                wc[arm][m] = {"bottom3_by_mean_rank": bottom3,
                              "weak_strictly_bottom3_by_mean_rank":
                                  bool(mr[:3].min() > mr[3:].max()),
                              "instances_weak_strictly_bottom3":
                                  int(sum(v[:3].min() > v[3:].max() for v in r)),
                              "of": len(r)}

        fr = res["friedman"][ds] = {"A": A_NOTE}
        for arm in ("B", "C-naive", "C-group"):
            fr[arm] = friedman(mats[(arm, "mcc")])
            if fr[arm]["disagree_at_0.05"]:
                log(f"{ds} {arm}: Friedman chi-square and Iman-Davenport disagree at 0.05")

        leak = {arm: [s["leak_csb_rate"] for s in splits if s["dataset"] == ds and
                      s["protocol"] == arm] for arm in ARMS}
        res["leakage"][ds] = {arm: {"mean": float(np.mean(v)), "min": float(np.min(v)),
                                    "max": float(np.max(v)), "n": len(v)}
                              for arm, v in leak.items()}

        cr = res["criteria"][ds] = {"H1": {}, "H3": {}}
        for k, m in enumerate(METRICS):
            cr["H1"][m] = {}
            for arm in ("C-naive", "C-group"):
                point = float((mats[("A", m)].mean(axis=0) - mats[(arm, m)].mean(axis=0)).mean())
                boot = (mm["A"][:, k] - mm[arm][:, k]).mean(axis=1)
                lo, hi = ci(boot)
                cr["H1"][m][f"A minus {arm}"] = {"mean_diff": point, "ci": [lo, hi],
                                                 "ci_excludes_zero": bool(lo > 0 or hi < 0)}
        for label, arm in (("primary", "C-naive"), ("secondary", "C-group")):
            # A vs C-group is not a 5.3 contrast, so both readings are computed here alike.
            cross = float(np.mean(pair_stats(ranks[("A", "mcc")], ranks[(arm, "mcc")], False)[0]))
            floor = wa[arm]["mcc"]["p5"]
            cr[f"H2_{label}"] = {"mean_cross_tau_b_A_vs_" + arm: cross,
                                 "p5_within_" + arm: floor, "criterion": bool(cross < floor)}
        for k, m in enumerate(METRICS):
            d_a = 1 - ba["A vs C-naive"]["ten"][m]["tau_b"]["mean"]
            d_b = 1 - ba["B vs C-naive"]["ten"][m]["tau_b"]["mean"]
            ia = sorted(1 - np.array(bs["contrasts"]["A vs C-naive"][m]["tau_b_ci"]))
            ib = sorted(1 - np.array(bs["contrasts"]["B vs C-naive"][m]["tau_b_ci"]))
            gt, sep = d_a > d_b, bool(ia[0] > ib[1] or ib[0] > ia[1])
            cr["H3"][m] = {"d_A_Cnaive": d_a, "d_A_Cnaive_ci": [float(x) for x in ia],
                           "d_B_Cnaive": d_b, "d_B_Cnaive_ci": [float(x) for x in ib],
                           "d_A_gt_d_B": bool(gt), "intervals_do_not_overlap": sep,
                           "criterion": bool(gt and sep)}
        k = METRICS.index("mcc")
        point = float((mats[("C-naive", "mcc")].mean(axis=0)
                       - mats[("C-group", "mcc")].mean(axis=0)).mean())
        lo, hi = ci((mm["C-naive"][:, k] - mm["C-group"][:, k]).mean(axis=1))
        cr["H4"] = {"mcc_mean_diff_Cnaive_minus_Cgroup": point, "ci": [lo, hi],
                    "ci_excludes_zero": bool(lo > 0 or hi < 0),
                    "tau_b_mean": ba["C-naive vs C-group"]["ten"]["mcc"]["tau_b"]["mean"],
                    "tau_b_ci": bs["contrasts"]["C-naive vs C-group"]["mcc"]["tau_b_ci"],
                    "leak_rate_pct_Cnaive": res["leakage"][ds]["C-naive"],
                    "leak_rate_pct_Cgroup": res["leakage"][ds]["C-group"]}

        log(f"{ds}: done")

    res["classifiers"] = classifier_facts(cells, codes_a)
    fitted = cells[~cells["oof"]]
    fit = fitted.groupby("model_id")["fit_seconds"]
    worst = fitted.loc[fitted["fit_seconds"].idxmax()]
    res["diagnostics"] = {
        "fit_seconds_by_model": {m: {"median": float(g.median()), "q1": float(g.quantile(.25)),
                                     "q3": float(g.quantile(.75)), "n": int(g.size)}
                                 for m, g in fit},
        "slowest_cell": {"cell": f"{worst['dataset']}__{worst['protocol']}__{worst['token']}"
                                 f"__{worst['model_id']}",
                         "fit_seconds": float(worst["fit_seconds"]),
                         "model_mean_s": float(fit.mean()[worst["model_id"]]),
                         "model_next_slowest_s": float(fit.get_group(worst["model_id"])
                                                       .nlargest(2).iloc[1])},
        "run_peak_rss_mb": float(cells["peak_rss_mb"].max()),
        "wall_clock_s": time.time() - t_start}
    with open(OUT_JSON + ".tmp", "w") as fh:
        json.dump(res, fh)
    os.replace(OUT_JSON + ".tmp", OUT_JSON)
    log(f"wrote {OUT_JSON}, wall clock {(time.time() - t_start) / 60:.1f} min")


if __name__ == "__main__":
    main()
