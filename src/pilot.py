import resource
import subprocess
import sys
import threading
import time

sys.path.insert(0, "src")

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, matthews_corrcoef

import preprocess as P

ABORT_MB = 2500.0


def rss_mb():
    with open("/proc/self/status") as fh:
        for line in fh:
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) / 1024.0
    return -1.0


class Sampler(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.peak = rss_mb()
        self.stop_flag = threading.Event()
        self.breached = False

    def run(self):
        while not self.stop_flag.is_set():
            r = rss_mb()
            if r > self.peak:
                self.peak = r
            if r > ABORT_MB:
                self.breached = True
            time.sleep(0.5)

    def finish(self):
        self.stop_flag.set()
        self.join(timeout=2)
        r = rss_mb()
        if r > self.peak:
            self.peak = r
        return self.peak


def maxrss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


free_before = subprocess.run(["free", "-m"], capture_output=True,
                             text=True).stdout.strip()
print(free_before)

avail = int(free_before.splitlines()[1].split()[6])
if avail < 3500:
    print(f"ABORT: available memory {avail} MB is under 3500 MB")
    sys.exit(1)

stages = {}
aborted = None

tr_df, te_df = P.load_unsw("data/raw/UNSW_NB15_training-set.csv",
                           "data/raw/UNSW_NB15_testing-set.csv")

s = Sampler(); s.start(); t0 = time.perf_counter()
data = P.preprocess(tr_df, te_df, dataset="unsw")
pre_wall = time.perf_counter() - t0
pre_peak = s.finish()
stages["preprocess"] = (pre_wall, pre_peak, maxrss_mb())
if s.breached:
    aborted = "preprocess"
print(f"preprocess: {pre_wall:.2f}s peak {pre_peak:.1f} MB "
      f"maxrss {maxrss_mb():.1f} MB features {data['n_features']}")

result = {}
if aborted is None:
    clf = RandomForestClassifier(n_estimators=100, max_depth=None, n_jobs=2,
                                 random_state=11)
    s = Sampler(); s.start(); t0 = time.perf_counter()
    clf.fit(data["X_train"], data["y_train"])
    fit_wall = time.perf_counter() - t0
    fit_peak = s.finish()
    stages["fit"] = (fit_wall, fit_peak, maxrss_mb())
    if s.breached:
        aborted = "fit"
    print(f"fit: {fit_wall:.2f}s peak {fit_peak:.1f} MB "
          f"maxrss {maxrss_mb():.1f} MB")

    s = Sampler(); s.start(); t0 = time.perf_counter()
    pred = clf.predict(data["X_test"])
    pred_wall = time.perf_counter() - t0
    pred_peak = s.finish()
    stages["predict"] = (pred_wall, pred_peak, maxrss_mb())
    result["accuracy"] = accuracy_score(data["y_test"], pred)
    result["mcc"] = matthews_corrcoef(data["y_test"], pred)
    print(f"predict: {pred_wall:.2f}s acc {result['accuracy']:.4f} "
          f"mcc {result['mcc']:.4f}")

free_after = subprocess.run(["free", "-m"], capture_output=True,
                            text=True).stdout.strip()

L = []
L.append("# Pilot run")
L.append("")
L.append("One model, once. RandomForestClassifier(n_estimators=100, "
         "max_depth=None, n_jobs=2, random_state=11).")
L.append("Dataset UNSW-NB15. Train on the full publisher training partition, "
         "test on the full publisher testing partition.")
L.append("Preprocessing by src/preprocess.py.")
L.append("")
L.append("## free -m taken before the run")
L.append("")
L.append("```")
L.append(free_before)
L.append("```")
L.append("")
L.append(f"Available memory before the run: {avail} MB, above the 3500 MB gate.")
L.append("")
L.append("## Stage measurements")
L.append("")
L.append("| Stage | Wall clock (s) | Peak RSS sampled every 0.5 s (MB) | "
         "ru_maxrss cross-check (MB) |")
L.append("|---|---|---|---|")
for k in ("preprocess", "fit", "predict"):
    if k in stages:
        w, p, m = stages[k]
        L.append(f"| {k} | {w:.2f} | {p:.1f} | {m:.1f} |")
L.append("")
L.append("ru_maxrss is a high water mark for the whole process, so it is "
         "monotonic across stages and is expected to be at or above the "
         "per-stage sampled peak.")
L.append("")
L.append(f"Abort threshold 2500 MB. Breached: {'yes' if aborted else 'no'}.")
if aborted:
    L.append(f"Aborted during stage: {aborted}.")
L.append("")
L.append("## Preprocessing output shape")
L.append("")
L.append(f"- Fitted feature column count: {data['n_features']}")
L.append(f"- Numeric columns passed through and scaled: {data['n_numeric']}")
L.append(f"- One-hot encoded columns: {data['n_encoded']}")
L.append(f"- Training matrix: {data['X_train'].shape}, dtype "
         f"{data['X_train'].dtype}")
L.append(f"- Testing matrix: {data['X_test'].shape}, dtype "
         f"{data['X_test'].dtype}")
L.append("")
L.append("Categories surviving the 0.1% rare-collapse threshold, computed on "
         "the training portion only:")
L.append("")
for c, vals in data["rare_kept"].items():
    L.append(f"- `{c}`: {len(vals)} kept, {vals}")
L.append("")
if result:
    L.append("## Sanity check only, not a result")
    L.append("")
    L.append(f"- Accuracy: {result['accuracy']:.4f}")
    L.append(f"- Matthews correlation coefficient: {result['mcc']:.4f}")
    L.append("")
    L.append("These two numbers exist to show the pipeline runs end to end. "
             "They are not a finding and no comparison is drawn from them.")
    L.append("")
L.append("## free -m taken after the run")
L.append("")
L.append("```")
L.append(free_after)
L.append("```")

open("logs/pilot.md", "w").write("\n".join(L) + "\n")

import json
json.dump({
    "stages": {k: {"wall_s": v[0], "peak_rss_mb": v[1], "ru_maxrss_mb": v[2]}
               for k, v in stages.items()},
    "n_features": data["n_features"],
    "accuracy": result.get("accuracy"),
    "mcc": result.get("mcc"),
    "aborted_stage": aborted,
}, open("results/raw/pilot.json", "w"), indent=2)
print("\nwrote logs/pilot.md and results/raw/pilot.json")
