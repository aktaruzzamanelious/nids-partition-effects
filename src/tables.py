"""Block 5 tables. Builds T1 to T8 and their markdown previews.

Reads results/analysis.json, the split records in results/raw/splits/ and the model
settings in src/experiment.py. Computes nothing that feeds a hypothesis criterion.
Usage: python src/tables.py
"""
import ast
import json
import time
from collections import Counter

import numpy as np
import pandas as pd

from analyze import (ARMS, CONTRASTS, DATASETS, METRICS, MODELS, OUT_JSON, RAW,
                     split_records, top_set)

TABLES = "results/tables"
PREVIEW = f"{TABLES}/previews.md"
DIGITS = 4
LIBRARY = {**{m: "scikit-learn" for m in MODELS[:8]}, "M09": "xgboost", "M10": "lightgbm"}
PUBLISHER_TEST = {"unsw": 82332, "nslkdd": 22544}
A_NOTE = ("Protocol A has one fixed split, so seeds change model randomness only. Seven models "
          "(M01, M02, M03, M07, M08, M09, M10) gave identical predictions at every seed; only "
          "M04, M05 and M06 varied. These values are a diagnostic, not a noise floor. Friedman "
          "and Wilcoxon were not run because seven models give constant values; within-A "
          "separability comes from the bootstrap intervals on each model's metric.")
ID_NOTE = ("Chi-square is at its maximum, N(k-1) = 45, because all five repeats rank the ten "
           "models identically. The Iman-Davenport F is infinite in the limit and its p-value "
           "is 0.")
# Expected values from the Block 5B specification; any mismatch stops the table build.
EXPECT_EVAL_ROWS = {("unsw", "A"): 82332, ("unsw", "B"): 257673, ("unsw", "C-naive"): 82332,
                    ("unsw", "C-group"): 82332, ("nslkdd", "A"): 22544, ("nslkdd", "B"): 148517,
                    ("nslkdd", "C-naive"): 22544, ("nslkdd", "C-group"): 22544}
EXPECT_UNSW_A = {
    "train": {"Normal": 56000, "Generic": 40000, "Exploits": 33393, "Fuzzers": 18184,
              "DoS": 12264, "Reconnaissance": 10491, "Analysis": 2000, "Backdoor": 1746,
              "Shellcode": 1133, "Worms": 130},
    "test": {"Normal": 37000, "Generic": 18871, "Exploits": 11132, "Fuzzers": 6062,
             "DoS": 4089, "Reconnaissance": 3496, "Analysis": 677, "Backdoor": 583,
             "Shellcode": 378, "Worms": 44}}
EXPECT_NSL_A = {"train": (67343, 58630), "test": (9711, 12833)}
EXPECT_TVD_A = {"unsw": 0.08111030527818755, "nslkdd": 0.4825162836851452}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def md_table(df, digits=DIGITS):
    def fmt(v):
        if isinstance(v, (bool, np.bool_)):
            return str(v)
        if isinstance(v, (float, np.floating)):
            if np.isnan(v):
                return ""
            return f"{v:.{digits}f}"
        return str(v).replace("|", "/")
    lines = ["| " + " | ".join(map(str, df.columns)) + " |",
             "|" + "---|" * len(df.columns)]
    lines += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(lines)


def attack_share(counts_dict):
    att = {k: v for k, v in counts_dict.items() if k.strip().lower() != "normal"}
    total = sum(att.values())
    return {k: v / total for k, v in att.items()}


def stop(msg):
    raise SystemExit(f"STOP: {msg}")


def evaluation_rows(sub, ds, arm):
    # Protocol B is ranked on the pooled out of fold record, so its unit is the whole pool.
    if arm == "B":
        sums = sub.groupby("seed_or_repeat")["n_test"].sum()
        if len(sums) != 5 or sums.nunique() != 1:
            stop(f"{ds} B fold test sizes differ between repeats: {sums.to_dict()}")
        n = int(sums.iloc[0])
    else:
        if sub["n_test"].nunique() != 1:
            stop(f"{ds} {arm} test sizes differ between seeds: {sorted(sub['n_test'].unique())}")
        n = int(sub["n_test"].iloc[0])
    if n != EXPECT_EVAL_ROWS[(ds, arm)]:
        stop(f"{ds} {arm} evaluation_rows {n}, expected {EXPECT_EVAL_ROWS[(ds, arm)]}")
    return n


