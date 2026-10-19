"""Block 3 verification. Loads the four raw files, rebuilds the three column
set keys, and checks every count stated in the Block 3 prompt. No model is
fitted. Nothing in data/raw/ is written to. No expected value is ever adjusted
to match a file. Exits non-zero if any check fails.
"""
import os

for _lib in ("OMP", "OPENBLAS", "MKL", "NUMEXPR"):
    os.environ[f"{_lib}_NUM_THREADS"] = "2"

import hashlib
import json
import sys

import numpy as np
import pandas as pd

RAW = "data/raw"
OUT = "results/smoke/verify.json"
SEP = "\x1f"

UNSW_TRAIN = "UNSW_NB15_training-set.csv"
UNSW_TEST = "UNSW_NB15_testing-set.csv"
NSL_TRAIN = "KDDTrain+.txt"
NSL_TEST = "KDDTest+.txt"

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

# The files are headerless. These names were validated against KDDTrain+.txt itself
# on 2026-09-05 by the seven checks of decision P10 and recorded in
# data/receipts/KDDTrain+.txt.json. They were not taken from a published source,
# because two published sources disagree about the position of flag.
NSL_COLUMNS = """
duration protocol_type service flag src_bytes dst_bytes land wrong_fragment urgent hot
num_failed_logins logged_in num_compromised root_shell su_attempted num_root
num_file_creations num_shells num_access_files num_outbound_cmds is_host_login
is_guest_login count srv_count serror_rate srv_serror_rate rerror_rate srv_rerror_rate
same_srv_rate diff_srv_rate srv_diff_host_rate dst_host_count dst_host_srv_count
dst_host_same_srv_rate dst_host_diff_srv_rate dst_host_same_src_port_rate
dst_host_srv_diff_host_rate dst_host_serror_rate dst_host_srv_serror_rate
dst_host_rerror_rate dst_host_srv_rerror_rate attack_name difficulty_level""".split()

EXP_SIZE = {UNSW_TRAIN: 32293018, UNSW_TEST: 15380800}
EXP_SHA = {
    NSL_TRAIN: "1b86d2f957b33082081bba410fe129b475efebcc13c9014c3f447c8271aadf95",
    NSL_TEST: "fa46b0935342616aa83b7c2578db355b6a7aaabbc492248172c7a1e8b7ab8f84",
}
UNSW_CAT_TRAIN = {"Normal": 56000, "Generic": 40000, "Exploits": 33393,
                  "Fuzzers": 18184, "DoS": 12264, "Reconnaissance": 10491,
                  "Analysis": 2000, "Backdoor": 1746, "Shellcode": 1133,
                  "Worms": 130}
UNSW_CAT_TEST = {"Normal": 37000, "Generic": 18871, "Exploits": 11132,
                 "Fuzzers": 6062, "DoS": 4089, "Reconnaissance": 3496,
                 "Analysis": 677, "Backdoor": 583, "Shellcode": 378,
                 "Worms": 44}

CHECKS = []


def check(name, expected, actual):
    ok = expected == actual
    CHECKS.append({"check": name, "expected": expected, "actual": actual,
                   "result": "PASS" if ok else "FAIL"})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: expected {expected}, actual {actual}")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def row_keys(df, cols):
    # String join under \x1f then factorize. Not a numeric hash: a collision
    # would be invisible and would corrupt every group and leakage count.
    s = df[cols[0]].astype(str)
    for c in cols[1:]:
        s = s + SEP + df[c].astype(str)
    return pd.factorize(s)[0]

def dup_count(gid):
    return int(gid.shape[0] - np.unique(gid).shape[0])

def load_nsl(name):
    df = pd.read_csv(os.path.join(RAW, name), header=None, names=NSL_COLUMNS,
                     low_memory=False)
    df["label"] = (df["attack_name"] != "normal").astype(np.int8)
    return df

def column_sets(dataset, cols):
    if dataset == "unsw":
        csb = [c for c in cols if c not in ("id", "attack_cat", "label")]
        return {"CS-A": [c for c in cols if c != "id"], "CS-B": csb,
                "CS-C": csb + ["label"]}
    csb = [c for c in NSL_COLUMNS if c not in ("attack_name", "difficulty_level")]
    return {"CS-A": list(NSL_COLUMNS), "CS-B": csb, "CS-C": csb + ["label"]}

