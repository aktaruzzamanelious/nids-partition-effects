"""Block 1C Tasks 1 five-class report and Tasks 2 to 5 for NSL-KDD.

Counting and sampling only. No model is fitted. Template: src/block1b_unsw.py.
"""
import json
import os
import resource
import time

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

RAW = "data/raw"
TRAIN_SIZE = 125973
TEST_SIZE = 22544
SEEDS = [11, 22, 33, 44, 55]

# The mapping below is external knowledge, from the KDD Cup 99 and NSL-KDD
# literature. It is not derivable from these files: neither file carries a
# category column. It is applied for reporting only and nothing is asserted
# against it. httptunnel is held out because published sources disagree on it.
FIVE_CLASS = {
    "DoS": ["back", "land", "neptune", "pod", "smurf", "teardrop", "mailbomb",
            "apache2", "processtable", "udpstorm"],
    "Probe": ["satan", "ipsweep", "nmap", "portsweep", "mscan", "saint"],
    "R2L": ["guess_passwd", "ftp_write", "imap", "phf", "multihop",
            "warezmaster", "warezclient", "spy", "xlock", "xsnoop",
            "snmpguess", "snmpgetattack", "sendmail", "named", "worm"],
    "U2R": ["buffer_overflow", "loadmodule", "rootkit", "perl", "sqlattack",
            "xterm", "ps"],
}
DISPUTED = "httptunnel"
EXPECTED_5C = {
    "train": {"Normal": 67343, "DoS": 45927, "Probe": 11656, "R2L": 995, "U2R": 52},
    "test": {"Normal": 9711, "DoS": 7458, "Probe": 2421, "R2L": 2754, "U2R": 200},
}


def rss_mb():
    with open("/proc/self/status") as fh:
        for line in fh:
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) / 1024.0
    return -1.0


def pct(num, den):
    return 0.0 if den == 0 else 100.0 * num / den


peak = [0.0]


def note_rss():
    r = rss_mb()
    if r > peak[0]:
        peak[0] = r
    return r


def columns():
    names = [f"f{i}" for i in range(41)]
    names[1] = "protocol_type"
    names[2] = "service"
    names[3] = "flag"
    return names + ["attack_name", "difficulty_level"]


COLS = columns()
tr = pd.read_csv(os.path.join(RAW, "KDDTrain+.txt"), header=None, names=COLS,
                 low_memory=False)
te = pd.read_csv(os.path.join(RAW, "KDDTest+.txt"), header=None, names=COLS,
                 low_memory=False)
for d in (tr, te):
    d["label"] = (d["attack_name"] != "normal").astype("int8")
merged = pd.concat([tr, te], ignore_index=True)
note_rss()

out = {}

# ------------------------------------------- Task 1, five-class reporting only
name_to_class = {}
for cls, names in FIVE_CLASS.items():
    for nm in names:
        name_to_class[nm] = cls
name_to_class["normal"] = "Normal"

five = {}
for kind, df in (("train", tr), ("test", te)):
    unmapped = sorted(set(df["attack_name"]) - set(name_to_class) - {DISPUTED})
    base = df["attack_name"].map(name_to_class)
    counts_r2l = {c: int((base == c).sum()) for c in
                  ("Normal", "DoS", "Probe", "R2L", "U2R")}
    n_disputed = int((df["attack_name"] == DISPUTED).sum())
    var_r2l = dict(counts_r2l)
    var_r2l["R2L"] += n_disputed
    var_u2r = dict(counts_r2l)
    var_u2r["U2R"] += n_disputed
    five[kind] = {
        "unmapped_names": unmapped,
        "n_disputed": n_disputed,
        "httptunnel_as_R2L": var_r2l,
        "httptunnel_as_U2R": var_u2r,
        "expected": EXPECTED_5C[kind],
        "match_as_R2L": var_r2l == EXPECTED_5C[kind],
        "match_as_U2R": var_u2r == EXPECTED_5C[kind],
        "attack_name_counts": {k: int(v) for k, v in
                               df["attack_name"].value_counts().items()},
    }
    print(f"five-class {kind}: unmapped {unmapped}, {DISPUTED} n={n_disputed}, "
          f"match as R2L {var_r2l == EXPECTED_5C[kind]}, "
          f"match as U2R {var_u2r == EXPECTED_5C[kind]}")
out["five_class"] = five

# ----------------------------------------------------------------- Task 2
feat = [c for c in COLS if c not in ("attack_name", "difficulty_level")]
CS = {"CS-A": list(COLS), "CS-B": feat, "CS-C": feat + ["label"]}
assert len(CS["CS-A"]) == 43 and len(CS["CS-B"]) == 41 and len(CS["CS-C"]) == 42