def full_splits_out(full):
    out = full.copy()
    is_c = out["protocol"].isin(["C-naive", "C-group"])
    dev = out["n_test"] - out["dataset"].map(PUBLISHER_TEST)
    if is_c.sum() != 40 or (dev[is_c] != 0).any():
        stop(f"achieved_size_deviation on C rows: {dev[is_c].tolist()}")
    out["achieved_size_deviation"] = dev.where(is_c).astype("Int64")
    for col in ("fold", "groups_deflected_by_capacity", "rows_deflected_by_capacity"):
        out[col] = out[col].astype("Int64")
    out["_arm"] = out["protocol"].map(ARMS.index)
    out = out.sort_values(["dataset", "_arm", "seed_or_repeat", "fold"], kind="stable")
    return out.drop(columns="_arm")


def table_t1(splits):
    full = pd.DataFrame([{k: v for k, v in s.items() if not isinstance(v, dict)}
                         for s in splits])
    full_out = full_splits_out(full)
    rows = []
    for ds in DATASETS:
        for arm in ARMS:
            sub = full[(full["dataset"] == ds) & (full["protocol"] == arm)]
            feat = sub["n_features_fitted"]
            for part in ("train", "test"):
                row = {"dataset": ds, "arm": arm, "portion": part, "n_splits": len(sub)}
                cols = {"rows": f"n_{part}", "attack_n": f"{part}_attack_n",
                        "attack_rate": f"{part}_attack_rate",
                        "dup_csa": f"dup_{part}_csa", "dup_csb": f"dup_{part}_csb",
                        "dup_csc": f"dup_{part}_csc"}
                if part == "test":
                    cols.update({"leak_csb_rows": "leak_csb_rows",
                                 "leak_csb_rate_pct": "leak_csb_rate"})
                for name, src in cols.items():
                    for fn in ("mean", "min", "max"):
                        row[f"{name}_{fn}"] = getattr(sub[src], fn)()
                row.update({"features_min": feat.min(), "features_max": feat.max(),
                            "features_mode": Counter(feat).most_common(1)[0][0]})
                if part == "test":
                    row["evaluation_rows"] = evaluation_rows(sub, ds, arm)
                if part == "test" and arm == "C-group":
                    for col in ("groups", "rows"):
                        row[f"{col}_deflected_max"] = int(
                            sub[f"{col}_deflected_by_capacity"].max())
                        if row[f"{col}_deflected_max"] != 0:
                            stop(f"{ds} C-group {col}_deflected_max is "
                                 f"{row[f'{col}_deflected_max']}, expected 0")
                rows.append(row)
    comp = pd.DataFrame(rows)
    for col in ("evaluation_rows", "groups_deflected_max", "rows_deflected_max"):
        comp[col] = comp[col].astype("Int64")
    full_out.to_csv(f"{TABLES}/T1_full_splits.csv", index=False)
    comp.to_csv(f"{TABLES}/T1_composition.csv", index=False)


def table_t1_categories(splits):
    rows = []
    for ds in DATASETS:
        for arm in ARMS:
            sub = [s for s in splits if s["dataset"] == ds and s["protocol"] == arm]
            for part in ("train", "test"):
                recs = [s[f"{part}_category_counts"] for s in sub]
                sizes = np.array([s[f"n_{part}"] for s in sub], dtype=np.float64)
                for s, rec in zip(sub, recs):
                    if sum(rec.values()) != s[f"n_{part}"]:
                        stop(f"{ds} {arm} {s['seed_or_repeat']} {s['fold']} {part}: category "
                             f"counts sum to {sum(rec.values())}, rows {s[f'n_{part}']}")
                block = []
                # Names sorted first, so equal share_mean values keep alphabetical order.
                for cat in sorted(set().union(*recs)):
                    cnt = np.array([r.get(cat, 0) for r in recs], dtype=np.int64)
                    share = cnt / sizes
                    block.append({"dataset": ds, "arm": arm, "portion": part, "category": cat,
                                  "n_splits": len(sub), "count_mean": float(cnt.mean()),
                                  "count_min": int(cnt.min()), "count_max": int(cnt.max()),
                                  "share_mean": float(share.mean()),
                                  "share_min": float(share.min()),
                                  "share_max": float(share.max())})
                rows += sorted(block, key=lambda r: -r["share_mean"])
    return pd.DataFrame(rows)