def dataset_block(tr, te, cs):
    merged = pd.concat([tr, te], ignore_index=True)
    n_tr, n_te = len(tr), len(te)
    y_te = merged["label"].to_numpy()[n_tr:]
    res = {"n_train": n_tr, "n_test": n_te, "n_merged": len(merged), "keys": {}}
    gids = {}
    for key, cols in cs.items():
        gid = row_keys(merged, cols)
        gids[key] = gid
        g_tr, g_te = gid[:n_tr], gid[n_tr:]
        hit = np.isin(g_te, np.unique(g_tr))
        res["keys"][key] = {
            "n_cols": len(cols), "dup_train": dup_count(g_tr),
            "dup_test": dup_count(g_te), "dup_merged": dup_count(gid),
            "dup_train_pct": 100.0 * dup_count(g_tr) / n_tr,
            "leak_rows": int(hit.sum()), "leak_pct": 100.0 * int(hit.sum()) / n_te,
            "leak_attack": int((y_te[hit] == 1).sum()),
            "leak_normal": int((y_te[hit] == 0).sum()),
        }
    sizes = np.bincount(gids["CS-B"])
    multi = int(sizes[sizes > 1].sum())
    res["groups_csb"] = {
        "n_groups": int(sizes.shape[0]), "size1": int((sizes == 1).sum()),
        "size2_10": int(((sizes >= 2) & (sizes <= 10)).sum()),
        "size_gt10": int((sizes > 10).sum()), "largest": int(sizes.max()),
        "rows_in_multi": multi, "rows_in_multi_pct": 100.0 * multi / len(merged),
    }
    return res