task2 = {}
for name, cols in CS.items():
    tr_s, te_s, me_s = tr[cols], te[cols], merged[cols]
    d_tr = int(tr_s.duplicated().sum())
    d_te = int(te_s.duplicated().sum())
    d_me = int(me_s.duplicated().sum())
    dist_tr = int(tr_s[tr_s.duplicated(keep=False)].drop_duplicates().shape[0])
    dist_te = int(te_s[te_s.duplicated(keep=False)].drop_duplicates().shape[0])
    dist_me = int(me_s[me_s.duplicated(keep=False)].drop_duplicates().shape[0])

    tr_keys = pd.MultiIndex.from_frame(tr_s)
    te_keys = pd.MultiIndex.from_frame(te_s)
    tr_u, te_u = tr_keys.unique(), te_keys.unique()
    te_in_tr = te_keys.isin(tr_u)
    tr_in_te = tr_keys.isin(te_u)
    n_te_in_tr, n_tr_in_te = int(te_in_tr.sum()), int(tr_in_te.sum())
    dist_shared = int(te_u.isin(tr_u).sum())
    ov = pd.concat([tr.loc[tr_in_te, "label"], te.loc[te_in_tr, "label"]])

    task2[name] = {
        "n_cols": len(cols),
        "d_tr": d_tr, "p_tr": pct(d_tr, len(tr)), "dist_tr": dist_tr,
        "d_te": d_te, "p_te": pct(d_te, len(te)), "dist_te": dist_te,
        "d_me": d_me, "p_me": pct(d_me, len(merged)), "dist_me": dist_me,
        "n_te_in_tr": n_te_in_tr, "p_te_in_tr": pct(n_te_in_tr, len(te)),
        "n_tr_in_te": n_tr_in_te, "p_tr_in_te": pct(n_tr_in_te, len(tr)),
        "dist_shared": dist_shared,
        "ov_attack": int((ov == 1).sum()), "ov_normal": int((ov == 0).sum()),
        "ov_attack_te": int((te.loc[te_in_tr, "label"] == 1).sum()),
        "ov_normal_te": int((te.loc[te_in_tr, "label"] == 0).sum()),
    }
    print(f"{name}: d_tr={d_tr} d_te={d_te} te_in_tr={n_te_in_tr} "
          f"tr_in_te={n_tr_in_te} d_merged={d_me} rss={note_rss():.0f}MB")
out["task2"] = task2

# ----------------------------------------------------------------- Task 3
sub = merged[CS["CS-B"]]
y = merged["label"].to_numpy()
n = len(merged)
keys = pd.util.hash_pandas_object(sub, index=False).to_numpy()
n_distinct_hash = int(pd.unique(keys).shape[0])
n_distinct_rows = int(n - sub.duplicated().sum())
gid, _ = pd.factorize(keys)
gsizes = np.bincount(gid)
n_groups = gsizes.shape[0]
note_rss()

lab_counts = pd.DataFrame({"g": gid, "y": y}).groupby("g")["y"].agg(["size", "sum"])
nm_by_gid = pd.DataFrame({"g": gid, "c": merged["attack_name"].to_numpy()})
top10 = []
for g in np.argsort(-gsizes)[:10]:
    sz = int(gsizes[g])
    n_att = int(lab_counts.loc[g, "sum"])
    cats = nm_by_gid.loc[nm_by_gid["g"] == g, "c"].value_counts()
    top10.append({"size": sz, "attack": n_att, "normal": sz - n_att,
                  "attack_names": ", ".join(f"{k} {v:,}" for k, v in cats.items())})

task3 = {
    "n_rows": n, "n_groups": n_groups,
    "n_distinct_hash": n_distinct_hash, "n_distinct_rows": n_distinct_rows,
    "size1": int((gsizes == 1).sum()),
    "size2_10": int(((gsizes >= 2) & (gsizes <= 10)).sum()),
    "size_gt10": int((gsizes > 10).sum()),
    "median": float(np.median(gsizes)), "mean": float(gsizes.mean()),
    "max": int(gsizes.max()),
    "rows_in_multi": int(gsizes[gsizes > 1].sum()),
    "max_pct_of_test_target": pct(int(gsizes.max()), TEST_SIZE),
    "top10": top10,
}
out["task3"] = task3
print(f"task3: {n_groups:,} groups, max {int(gsizes.max()):,}, rss {note_rss():.0f}MB")