def check_categories(cat, t8):
    a = cat[cat["arm"] == "A"]
    if (a["count_min"] != a["count_max"]).any():
        stop("Protocol A category counts differ between seeds")
    stored = {(ds, p): dict(zip(g["category"], g["count_min"]))
              for (ds, p), g in a.groupby(["dataset", "portion"])}
    for part, want in EXPECT_UNSW_A.items():
        got = stored[("unsw", part)]
        if got != want:
            stop(f"UNSW-NB15 A {part}: stored names and counts {got}, expected {want}")
    for part, (n_normal, n_attack) in EXPECT_NSL_A.items():
        got = stored[("nslkdd", part)]
        other = sum(v for k, v in got.items() if k != "normal")
        if got.get("normal") != n_normal or other != n_attack:
            stop(f"NSL-KDD A {part}: normal {got.get('normal')}, others {other}; "
                 f"stored names {sorted(got)}")
    new = set(stored[("nslkdd", "test")]) - set(stored[("nslkdd", "train")])
    t8_new = t8[(t8["dataset"] == "nslkdd") & (t8["partition"] == "publisher (A)")]
    if len(new) != 17 or float(t8_new["test_categories_absent_from_train"].iloc[0]) != 17:
        stop(f"NSL-KDD A test names absent from train: {len(new)} {sorted(new)}")
    for ds, want in EXPECT_TVD_A.items():
        tr, te = attack_share(stored[(ds, "train")]), attack_share(stored[(ds, "test")])
        tvd = 0.5 * sum(abs(tr.get(c, 0.0) - te.get(c, 0.0)) for c in set(tr) | set(te))
        t8_tvd = float(t8[(t8["dataset"] == ds) & (t8["partition"] == "publisher (A)")]
                       ["tvd_attack_categories"].iloc[0])
        if abs(tvd - t8_tvd) > 1e-12 or abs(tvd - want) > 1e-12:
            stop(f"{ds} A attack-category TVD {tvd!r}, Table 8 {t8_tvd!r}, expected {want!r}")
    log("T1 category assertions 1 to 6 passed")


def model_settings():
    src = open("src/experiment.py").read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "MODEL_SPEC":
            return {k.value: " ".join(ast.get_source_segment(src, v.elts[1]).split())
                    for k, v in zip(node.value.keys, node.value.values)}
    raise RuntimeError("MODEL_SPEC not found in src/experiment.py")


def table_t2(res, versions):
    settings, rows = model_settings(), []
    for m in MODELS:
        facts = res["classifiers"][m]
        seed_rule = ("not seeded, GaussianNB takes no random_state" if m == "M01" else
                     "random_state = cell seed (A, C-naive, C-group); Protocol B repeat r "
                     "uses SEEDS_B[r] = 11, 22, 33, 44, 55")
        rows.append({"model_id": m, "class": facts["class"],
                     "library": LIBRARY[m], "version": versions[LIBRARY[m]],
                     "settings_verbatim": settings[m], "seed_application": seed_rule,
                     "score_source": facts["score_source"],
                     "deterministic_under_fixed_split_measured":
                         facts["deterministic_under_fixed_split_measured"],
                     "n_fits": facts["n_fits"], "warnings_total": facts["warnings_total"],
                     "warning_texts": facts["warning_texts"]})
    return pd.DataFrame(rows)


def table_t3(res):
    df = pd.DataFrame([res["per_model"][ds][arm][mid] for ds in DATASETS for arm in ARMS
                       for mid in MODELS])
    # Detection rate by the identity recall = 2 * balanced accuracy - 1 + false alarm rate.
    df["recall_attack_mean"] = (2 * df["balanced_accuracy_mean"] - 1
                                + df["false_alarm_rate_mean"])
    return df


def table_t4(res):
    rows = []
    for ds in DATASETS:
        mean_rank = {arm: np.array(res["mean_rank"][ds][arm]) for arm in ARMS}
        for j, mid in enumerate(MODELS):
            row = {"dataset": ds, "model_id": mid}
            row.update({f"rank_{arm}": float(mean_rank[arm][j]) for arm in ARMS})
            row["change_A_to_C-naive"] = row["rank_C-naive"] - row["rank_A"]
            row["change_A_to_C-group"] = row["rank_C-group"] - row["rank_A"]
            rows.append(row)
        top_row = {"dataset": ds, "model_id": "top ranked"}
        for arm in ARMS:
            top, tied = top_set(mean_rank[arm], 1)
            top_row[f"rank_{arm}"] = top[0] + (" (tied)" if tied else "")
        rows.append(top_row)
    return pd.DataFrame(rows)


def table_t5(res):
    rows = []
    for ds in DATASETS:
        ba, bs = res["between_arm"][ds], res["bootstrap"][ds]
        for a, b in CONTRASTS:
            key, c = f"{a} vs {b}", ba[f"{a} vs {b}"]["ten"]["mcc"]
            rows.append({"dataset": ds, "contrast": key, "n_pairs": c["tau_b"]["n_pairs"],
                         "tau_b_mean": c["tau_b"]["mean"],
                         "tau_b_ci_lo": bs["contrasts"][key]["mcc"]["tau_b_ci"][0],
                         "tau_b_ci_hi": bs["contrasts"][key]["mcc"]["tau_b_ci"][1],
                         "rho_mean": c["rho"]["mean"],
                         "rho_ci_lo": bs["contrasts"][key]["mcc"]["rho_ci"][0],
                         "rho_ci_hi": bs["contrasts"][key]["mcc"]["rho_ci"][1]})
    return pd.DataFrame(rows)


