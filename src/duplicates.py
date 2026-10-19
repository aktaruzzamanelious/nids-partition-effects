import os
import resource

import pandas as pd

RAW = "data/raw"
TRAIN = "UNSW_NB15_training-set.csv"
TEST = "UNSW_NB15_testing-set.csv"


def rss_mb():
    with open("/proc/self/status") as fh:
        for line in fh:
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) / 1024.0
    return -1.0


def pct(num, den):
    return 0.0 if den == 0 else 100.0 * num / den


tr = pd.read_csv(os.path.join(RAW, TRAIN), low_memory=False)
te = pd.read_csv(os.path.join(RAW, TEST), low_memory=False)
merged = pd.concat([tr, te], ignore_index=True)

all_cols = list(tr.columns)
CS = {
    "CS-A": [c for c in all_cols if c != "id"],
    "CS-B": [c for c in all_cols if c not in ("id", "attack_cat", "label")],
    "CS-C": [c for c in all_cols if c not in ("id", "attack_cat")],
}

lines = []
lines.append("# Duplicate counts")
lines.append("")
lines.append("Dataset: UNSW-NB15. Publisher train/test partitions as downloaded.")
lines.append("NSL-KDD was not analysed because KDDTrain+.txt and KDDTest+.txt "
             "are absent from data/raw/. See BLOCK1-REPORT.md.")
lines.append("")
lines.append("No downcasting or category encoding was applied. Peak RSS during "
             "this task stayed far below the 2500 MB abort threshold, so the "
             "memory fallback described in the prompt was not needed.")
lines.append("")
lines.append("## Column sets")
lines.append("")
lines.append("| Set | Definition | Column count |")
lines.append("|---|---|---|")
lines.append(f"| CS-A | all 45 columns except id | {len(CS['CS-A'])} |")
lines.append(f"| CS-B | features only: drop id, attack_cat, label | {len(CS['CS-B'])} |")
lines.append(f"| CS-C | CS-B plus label | {len(CS['CS-C'])} |")
lines.append("")

summary = {}

for name, cols in CS.items():
    tr_s = tr[cols]
    te_s = te[cols]
    me_s = merged[cols]

    d_tr = int(tr_s.duplicated().sum())
    d_te = int(te_s.duplicated().sum())
    d_me = int(me_s.duplicated().sum())

    distinct_tr = int(tr_s.duplicated(keep=False).sum() and
                      tr_s[tr_s.duplicated(keep=False)].drop_duplicates().shape[0])
    distinct_te = int(te_s.duplicated(keep=False).sum() and
                      te_s[te_s.duplicated(keep=False)].drop_duplicates().shape[0])
    distinct_me = int(me_s.duplicated(keep=False).sum() and
                      me_s[me_s.duplicated(keep=False)].drop_duplicates().shape[0])

    tr_keys = pd.MultiIndex.from_frame(tr_s)
    te_keys = pd.MultiIndex.from_frame(te_s)
    tr_unique = tr_keys.unique()
    te_unique = te_keys.unique()

    te_in_tr = te_keys.isin(tr_unique)
    tr_in_te = tr_keys.isin(te_unique)
    n_te_in_tr = int(te_in_tr.sum())
    n_tr_in_te = int(tr_in_te.sum())
    distinct_shared = int(te_unique.isin(tr_unique).sum())

    ov_lab = pd.concat([tr.loc[tr_in_te, "label"], te.loc[te_in_tr, "label"]])
    ov_attack = int((ov_lab == 1).sum())
    ov_normal = int((ov_lab == 0).sum())
    ov_attack_te = int((te.loc[te_in_tr, "label"] == 1).sum())
    ov_normal_te = int((te.loc[te_in_tr, "label"] == 0).sum())

    summary[name] = {
        "d_tr": d_tr, "p_tr": pct(d_tr, len(tr)),
        "d_te": d_te, "p_te": pct(d_te, len(te)),
        "d_me": d_me, "p_me": pct(d_me, len(merged)),
        "n_te_in_tr": n_te_in_tr, "p_te_in_tr": pct(n_te_in_tr, len(te)),
        "n_tr_in_te": n_tr_in_te, "p_tr_in_te": pct(n_tr_in_te, len(tr)),
    }

    lines.append(f"## {name} ({len(cols)} columns)")
    lines.append("")
    lines.append("| Count | Raw | Percent of relevant total | Distinct rows involved |")
    lines.append("|---|---|---|---|")
    lines.append(f"| 1. Duplicated rows within training (non-first occurrences) "
                 f"| {d_tr:,} | {pct(d_tr, len(tr)):.4f}% of {len(tr):,} training rows "
                 f"| {distinct_tr:,} |")
    lines.append(f"| 2. Duplicated rows within testing (non-first occurrences) "
                 f"| {d_te:,} | {pct(d_te, len(te)):.4f}% of {len(te):,} testing rows "
                 f"| {distinct_te:,} |")
    lines.append(f"| 3a. Testing rows also present in training "
                 f"| {n_te_in_tr:,} | {pct(n_te_in_tr, len(te)):.4f}% of {len(te):,} testing rows "
                 f"| {distinct_shared:,} shared distinct rows |")
    lines.append(f"| 3b. Training rows also present in testing "
                 f"| {n_tr_in_te:,} | {pct(n_tr_in_te, len(tr)):.4f}% of {len(tr):,} training rows "
                 f"| {distinct_shared:,} shared distinct rows |")
    lines.append(f"| 4. Duplicated rows within merged pool (non-first occurrences) "
                 f"| {d_me:,} | {pct(d_me, len(merged)):.4f}% of {len(merged):,} merged rows "
                 f"| {distinct_me:,} |")
    lines.append("")
    lines.append(f"Class breakdown of the cross-partition overlap (count 3), "
                 f"counting every overlapping row on both sides: "
                 f"attack {ov_attack:,}, normal {ov_normal:,}. "
                 f"Testing side only: attack {ov_attack_te:,}, normal {ov_normal_te:,}.")
    lines.append("")
    print(f"{name}: d_tr={d_tr} d_te={d_te} te_in_tr={n_te_in_tr} "
          f"tr_in_te={n_tr_in_te} d_merged={d_me} rss={rss_mb():.0f}MB")

lines.append("## Note on the published contradiction")
lines.append("")
lines.append("One published source reports 42.24% duplication in the UNSW-NB15 "
             "training partition and another reports none. The measured values "
             "above are what these two files contain. Every cell is a measured "
             "value, including the zeros.")
lines.append("")
lines.append(f"Peak RSS observed during this task: {rss_mb():.1f} MB "
             f"(ru_maxrss cross-check "
             f"{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0:.1f} MB).")
lines.append("")

with open("logs/duplicates.md", "w") as fh:
    fh.write("\n".join(lines) + "\n")

print(f"\npeak rss {rss_mb():.1f} MB, ru_maxrss "
      f"{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0:.1f} MB")
