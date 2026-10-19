"""Block 1C Task 1. NSL-KDD receipts and assertions. No model is fitted.

Column names are positional, not read from a header. The files are headerless.
Only the names the Block 1C prompt states are used: protocol_type at index 1,
service at index 2, flag at index 3, attack_name at index 41, difficulty_level
at index 42. Every other feature is named by its index as f<i>.
"""
import hashlib
import json
import os
import sys

import pandas as pd

RAW = "data/raw"
REC = "data/receipts"
FILES = {"KDDTrain+.txt": "train", "KDDTest+.txt": "test"}

EXPECTED_SHA = {
    "KDDTrain+.txt": "1b86d2f957b33082081bba410fe129b475efebcc13c9014c3f447c8271aadf95",
    "KDDTest+.txt": "fa46b0935342616aa83b7c2578db355b6a7aaabbc492248172c7a1e8b7ab8f84",
}
EXPECTED = {
    "KDDTrain+.txt": {"rows": 125973, "fields": 43,
                      "attack": 58630, "attack_pct": 46.54,
                      "normal": 67343, "normal_pct": 53.46},
    "KDDTest+.txt": {"rows": 22544, "fields": 43,
                     "attack": 12833, "attack_pct": 56.92,
                     "normal": 9711, "normal_pct": 43.08},
}
MERGED_EXPECTED = 148517

SOURCE = ("Two mirrors, github.com/jmnwong/NSL-KDD-Dataset, stated to be a "
          "Wayback Machine backup of the original nsl.cs.unb.ca site, and "
          "github.com/defcom17/NSL_KDD. The two produced byte-identical files. "
          "The original ISCX host no longer distributes the dataset.")
LICENCE = ("The NSL-KDD licence permits redistribution and mirroring provided "
           "the dataset and Tavallaee et al. are cited.")


def columns():
    names = [f"f{i}" for i in range(41)]
    names[1] = "protocol_type"
    names[2] = "service"
    names[3] = "flag"
    return names + ["attack_name", "difficulty_level"]


COLS = columns()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(label, expected, actual):
    print("\nASSERTION FAILED: " + label)
    print(f"  {'expected':<12} {'actual':<12}")
    print(f"  {str(expected):<12} {str(actual):<12}")
    sys.exit(1)


os.makedirs(REC, exist_ok=True)
frames = {}
results = {}

for fname, kind in FILES.items():
    path = os.path.join(RAW, fname)
    exp = EXPECTED[fname]

    digest = sha256(path)
    if digest != EXPECTED_SHA[fname]:
        fail(f"{fname} SHA-256", EXPECTED_SHA[fname], digest)
    print(f"{fname}: SHA-256 PASS")

    widths = set()
    with open(path) as fh:
        raw_lines = []
        n_lines = 0
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            n_lines += 1
            widths.add(line.count(",") + 1)
            if n_lines <= 2:
                raw_lines.append(line)
    if widths != {exp["fields"]}:
        fail(f"{fname} field widths", {exp["fields"]}, sorted(widths))
    print(f"{fname}: field count PASS, {exp['fields']} on every one of "
          f"{n_lines:,} rows")

    df = pd.read_csv(path, header=None, names=COLS, low_memory=False)
    if len(df) != exp["rows"]:
        fail(f"{fname} row count", exp["rows"], len(df))
    if df.shape[1] != exp["fields"]:
        fail(f"{fname} column count", exp["fields"], df.shape[1])

    df["label"] = (df["attack_name"] != "normal").astype("int8")
    n_att = int((df["label"] == 1).sum())
    n_nor = int((df["label"] == 0).sum())
    if n_att != exp["attack"]:
        fail(f"{fname} attack count", exp["attack"], n_att)
    if n_nor != exp["normal"]:
        fail(f"{fname} normal count", exp["normal"], n_nor)
    p_att = round(100.0 * n_att / len(df), 2)
    p_nor = round(100.0 * n_nor / len(df), 2)
    if p_att != exp["attack_pct"]:
        fail(f"{fname} attack percent", exp["attack_pct"], p_att)
    if p_nor != exp["normal_pct"]:
        fail(f"{fname} normal percent", exp["normal_pct"], p_nor)
    print(f"{fname}: rows {len(df):,} PASS, attack {n_att:,} ({p_att}%) PASS, "
          f"normal {n_nor:,} ({p_nor}%) PASS")

    receipt = {
        "file": fname,
        "source": SOURCE,
        "source_mirrors": ["https://github.com/jmnwong/NSL-KDD-Dataset",
                           "https://github.com/defcom17/NSL_KDD"],
        "mirrors_byte_identical": True,
        "licence": LICENCE,
        "citation_required": "Tavallaee et al., plus the dataset itself",
        "downloaded_in_block": "acceptance test prior to Block 1C",
        "size_bytes": os.path.getsize(path),
        "sha256": digest,
        "sha256_expected": EXPECTED_SHA[fname],
        "sha256_match": True,
        "row_count": len(df),
        "row_count_expected": exp["rows"],
        "field_count": exp["fields"],
        "field_count_expected": exp["fields"],
        "field_widths_observed": sorted(widths),
        "header_row": None,
        "delimiter": ",",
        "column_names_in_order": COLS,
        "column_names_note": ("Positional. The files are headerless. Only the "
                              "names stated in the Block 1C prompt are used; "
                              "every other feature is named f<index>."),
        "first_two_raw_lines": raw_lines,
        "binary_label_rule": "1 where index 41 is not the string normal, else 0",
        "class_balance": {
            "label_1_attack": n_att, "label_1_pct": p_att,
            "label_0_normal": n_nor, "label_0_pct": p_nor,
        },
        "attack_name_counts": {k: int(v) for k, v in
                               df["attack_name"].value_counts().items()},
        "difficulty_level_min": int(df["difficulty_level"].min()),
        "difficulty_level_max": int(df["difficulty_level"].max()),
        "categorical_indices": {"protocol_type": 1, "service": 2, "flag": 3},
        "assertions": {
            "sha256": "PASS", "row_count": "PASS", "field_count": "PASS",
            "binary_attack": "PASS", "binary_normal": "PASS",
        },
    }
    with open(os.path.join(REC, fname + ".json"), "w") as fh:
        json.dump(receipt, fh, indent=2)
    frames[kind] = df
    results[fname] = receipt

merged = len(frames["train"]) + len(frames["test"])
if merged != MERGED_EXPECTED:
    fail("merged pool rows", MERGED_EXPECTED, merged)
print(f"\nmerged pool {merged:,} PASS")

with open("results/raw/block1c_receipts.json", "w") as fh:
    json.dump(results, fh, indent=2)
print("receipts written to data/receipts/")
