import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ID_COLUMNS = {"unsw": ["id"], "nslkdd": []}
MULTICLASS_LABEL = {"unsw": "attack_cat", "nslkdd": "attack_name"}
DROP_EXTRA = {"unsw": [], "nslkdd": ["difficulty_level"]}
CATEGORICAL = {
    "unsw": ["proto", "service", "state"],
    "nslkdd": ["protocol_type", "service", "flag"],
}
BINARY_LABEL = "label"
RARE_THRESHOLD = 0.001
OTHER = "__other__"


def split_frame(df, dataset):
    y = df[BINARY_LABEL].to_numpy(dtype=np.int8)
    multiclass = df[MULTICLASS_LABEL[dataset]].copy()
    drop = (ID_COLUMNS[dataset] + [MULTICLASS_LABEL[dataset]]
            + DROP_EXTRA[dataset] + [BINARY_LABEL])
    X = df.drop(columns=[c for c in drop if c in df.columns])
    return X, y, multiclass


def rare_maps(X_train, dataset):
    # Thresholds come from the training portion only, then apply unchanged
    # to the test portion.
    maps = {}
    n = len(X_train)
    for col in CATEGORICAL[dataset]:
        freq = X_train[col].value_counts() / n
        maps[col] = set(freq[freq >= RARE_THRESHOLD].index)
    return maps


def apply_rare(X, maps):
    X = X.copy()
    for col, keep in maps.items():
        X[col] = X[col].where(X[col].isin(keep), OTHER).astype(str)
    return X


def preprocess(train_df, test_df, dataset="unsw"):
    """Fit on train_df only, transform both. Returns matrices, targets,
    multiclass labels, feature names and the fitted column count."""
    X_tr, y_tr, mc_tr = split_frame(train_df, dataset)
    X_te, y_te, mc_te = split_frame(test_df, dataset)

    cat = [c for c in CATEGORICAL[dataset] if c in X_tr.columns]
    num = [c for c in X_tr.columns if c not in cat]

    maps = rare_maps(X_tr, dataset)          # fit: train only
    X_tr = apply_rare(X_tr, maps)
    X_te = apply_rare(X_te, maps)            # transform only

    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False,
                            dtype=np.float32)
    cat_tr = encoder.fit_transform(X_tr[cat])   # fit: train only
    cat_te = encoder.transform(X_te[cat])       # transform only

    num_tr = X_tr[num].to_numpy(dtype=np.float32)
    num_te = X_te[num].to_numpy(dtype=np.float32)

    scaler = StandardScaler()
    num_tr = scaler.fit_transform(num_tr).astype(np.float32)  # fit: train only
    num_te = scaler.transform(num_te).astype(np.float32)      # transform only

    out_tr = np.hstack([num_tr, cat_tr]).astype(np.float32)
    out_te = np.hstack([num_te, cat_te]).astype(np.float32)

    names = list(num) + list(encoder.get_feature_names_out(cat))
    if out_tr.shape[1] != out_te.shape[1]:
        raise ValueError(f"column count differs: train {out_tr.shape[1]} "
                         f"test {out_te.shape[1]}")
    if len(names) != out_tr.shape[1]:
        raise ValueError(f"name count {len(names)} != matrix columns "
                         f"{out_tr.shape[1]}")

    return {
        "X_train": out_tr, "X_test": out_te,
        "y_train": y_tr, "y_test": y_te,
        "multiclass_train": mc_tr, "multiclass_test": mc_te,
        "feature_names": names, "n_features": out_tr.shape[1],
        "n_numeric": len(num), "n_encoded": cat_tr.shape[1],
        "rare_kept": {c: sorted(v) for c, v in maps.items()},
    }


def load_unsw(train_path, test_path):
    return (pd.read_csv(train_path, low_memory=False),
            pd.read_csv(test_path, low_memory=False))


def nslkdd_columns():
    """The NSL-KDD files are headerless and comma separated with 43 fields. These
    names were validated against KDDTrain+.txt itself on 2026-09-05 by the seven
    checks of decision P10, not taken from a published source, because two
    published sources disagree about the position of flag."""
    return """
duration protocol_type service flag src_bytes dst_bytes land wrong_fragment urgent hot
num_failed_logins logged_in num_compromised root_shell su_attempted num_root
num_file_creations num_shells num_access_files num_outbound_cmds is_host_login
is_guest_login count srv_count serror_rate srv_serror_rate rerror_rate srv_rerror_rate
same_srv_rate diff_srv_rate srv_diff_host_rate dst_host_count dst_host_srv_count
dst_host_same_srv_rate dst_host_diff_srv_rate dst_host_same_src_port_rate
dst_host_srv_diff_host_rate dst_host_serror_rate dst_host_srv_serror_rate
dst_host_rerror_rate dst_host_srv_rerror_rate attack_name difficulty_level""".split()


NSLKDD_COLUMNS = nslkdd_columns()


def load_nslkdd(train_path, test_path):
    """Read both partitions and derive the binary label. difficulty_level and
    attack_name are kept on the frame here; split_frame drops difficulty_level
    and returns attack_name separately as the multiclass label."""
    frames = []
    for path in (train_path, test_path):
        df = pd.read_csv(path, header=None, names=NSLKDD_COLUMNS,
                         low_memory=False)
        if df.shape[1] != 43:
            raise ValueError(f"{path}: expected 43 fields, got {df.shape[1]}")
        df[BINARY_LABEL] = (df["attack_name"] != "normal").astype(np.int8)
        frames.append(df)
    return frames[0], frames[1]