# ----------------------------------------------------------------- Task 4
idx = np.arange(n)
sim = []
for seed in SEEDS:
    i_tr, i_te = train_test_split(idx, stratify=y, train_size=TRAIN_SIZE,
                                  test_size=TEST_SIZE, random_state=seed)
    train_keys = set(keys[i_tr].tolist())
    te_k = keys[i_te]
    hit = np.fromiter((k in train_keys for k in te_k.tolist()), dtype=bool,
                      count=te_k.shape[0])
    y_te = y[i_te]
    n_hit = int(hit.sum())
    sim.append({"seed": seed, "n_test": int(i_te.shape[0]), "leaked": n_hit,
                "pct": pct(n_hit, i_te.shape[0]),
                "leaked_attack": int((y_te[hit] == 1).sum()),
                "leaked_normal": int((y_te[hit] == 0).sum()),
                "test_attack": int((y_te == 1).sum()),
                "test_normal": int((y_te == 0).sum())})
    print(f"  seed {seed}: leaked {n_hit:,} ({pct(n_hit, i_te.shape[0]):.4f}%) "
          f"rss {note_rss():.0f}MB")
    del train_keys

pcts = [s["pct"] for s in sim]
task4 = {"seeds": sim, "mean_pct": float(np.mean(pcts)),
         "min_pct": float(np.min(pcts)), "max_pct": float(np.max(pcts)),
         "publisher_n": task2["CS-B"]["n_te_in_tr"],
         "publisher_pct": task2["CS-B"]["p_te_in_tr"]}
task4["ratio_mean"] = (task4["mean_pct"] / task4["publisher_pct"]
                       if task4["publisher_pct"] else None)
out["task4"] = task4
print(f"task4: mean {task4['mean_pct']:.4f}% vs publisher "
      f"{task4['publisher_pct']:.4f}%")

# ----------------------------------------------------------------- Task 5
rng = np.random.default_rng(11)
g_att = lab_counts["sum"].to_numpy().astype(int)
g_nor = gsizes - g_att
pool_att = int((y == 1).sum())
target_te_att = int(round(TEST_SIZE * pool_att / n))
target_te_nor = TEST_SIZE - target_te_att

to_test = np.zeros(n_groups, dtype=bool)
cur_n = cur_a = cur_o = 0
for g in rng.permutation(n_groups):
    s, a, o = int(gsizes[g]), int(g_att[g]), int(g_nor[g])
    if cur_n + s > TEST_SIZE or cur_a + a > target_te_att or cur_o + o > target_te_nor:
        continue
    to_test[g] = True
    cur_n += s
    cur_a += a
    cur_o += o
    if cur_n == TEST_SIZE:
        break

in_test = to_test[gid]
ach_te = int(in_test.sum())
ach_tr = n - ach_te
te_att = int((y[in_test] == 1).sum())
tr_att = int((y[~in_test] == 1).sum())
train_keys = set(keys[~in_test].tolist())
leak = int(sum(1 for k in keys[in_test].tolist() if k in train_keys))

task5 = {
    "seed": 11, "target_train": TRAIN_SIZE, "target_test": TEST_SIZE,
    "achieved_train": ach_tr, "achieved_test": ach_te,
    "dev_train_abs": ach_tr - TRAIN_SIZE,
    "dev_train_pct": pct(abs(ach_tr - TRAIN_SIZE), TRAIN_SIZE),
    "dev_test_abs": ach_te - TEST_SIZE,
    "dev_test_pct": pct(abs(ach_te - TEST_SIZE), TEST_SIZE),
    "train_attack": tr_att, "train_normal": ach_tr - tr_att,
    "train_attack_pct": pct(tr_att, ach_tr),
    "test_attack": te_att, "test_normal": ach_te - te_att,
    "test_attack_pct": pct(te_att, ach_te),
    "pool_attack_pct": pct(pool_att, n),
    "target_te_att": target_te_att, "target_te_nor": target_te_nor,
    "leakage": leak, "n_groups_in_test": int(to_test.sum()),
}
out["task5"] = task5
print(f"task5: train {ach_tr:,} test {ach_te:,} leak {leak} rss {note_rss():.0f}MB")

out["peak_rss_mb"] = peak[0]
out["ru_maxrss_mb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
with open("results/raw/block1c_nslkdd.json", "w") as fh:
    json.dump(out, fh, indent=2)
print(f"peak rss {peak[0]:.1f} MB, ru_maxrss {out['ru_maxrss_mb']:.1f} MB")