def table_t6(res):
    rows = []
    for ds in DATASETS:
        wa, fr = res["within_arm"][ds], res["friedman"][ds]
        for arm in ARMS:
            for m in METRICS:
                row = {"dataset": ds, "arm": arm, "metric": m,
                       **{f"tau_b_{s}": wa[arm][m][s] for s in ("mean", "min", "max", "p5")},
                       "n_pairs": wa[arm][m]["n_pairs"]}
                if m == "mcc" and arm == "A":
                    row["friedman_note"] = A_NOTE
                elif m == "mcc":
                    f = fr[arm]
                    if f["F_F"] == "inf":
                        row["friedman_note"] = ID_NOTE
                    row.update({"friedman_chi2": f["chi2"], "friedman_p": f["p_chi2"],
                                "iman_davenport_F": f["F_F"], "iman_davenport_p": f["p_F"]})
                rows.append(row)
    return pd.DataFrame(rows)


def table_t7(res):
    rows = []
    for ds in DATASETS:
        ba = res["between_arm"][ds]
        for a, b in CONTRASTS:
            key = f"{a} vs {b}"
            for m in METRICS:
                row = {"dataset": ds, "contrast": key, "metric": m,
                       "tau_b_mean_ten": ba[key]["ten"][m]["tau_b"]["mean"],
                       "tau_b_mean_seven": ba[key]["seven"][m]["tau_b"]["mean"]}
                if key == "C-naive vs C-group":
                    row["leak_rate_pct_Cnaive_mean"] = res["leakage"][ds]["C-naive"]["mean"]
                    row["leak_rate_pct_Cgroup_mean"] = res["leakage"][ds]["C-group"]["mean"]
                rows.append(row)
    return pd.DataFrame(rows)


def table_t8(res, splits):
    rows = []
    for ds in DATASETS:
        ba = res["between_arm"][ds]
        for arm in ("A", "C-naive", "C-group"):
            sub = [s for s in splits if s["dataset"] == ds and s["protocol"] == arm]
            tvd, new = [], []
            for s in sub:
                tr, te = attack_share(s["train_category_counts"]), attack_share(
                    s["test_category_counts"])
                tvd.append(0.5 * sum(abs(tr.get(c, 0.0) - te.get(c, 0.0))
                                     for c in set(tr) | set(te)))
                new.append(len(set(te) - set(tr)))
            tr_rate = float(np.mean([s["train_attack_rate"] for s in sub]))
            te_rate = float(np.mean([s["test_attack_rate"] for s in sub]))
            rows.append({"dataset": ds, "partition": "publisher (A)" if arm == "A" else arm,
                         "n_splits": len(sub), "train_attack_rate": tr_rate,
                         "test_attack_rate": te_rate,
                         "attack_rate_diff_pp": 100.0 * (te_rate - tr_rate),
                         "tvd_attack_categories": float(np.mean(tvd)),
                         "test_categories_absent_from_train": float(np.mean(new)),
                         "mean_tau_b_A_vs_C-naive_mcc":
                             ba["A vs C-naive"]["ten"]["mcc"]["tau_b"]["mean"]
                             if arm == "A" else None})
    return pd.DataFrame(rows)


def main():
    with open(OUT_JSON) as fh:
        res = json.load(fh)
    with open(f"{RAW}/manifest.json") as fh:
        versions = json.load(fh)["versions"]
    splits = split_records()
    t8 = table_t8(res, splits)
    cat = table_t1_categories(splits)
    check_categories(cat, t8)
    table_t1(splits)
    frames = {"T1_composition": pd.read_csv(f"{TABLES}/T1_composition.csv"),
              "T1_category_composition": cat,
              "T2_classifiers": table_t2(res, versions), "T3_per_model": table_t3(res),
              "T4_rank_side_by_side": table_t4(res), "T5_between_arm": table_t5(res),
              "T6_within_arm": table_t6(res), "T7_robustness": table_t7(res),
              "T8_distribution_shift": t8}
    parts = [f"Markdown previews. Floats rounded to {DIGITS} decimals for display; the CSV "
             f"files and results/analysis.json hold full precision."]
    for name, df in frames.items():
        if name != "T1_composition":
            df.to_csv(f"{TABLES}/{name}.csv", index=False)
        parts.append(f"## {name}\n\n{md_table(df)}")
        log(f"wrote {TABLES}/{name}.csv, {len(df)} rows")
    with open(PREVIEW, "w") as fh:
        fh.write("\n\n".join(parts) + "\n")
    log(f"wrote {PREVIEW}")


if __name__ == "__main__":
    main()
