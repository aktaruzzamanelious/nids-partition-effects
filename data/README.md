# Data

The study uses the official training and test files of two public benchmarks, UNSW-NB15 and NSL-KDD. The files are not in this repository. Download them with the commands below, then check them against the frozen SHA-256 values.

## The four files

| File | What it is | Rows | Bytes | SHA-256 |
|---|---|---|---|---|
| `UNSW_NB15_training-set.csv` | UNSW-NB15 official training file | 175,341 | 32,293,018 | `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa` |
| `UNSW_NB15_testing-set.csv` | UNSW-NB15 official test file | 82,332 | 15,380,800 | `734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559` |
| `KDDTrain+.txt` | NSL-KDD official training file | 125,973 | 19,109,424 | `1b86d2f957b33082081bba410fe129b475efebcc13c9014c3f447c8271aadf95` |
| `KDDTest+.txt` | NSL-KDD official test file | 22,544 | 3,441,513 | `fa46b0935342616aa83b7c2578db355b6a7aaabbc492248172c7a1e8b7ab8f84` |

## Download and check

Run from the repository root:

```bash
mkdir -p data/raw
curl -L -o data/raw/UNSW_NB15_training-set.csv "https://raw.githubusercontent.com/Nir-J/ML-Projects/master/UNSW-Network_Packet_Classification/UNSW_NB15_training-set.csv"
curl -L -o data/raw/UNSW_NB15_testing-set.csv "https://raw.githubusercontent.com/ishaak15/UNSW-IDS-Feature-Selection/main/UNSW_NB15_testing-set.csv"
curl -L -o "data/raw/KDDTrain+.txt" "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt"
curl -L -o "data/raw/KDDTest+.txt" "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt"
sha256sum -c --ignore-missing results/SHA256SUMS | grep data/raw
```

All four lines must end in `OK`. These links were checked on 19 October 2026, and all four downloads matched the frozen hashes.

**Why these links.** They are public copies (mirrors) on GitHub, not the original hosts. The official UNSW-NB15 download host could not be reached from the server used for the study. The NSL-KDD page of the Canadian Institute for Cybersecurity says the dataset is no longer available there. A second NSL-KDD mirror, [jmnwong/NSL-KDD-Dataset](https://github.com/jmnwong/NSL-KDD-Dataset), gives byte-identical files.

**Why the copies can be trusted.** A matching hash only shows that a file arrived as it was published. It does not show that the content is right. So the study accepted each file only after checking its content:

- UNSW-NB15: exact byte size, row count, all 45 column names in order, class balance and all 20 attack-category counts (10 categories in each file). The category counts match Moustafa and Slay (2016, Table 6) cell for cell.
- NSL-KDD: 43 fields on every row, row counts, class balance, and difficulty levels from 0 to 21. The two independent mirrors gave byte-identical files.

`src/receipts.py`, `src/nslkdd_receipts.py` and `src/verify.py` repeat these checks.

## A damaged copy to avoid

Zenodo record `10.5281/zenodo.17424143` offers NSL-KDD files whose published MD5 checksums match. Its content is damaged. The test file has 42 fields instead of 43 and no difficulty level. The attack names are replaced by "Attack" and "Normal", and 306 lines have the service value "Attack4". The study rejected this copy. Its checksums only showed that the files had arrived as published. The content checks found the damage.

## File format

- **UNSW-NB15.** CSV with a header row and 45 columns: `id`, 42 features, `attack_cat` (normal or one of 9 attack categories) and `label` (1 = attack, 0 = normal).
- **NSL-KDD.** No header row. Each row has 43 comma-separated fields: 41 features, the attack name and a difficulty level. Two published sources disagree about the position of the `flag` column, so the 43 names were confirmed against the data itself by seven checks on 5 September 2026. The final pipeline uses these names (`NSL_COLUMNS` in [`src/verify.py`](../src/verify.py) and [`src/experiment.py`](../src/experiment.py)). The earlier Block 1C scripts name the columns by position. The binary label is 1 for every attack name other than `normal`.
- The row identifier, the attack category or attack name, and the difficulty level are never used as features. The task is binary, with attack as the positive class.

## Receipts

[`receipts/`](receipts/) holds one JSON receipt per file from the data checks. Each receipt records the source, byte size, SHA-256, row and column counts, column names, the first two raw lines, class balance and category counts. The NSL-KDD receipts also record the seven column-name checks. Running `src/receipts.py` or `src/nslkdd_receipts.py` again rewrites these files. The new NSL-KDD receipts will not include the column-name checks, which were added after those scripts ran.

## Licences and required citations

This repository does not redistribute either dataset.

**UNSW-NB15.** The [project page](https://research.unsw.edu.au/projects/unsw-nb15-dataset) states: "Free use of the UNSW-NB15 dataset for academic research purposes is hereby granted in perpetuity. Use for commercial purposes should be agreed by the authors." It asks every user to cite these five papers:

1. Moustafa, N., & Slay, J. (2015). UNSW-NB15: A comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set). *2015 Military Communications and Information Systems Conference (MilCIS)*, 1-6. https://doi.org/10.1109/milcis.2015.7348942
2. Moustafa, N., & Slay, J. (2016). The evaluation of network anomaly detection systems: Statistical analysis of the UNSW-NB15 data set and the comparison with the KDD99 data set. *Information Security Journal: A Global Perspective, 25*(1-3), 18-31. https://doi.org/10.1080/19393555.2015.1125974
3. Moustafa, N., Slay, J., & Creech, G. (2019). Novel geometric area analysis technique for anomaly detection using trapezoidal area estimation on large-scale networks. *IEEE Transactions on Big Data, 5*(4), 481-494. https://doi.org/10.1109/tbdata.2017.2715166
4. Moustafa, N., Creech, G., & Slay, J. (2017). Big data analytics for intrusion detection system: Statistical decision-making using finite Dirichlet mixture models. In *Data analytics and decision support for cybersecurity* (pp. 127-156). Springer. https://doi.org/10.1007/978-3-319-59439-2_5
5. Sarhan, M., Layeghy, S., Moustafa, N., & Portmann, M. (2021). NetFlow datasets for machine learning-based network intrusion detection systems. In *Big data technologies and applications* (pp. 117-135). Springer. https://doi.org/10.1007/978-3-030-72802-1_9

**NSL-KDD.** The [dataset page](https://www.unb.ca/cic/datasets/nsl.html) states that "any use or redistribution of the data must include a citation to the NSL-KDD dataset and the paper referenced below":

- Tavallaee, M., Bagheri, E., Lu, W., & Ghorbani, A. A. (2009). A detailed analysis of the KDD CUP 99 data set. *2009 IEEE Symposium on Computational Intelligence for Security and Defense Applications*, 1-6. https://doi.org/10.1109/cisda.2009.5356528
- Canadian Institute for Cybersecurity. (n.d.). *NSL-KDD dataset*. University of New Brunswick. https://www.unb.ca/cic/datasets/nsl.html
