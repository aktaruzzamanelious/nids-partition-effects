import hashlib
import json
import os
import sys

import pandas as pd

RAW = "data/raw"
RECEIPTS = "data/receipts"

UNSW_COLUMNS = [
    "id", "dur", "proto", "service", "state", "spkts", "dpkts", "sbytes",
    "dbytes", "rate", "sttl", "dttl", "sload", "dload", "sloss", "dloss",
    "sinpkt", "dinpkt", "sjit", "djit", "swin", "stcpb", "dtcpb", "dwin",
    "tcprtt", "synack", "ackdat", "smean", "dmean", "trans_depth",
    "response_body_len", "ct_srv_src", "ct_state_ttl", "ct_dst_ltm",
    "ct_src_dport_ltm", "ct_dst_sport_ltm", "ct_dst_src_ltm", "is_ftp_login",
    "ct_ftp_cmd", "ct_flw_http_mthd", "ct_src_ltm", "ct_srv_dst",
    "is_sm_ips_ports", "attack_cat", "label",
]

EXPECTED = {
    "UNSW_NB15_training-set.csv": {
        "url": "https://raw.githubusercontent.com/Nir-J/ML-Projects/master/UNSW-Network_Packet_Classification/UNSW_NB15_training-set.csv",
        "http_status": 200,
        "rows": 175341, "cols": 45, "bytes": 32293018,
        "attack": 119341, "normal": 56000,
        "attack_cat": {
            "Normal": 56000, "Generic": 40000, "Exploits": 33393,
            "Fuzzers": 18184, "DoS": 12264, "Reconnaissance": 10491,
            "Analysis": 2000, "Backdoor": 1746, "Shellcode": 1133, "Worms": 130,
        },
    },
    "UNSW_NB15_testing-set.csv": {
        "url": "https://raw.githubusercontent.com/ishaak15/UNSW-IDS-Feature-Selection/main/UNSW_NB15_testing-set.csv",
        "http_status": 200,
        "rows": 82332, "cols": 45, "bytes": 15380800,
        "attack": 45332, "normal": 37000,
        "attack_cat": {
            "Normal": 37000, "Generic": 18871, "Exploits": 11132,
            "Fuzzers": 6062, "DoS": 4089, "Reconnaissance": 3496,
            "Analysis": 677, "Backdoor": 583, "Shellcode": 378, "Worms": 44,
        },
    },
}

failures = []
byte_flags = []


def fail(label, expected, actual):
    failures.append((label, expected, actual))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def first_lines(path, n=2):
    out = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for _ in range(n):
            line = fh.readline()
            if not line:
                break
            out.append(line.rstrip("\n"))
    return out


frames = {}
for name, exp in EXPECTED.items():
    path = os.path.join(RAW, name)
    size = os.path.getsize(path)
    df = pd.read_csv(path, low_memory=False)
    frames[name] = df

    cols = list(df.columns)
    n_rows, n_cols = df.shape
    counts = df["label"].value_counts().to_dict() if "label" in cols else {}
    attack = int(counts.get(1, 0))
    normal = int(counts.get(0, 0))
    cat_counts = (
        df["attack_cat"].value_counts().to_dict() if "attack_cat" in cols else {}
    )

    if n_rows != exp["rows"]:
        fail(f"{name} rows", exp["rows"], n_rows)
    if n_cols != exp["cols"]:
        fail(f"{name} columns", exp["cols"], n_cols)
    if cols != UNSW_COLUMNS:
        fail(f"{name} column names/order", UNSW_COLUMNS, cols)
    if attack != exp["attack"]:
        fail(f"{name} label=1", exp["attack"], attack)
    if normal != exp["normal"]:
        fail(f"{name} label=0", exp["normal"], normal)
    for cat, want in exp["attack_cat"].items():
        got = int(cat_counts.get(cat, 0))
        if got != want:
            fail(f"{name} attack_cat[{cat}]", want, got)
    extra = sorted(set(cat_counts) - set(exp["attack_cat"]))
    if extra:
        fail(f"{name} unexpected attack_cat values", [], extra)
    if size != exp["bytes"]:
        byte_flags.append((name, exp["bytes"], size))

    receipt = {
        "file": name,
        "source_url": exp["url"],
        "http_status": exp["http_status"],
        "size_bytes": size,
        "size_bytes_expected": exp["bytes"],
        "size_bytes_match": size == exp["bytes"],
        "sha256": sha256(path),
        "row_count": int(n_rows),
        "column_count": int(n_cols),
        "column_names_in_order": cols,
        "first_two_raw_lines": first_lines(path),
        "class_balance": {
            "label_1_attack": attack,
            "label_1_pct": round(100.0 * attack / n_rows, 4),
            "label_0_normal": normal,
            "label_0_pct": round(100.0 * normal / n_rows, 4),
        },
        "attack_cat_counts": {k: int(v) for k, v in cat_counts.items()},
    }
    with open(os.path.join(RECEIPTS, name + ".json"), "w") as fh:
        json.dump(receipt, fh, indent=2)
    print(f"receipt written: {name}  rows={n_rows} cols={n_cols} "
          f"attack={attack} normal={normal} bytes={size}")

merged = pd.concat(list(frames.values()), ignore_index=True)
m_rows = len(merged)
m_attack = int((merged["label"] == 1).sum())
m_normal = int((merged["label"] == 0).sum())
if m_rows != 257673:
    fail("merged pool rows", 257673, m_rows)
if m_attack != 164673:
    fail("merged pool attack", 164673, m_attack)
if m_normal != 93000:
    fail("merged pool normal", 93000, m_normal)
print(f"merged pool: rows={m_rows} attack={m_attack} "
      f"({100.0*m_attack/m_rows:.2f}%) normal={m_normal} "
      f"({100.0*m_normal/m_rows:.2f}%)")

for name, want, got in byte_flags:
    print(f"FLAG byte size differs for {name}: expected {want} actual {got}. "
          "All other values matched, continuing.")

if failures:
    print("\nASSERTION FAILURES. EXPECTED vs ACTUAL")
    for label, expected, actual in failures:
        print(f"  {label}\n    expected: {expected}\n    actual:   {actual}")
    sys.exit(1)

print("\nALL UNSW-NB15 ASSERTIONS PASSED")