def main():
    print("== file receipts ==")
    receipts = {}
    for fname in (UNSW_TRAIN, UNSW_TEST, NSL_TRAIN, NSL_TEST):
        path = os.path.join(RAW, fname)
        receipts[fname] = {"bytes": os.path.getsize(path), "sha256": sha256(path)}
    for fname, exp in EXP_SIZE.items():
        check(f"{fname} size bytes", exp, receipts[fname]["bytes"])
    for fname, exp in EXP_SHA.items():
        check(f"{fname} sha256", exp, receipts[fname]["sha256"])

    print("== UNSW-NB15 ==")
    tr = pd.read_csv(os.path.join(RAW, UNSW_TRAIN), low_memory=False)
    te = pd.read_csv(os.path.join(RAW, UNSW_TEST), low_memory=False)
    for part, df, nrow, att, nor, apct in [
            ("train", tr, 175341, 119341, 56000, 68.06),
            ("test", te, 82332, 45332, 37000, 55.06)]:
        check(f"UNSW {part} column names in order", UNSW_COLUMNS, list(df.columns))
        check(f"UNSW {part} rows", nrow, len(df))
        check(f"UNSW {part} columns", 45, df.shape[1])
        check(f"UNSW {part} attack rows", att, int((df["label"] == 1).sum()))
        check(f"UNSW {part} normal rows", nor, int((df["label"] == 0).sum()))
        check(f"UNSW {part} attack pct", apct,
              round(100.0 * (df["label"] == 1).mean(), 2))
    check("UNSW merged rows", 257673, len(tr) + len(te))
    check("UNSW merged attack", 164673, int(tr["label"].sum() + te["label"].sum()))
    check("UNSW merged normal", 93000,
          int((tr["label"] == 0).sum() + (te["label"] == 0).sum()))
    check("UNSW merged attack pct", 63.91,
          round(100.0 * (tr["label"].sum() + te["label"].sum()) / 257673, 2))
    check("UNSW train attack_cat composition", UNSW_CAT_TRAIN,
          {k: int(v) for k, v in tr["attack_cat"].value_counts().items()})
    check("UNSW test attack_cat composition", UNSW_CAT_TEST,
          {k: int(v) for k, v in te["attack_cat"].value_counts().items()})

    u = dataset_block(tr, te, column_sets("unsw", list(tr.columns)))
    check("UNSW CS-A dup rate in train pct", 38.55,
          round(u["keys"]["CS-A"]["dup_train_pct"], 2))
    check("UNSW CS-B dup rate in train pct", 42.38,
          round(u["keys"]["CS-B"]["dup_train_pct"], 2))
    check("UNSW CS-C dup rate in train pct", 42.2445,
          round(u["keys"]["CS-C"]["dup_train_pct"], 4))
    check("UNSW CS-B test rows also in train", 8541, u["keys"]["CS-B"]["leak_rows"])
    check("UNSW CS-B leak pct", 10.3739, round(u["keys"]["CS-B"]["leak_pct"], 4))
    check("UNSW CS-B leaked attack rows", 7069, u["keys"]["CS-B"]["leak_attack"])
    g = u["groups_csb"]
    check("UNSW CS-B groups in merged pool", 153684, g["n_groups"])
    check("UNSW CS-B groups of size 1", 137972, g["size1"])
    check("UNSW CS-B groups of size 2 to 10", 11935, g["size2_10"])
    check("UNSW CS-B groups above size 10", 3777, g["size_gt10"])
    check("UNSW CS-B largest group", 483, g["largest"])
    check("UNSW CS-B rows in a group larger than one", 119701, g["rows_in_multi"])
    check("UNSW CS-B rows in multi pct", 46.45, round(g["rows_in_multi_pct"], 2))

    print("== NSL-KDD ==")
    ntr, nte = load_nsl(NSL_TRAIN), load_nsl(NSL_TEST)
    for part, df, nrow, att, nor, apct in [
            ("train", ntr, 125973, 58630, 67343, 46.54),
            ("test", nte, 22544, 12833, 9711, 56.92)]:
        check(f"NSL-KDD {part} rows", nrow, len(df))
        check(f"NSL-KDD {part} fields", 43, df.shape[1] - 1)
        check(f"NSL-KDD {part} attack rows", att, int(df["label"].sum()))
        check(f"NSL-KDD {part} normal rows", nor, int((df["label"] == 0).sum()))
        check(f"NSL-KDD {part} attack pct", apct, round(100.0 * df["label"].mean(), 2))
        check(f"NSL-KDD {part} difficulty_level min", 0,
              int(df["difficulty_level"].min()))
        check(f"NSL-KDD {part} difficulty_level max", 21,
              int(df["difficulty_level"].max()))
    check("NSL-KDD merged rows", 148517, len(ntr) + len(nte))

    k = dataset_block(ntr, nte, column_sets("nslkdd", NSL_COLUMNS))
    for key, (d_tr, d_te, leak, d_me) in {
            "CS-A": (0, 0, 610, 610), "CS-B": (16, 57, 664, 727),
            "CS-C": (9, 3, 617, 629)}.items():
        r = k["keys"][key]
        check(f"NSL-KDD {key} duplicates in KDDTrain+", d_tr, r["dup_train"])
        check(f"NSL-KDD {key} duplicates in KDDTest+", d_te, r["dup_test"])
        check(f"NSL-KDD {key} test rows also in training", leak, r["leak_rows"])
        check(f"NSL-KDD {key} duplicates in merged pool", d_me, r["dup_merged"])
    check("NSL-KDD CS-B overlap attack rows", 559, k["keys"]["CS-B"]["leak_attack"])
    check("NSL-KDD CS-B overlap normal rows", 105, k["keys"]["CS-B"]["leak_normal"])
    gk = k["groups_csb"]
    check("NSL-KDD CS-B groups in merged pool", 147790, gk["n_groups"])
    check("NSL-KDD CS-B maximum group size", 3, gk["largest"])
    check("NSL-KDD CS-B groups above size 10", 0, gk["size_gt10"])
    check("NSL-KDD CS-B rows in a group larger than one", 1439, gk["rows_in_multi"])
    check("NSL-KDD CS-B rows in multi pct", 0.97, round(gk["rows_in_multi_pct"], 2))

    failed = [c for c in CHECKS if c["result"] == "FAIL"]
    payload = {"receipts": receipts, "unsw": u, "nslkdd": k,
               "nslkdd_columns": NSL_COLUMNS, "checks": CHECKS,
               "n_checks": len(CHECKS), "n_failed": len(failed)}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT + ".tmp", "w") as fh:
        json.dump(payload, fh, indent=2, default=str)
    os.replace(OUT + ".tmp", OUT)

    print(f"\n{len(CHECKS)} checks, {len(failed)} failed")
    for c in failed:
        print(f"FAIL {c['check']}: expected {c['expected']}, actual {c['actual']}")
    if failed:
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
