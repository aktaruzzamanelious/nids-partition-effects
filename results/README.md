# Results

Everything in this folder was frozen on 22 September 2026. [`SHA256SUMS`](SHA256SUMS) lists the SHA-256 of all 2,660 frozen files. Its own SHA-256 is `df6b9e09d06ac30de772e9e0cf1559302206d24267ff7c96fcd4fdce848fe820`, as printed in Appendix C of the thesis. Check the files from the repository root with:

```bash
sha256sum -c --ignore-missing results/SHA256SUMS
```

## Statistics, tables and figures

| File | Content | In the thesis |
|---|---|---|
| `analysis.json` | Every statistic at full precision: input checks, rank vectors, within-arm noise floors, between-arm agreement, the bootstrap distributions of between-arm agreement, bootstrap intervals for every model and criterion, Friedman and Wilcoxon tests, top-model counts, the H1 to H4 criteria, per-model means, mean ranks, leakage and run diagnostics | Source of all tables and figures |
| `tables/T1_composition.csv` | Per dataset, arm and side: rows, attack share, duplicates under three column sets, leakage, fitted feature columns, evaluation rows | Table 4.1 |
| `tables/T1_full_splits.csv` | The same measures for each of the 110 splits | |
| `tables/T1_category_composition.csv` | Attack-category make-up of every side | Table 4.1 (c); the thesis groups the NSL-KDD attack names into four classes |
| `tables/T2_classifiers.csv` | The ten classifiers: library, version, exact settings, seed rule, score source, measured determinism, warnings | Table 3.1 |
| `tables/T3_per_model.csv` | Per model and arm: mean and SD of MCC, accuracy and macro-F1; balanced accuracy, ROC AUC, average precision, false alarm rate, detection rate and mean MCC rank | Table 4.2 and Appendix B |
| `tables/T4_rank_side_by_side.csv` | Mean MCC rank in each arm, rank change and top model | Table 4.5 |
| `tables/T5_between_arm.csv` | Rank agreement between arms on MCC: tau-b and rho with 95% intervals | Table 4.4 |
| `tables/T6_within_arm.csv` | Within-arm noise floors for three metrics; Friedman and Iman-Davenport tests | Table 4.3 |
| `tables/T7_robustness.csv` | Between-arm tau-b for MCC, accuracy and macro-F1, on all ten models and on the seven non-weak models | Table 4.6 |
| `tables/T8_distribution_shift.csv` | Attack share of each side, attack-category distance between sides, test categories missing from training | Table 4.7 |
| `tables/previews.md` | The tables as Markdown (all except `T1_full_splits`), rounded to 4 decimals for reading | |
| `figures/F2_rank_slope` | Mean MCC rank of each model in each arm | Figure 4 |
| `figures/F3_mcc_by_arm` | Mean MCC of each model in each arm, with 95% intervals | Figure 2 |
| `figures/F4_bootstrap_tau` | Bootstrap distributions of between-arm tau-b against the seed noise floor | Figure 3 |

Each figure is a vector PDF and a 1000 dpi PNG. Thesis Figure 1, the design diagram, is not a results file.

## Run records in `raw/`

| Path | Content |
|---|---|
| `raw/manifest.json` | The full run: start and end time, Python and package versions, thread settings, SHA-256 of the pipeline scripts and of the four data files |
| `raw/cells/` | 1,200 JSON records. Arms A, C-naive and C-group: `{dataset}__{arm}__{seed}__{model}.json`. Arm B: one record per fold, `{dataset}__B__r{repeat}f{fold}__{model}.json`, and one out-of-fold record per repeat, `{dataset}__B__r{repeat}oof__{model}.json`. Only the out-of-fold records are ranked |
| `raw/splits/` | 110 JSON split records, `{dataset}__{arm}__{seed}.json` or `{dataset}__B__r{repeat}f{fold}.json`: sizes, attack shares, category counts, duplicates, leakage, fitted feature columns |
| `raw/block1b_unsw.json`, `raw/block1c_nslkdd.json` | Data checks before the design was fixed: duplicate groups, leakage under random splits, a trial group-aware split |
| `raw/block1c_receipts.json`, `raw/block1c_preprocess.json` | NSL-KDD file receipts and fitted column counts |
| `raw/pilot.json` | The pilot fit used to measure time and memory |

Each fitted-cell record holds the split sizes and attack shares, every metric and the confusion counts. It also holds fit and predict times, memory use, any warnings, and the SHA-256 of the three pipeline scripts (`verify.py`, `preprocess.py` and `experiment.py`). The 100 out-of-fold records hold the metrics of each repeat of arm B, without timings.

## In the release archive

[`predictions-and-splits-v1.0.0.zip`](https://github.com/aktaruzzamanelious/nids-partition-effects/releases/tag/v1.0.0) is unzipped from the repository root. It fills two folders here:

- `raw/preds/`: 1,200 `.npz` files, one per cell record, with `y_pred` (predicted label) and `y_score` (predicted probability of attack; the decision function for the ridge classifier, M03).
- `raw/splits/`: 110 `.npz` files with `train_idx` and `test_idx` (positions in the merged pool, training file first) and `y_true`.

`src/analyze.py` needs these files. It counts them before it starts, rebuilds every confusion matrix from them, and draws the bootstrap resamples from them.

## Terms

- **Arms.** A: official split. B: repeated stratified 5-fold cross-validation on the merged pool. C-naive: stratified random split of the merged pool at the official sizes. C-group: as C-naive, with identical feature rows kept on one side.
- **Column sets for duplicates.** CS-A: all columns except the row identifier. CS-B: the features only; it defines the groups of arm C-group and every leakage count. CS-C: the features plus the binary label; the declared definition for counting duplicates.
- **Leakage.** The share of test rows whose CS-B feature row also appears on the training side of the same split.
- **Noise floor.** Kendall's tau-b between the rank vectors of the seeds inside one arm.
- **Models.** The tables use the codes; the figures use the short names. M01 to M03 are the three weak or linear models.

| Code | Short name | Class | Library |
|---|---|---|---|
| M01 | NB | GaussianNB | scikit-learn |
| M02 | LR | LogisticRegression | scikit-learn |
| M03 | Ridge | RidgeClassifier | scikit-learn |
| M04 | DT | DecisionTreeClassifier | scikit-learn |
| M05 | RF | RandomForestClassifier | scikit-learn |
| M06 | ET | ExtraTreesClassifier | scikit-learn |
| M07 | AB | AdaBoostClassifier | scikit-learn |
| M08 | HGB | HistGradientBoostingClassifier | scikit-learn |
| M09 | XGB | XGBClassifier | XGBoost |
| M10 | LGBM | LGBMClassifier | LightGBM |
