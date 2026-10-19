"""Block 1B Tasks 3, 4 and 5 for UNSW-NB15. Counting and sampling only.

No model is fitted here. NSL-KDD is not touched by this script: the schema
stop recorded in logs/nslkdd-schema-stop.md is still in force.
"""
import json
import os
import resource
import time

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

RAW = "data/raw"
TRAIN = "UNSW_NB15_training-set.csv"
TEST = "UNSW_NB15_testing-set.csv"
TRAIN_SIZE = 175341
TEST_SIZE = 82332
SEEDS = [11, 22, 33, 44, 55]


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


tr = pd.read_csv(os.path.join(RAW, TRAIN), low_memory=False)
te = pd.read_csv(os.path.join(RAW, TEST), low_memory=False)
merged = pd.concat([tr, te], ignore_index=True)
note_rss()

CS_B = [c for c in tr.columns if c not in ("id", "attack_cat", "label")]
assert len(CS_B) == 42, len(CS_B)

sub = merged[CS_B]
y = merged["label"].to_numpy()
n = len(merged)

# One hash per row under CS-B. Used as the group id everywhere below.
keys = pd.util.hash_pandas_object(sub, index=False).to_numpy()
note_rss()

# Cross-check that the hash does not collapse distinct rows: the number of
# distinct hashes must equal the number of distinct CS-B rows.
n_distinct_hash = int(pd.unique(keys).shape[0])
n_distinct_rows = int(n - sub.duplicated().sum())
note_rss()

gid, _ = pd.factorize(keys)
gsizes = np.bincount(gid)
n_groups = gsizes.shape[0]

out = {}

# ---------------------------------------------------------------- Task 3
t0 = time.time()
size1 = int((gsizes == 1).sum())
size2_10 = int(((gsizes >= 2) & (gsizes <= 10)).sum())
size_gt10 = int((gsizes > 10).sum())
rows_in_multi = int(gsizes[gsizes > 1].sum())

order = np.argsort(-gsizes)[:10]
top10 = []
lab_by_gid = pd.DataFrame({"g": gid, "y": y})
lab_counts = lab_by_gid.groupby("g")["y"].agg(["size", "sum"])
cat_by_gid = pd.DataFrame({"g": gid, "c": merged["attack_cat"].to_numpy()})
for g in order:
    sz = int(gsizes[g])
    n_att = int(lab_counts.loc[g, "sum"])
    n_nor = sz - n_att
    cats = cat_by_gid.loc[cat_by_gid["g"] == g, "c"].value_counts()
    cat_str = ", ".join(f"{k} {v:,}" for k, v in cats.items())
    top10.append({"gid": int(g), "size": sz, "attack": n_att, "normal": n_nor,
                  "attack_cat": cat_str})

task3 = {
    "n_rows": n,
    "n_groups": n_groups,
    "n_distinct_hash": n_distinct_hash,
    "n_distinct_rows": n_distinct_rows,
    "size1": size1,
    "size2_10": size2_10,
    "size_gt10": size_gt10,
    "median": float(np.median(gsizes)),
    "mean": float(gsizes.mean()),
    "max": int(gsizes.max()),
    "rows_in_multi": rows_in_multi,
    "top10": top10,
    "secs": time.time() - t0,
}
out["task3"] = task3
print("task3 done", n_groups, "groups, max", int(gsizes.max()), f"rss {note_rss():.0f}MB")

# ---------------------------------------------------------------- Task 4
t0 = time.time()
idx = np.arange(n)
sim = []
for seed in SEEDS:
    i_tr, i_te = train_test_split(idx, stratify=y, train_size=TRAIN_SIZE,
                                  test_size=TEST_SIZE, random_state=seed)
    train_keys = set(keys[i_tr].tolist())
    te_keys = keys[i_te]
    hit = np.fromiter((k in train_keys for k in te_keys.tolist()), dtype=bool,
                      count=te_keys.shape[0])
    y_te = y[i_te]
    n_hit = int(hit.sum())
    sim.append({
        "seed": seed,
        "n_test": int(i_te.shape[0]),
        "leaked": n_hit,
        "pct": pct(n_hit, i_te.shape[0]),
        "leaked_attack": int((y_te[hit] == 1).sum()),
        "leaked_normal": int((y_te[hit] == 0).sum()),
        "test_attack": int((y_te == 1).sum()),
        "test_normal": int((y_te == 0).sum()),
    })
    print(f"  seed {seed}: leaked {n_hit:,} ({pct(n_hit, i_te.shape[0]):.4f}%) "
          f"rss {note_rss():.0f}MB")
    del train_keys

pcts = [s["pct"] for s in sim]
task4 = {
    "seeds": sim,
    "mean_pct": float(np.mean(pcts)),
    "min_pct": float(np.min(pcts)),
    "max_pct": float(np.max(pcts)),
    "publisher_pct": 10.3739,   # logs/duplicates.md CS-B count 3a
    "publisher_n": 8541,
    "secs": time.time() - t0,
}
task4["ratio_mean"] = task4["mean_pct"] / task4["publisher_pct"]
out["task4"] = task4
print("task4 done", f"mean {task4['mean_pct']:.4f}%")

# ---------------------------------------------------------------- Task 5
t0 = time.time()
rng = np.random.default_rng(11)
g_size = gsizes
g_att = lab_counts["sum"].to_numpy().astype(int)
g_nor = g_size - g_att

pool_att = int((y == 1).sum())
pool_nor = int((y == 0).sum())
target_te_att = int(round(TEST_SIZE * pool_att / n))
target_te_nor = TEST_SIZE - target_te_att

perm = rng.permutation(n_groups)
to_test = np.zeros(n_groups, dtype=bool)
cur_n = cur_a = cur_o = 0
for g in perm:
    s, a, o = int(g_size[g]), int(g_att[g]), int(g_nor[g])
    if cur_n + s > TEST_SIZE:
        continue
    if cur_a + a > target_te_att or cur_o + o > target_te_nor:
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
te_nor = ach_te - te_att
tr_att = int((y[~in_test] == 1).sum())
tr_nor = ach_tr - tr_att

train_keys = set(keys[~in_test].tolist())
leak = int(sum(1 for k in keys[in_test].tolist() if k in train_keys))

task5 = {
    "seed": 11,
    "target_train": TRAIN_SIZE, "target_test": TEST_SIZE,
    "achieved_train": ach_tr, "achieved_test": ach_te,
    "dev_train_abs": ach_tr - TRAIN_SIZE,
    "dev_train_pct": pct(abs(ach_tr - TRAIN_SIZE), TRAIN_SIZE),
    "dev_test_abs": ach_te - TEST_SIZE,
    "dev_test_pct": pct(abs(ach_te - TEST_SIZE), TEST_SIZE),
    "train_attack": tr_att, "train_normal": tr_nor,
    "train_attack_pct": pct(tr_att, ach_tr),
    "test_attack": te_att, "test_normal": te_nor,
    "test_attack_pct": pct(te_att, ach_te),
    "pool_attack_pct": pct(pool_att, n),
    "target_te_att": target_te_att, "target_te_nor": target_te_nor,
    "leakage": leak,
    "n_groups_in_test": int(to_test.sum()),
    "secs": time.time() - t0,
}
out["task5"] = task5
print("task5 done", ach_tr, ach_te, "leak", leak, f"rss {note_rss():.0f}MB")

out["peak_rss_mb"] = peak[0]
out["ru_maxrss_mb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
os.makedirs("results/raw", exist_ok=True)
with open("results/raw/block1b_unsw.json", "w") as fh:
    json.dump(out, fh, indent=2)
print(f"peak rss {peak[0]:.1f} MB, ru_maxrss {out['ru_maxrss_mb']:.1f} MB")
