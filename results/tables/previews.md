Markdown previews. Floats rounded to 4 decimals for display; the CSV files and results/analysis.json hold full precision.

## T1_composition

| dataset | arm | portion | n_splits | rows_mean | rows_min | rows_max | attack_n_mean | attack_n_min | attack_n_max | attack_rate_mean | attack_rate_min | attack_rate_max | dup_csa_mean | dup_csa_min | dup_csa_max | dup_csb_mean | dup_csb_min | dup_csb_max | dup_csc_mean | dup_csc_min | dup_csc_max | features_min | features_max | features_mode | leak_csb_rows_mean | leak_csb_rows_min | leak_csb_rows_max | leak_csb_rate_pct_mean | leak_csb_rate_pct_min | leak_csb_rate_pct_max | evaluation_rows | groups_deflected_max | rows_deflected_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unsw | A | train | 10 | 175341.0000 | 175341 | 175341 | 119341.0000 | 119341 | 119341 | 0.6806 | 0.6806 | 0.6806 | 67601.0000 | 67601 | 67601 | 74301.0000 | 74301 | 74301 | 74072.0000 | 74072 | 74072 | 69 | 69 | 69 |  |  |  |  |  |  |  |  |  |
| unsw | A | test | 10 | 82332.0000 | 82332 | 82332 | 45332.0000 | 45332 | 45332 | 0.5506 | 0.5506 | 0.5506 | 26387.0000 | 26387 | 26387 | 28386.0000 | 28386 | 28386 | 28380.0000 | 28380 | 28380 | 69 | 69 | 69 | 8541.0000 | 8541.0000 | 8541.0000 | 10.3739 | 10.3739 | 10.3739 | 82332.0000 |  |  |
| unsw | B | train | 25 | 206138.4000 | 206138 | 206139 | 131738.4000 | 131738 | 131739 | 0.6391 | 0.6391 | 0.6391 | 72531.4800 | 72428 | 72638 | 80359.1600 | 80268 | 80450 | 80036.4400 | 79952 | 80124 | 63 | 67 | 64 |  |  |  |  |  |  |  |  |  |
| unsw | B | test | 25 | 51534.6000 | 51534 | 51535 | 32934.6000 | 32934 | 32935 | 0.6391 | 0.6391 | 0.6391 | 11922.2400 | 11788 | 12097 | 14666.2800 | 14543 | 14797 | 14613.6800 | 14490 | 14743 | 63 | 67 | 64 | 23305.1600 | 23199.0000 | 23400.0000 | 45.2224 | 45.0169 | 45.4060 | 257673.0000 |  |  |
| unsw | C-naive | train | 10 | 175341.0000 | 175341 | 175341 | 112056.0000 | 112056 | 112056 | 0.6391 | 0.6391 | 0.6391 | 59539.1000 | 59314 | 59752 | 66593.4000 | 66367 | 66787 | 66327.6000 | 66108 | 66520 | 64 | 66 | 64 |  |  |  |  |  |  |  |  |  |
| unsw | C-naive | test | 10 | 82332.0000 | 82332 | 82332 | 52617.0000 | 52617 | 52617 | 0.6391 | 0.6391 | 0.6391 | 22639.0000 | 22506 | 22825 | 26772.5000 | 26641 | 26959 | 26668.2000 | 26535 | 26852 | 64 | 66 | 64 | 36507.7000 | 36287.0000 | 36770.0000 | 44.3421 | 44.0740 | 44.6606 | 82332.0000 |  |  |
| unsw | C-group | train | 10 | 175341.0000 | 175341 | 175341 | 112056.0000 | 112056 | 112056 | 0.6391 | 0.6391 | 0.6391 | 64521.4000 | 63137 | 66208 | 70700.0000 | 69131 | 72427 | 70415.7000 | 68830 | 72150 | 64 | 68 | 66 |  |  |  |  |  |  |  |  |  |
| unsw | C-group | test | 10 | 82332.0000 | 82332 | 82332 | 52617.0000 | 52617 | 52617 | 0.6391 | 0.6391 | 0.6391 | 30406.6000 | 28720 | 31791 | 33289.0000 | 31562 | 34858 | 33159.3000 | 31425 | 34745 | 64 | 68 | 66 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 82332.0000 | 0.0000 | 0.0000 |
| nslkdd | A | train | 10 | 125973.0000 | 125973 | 125973 | 58630.0000 | 58630 | 58630 | 0.4654 | 0.4654 | 0.4654 | 0.0000 | 0 | 0 | 16.0000 | 16 | 16 | 9.0000 | 9 | 9 | 106 | 106 | 106 |  |  |  |  |  |  |  |  |  |
| nslkdd | A | test | 10 | 22544.0000 | 22544 | 22544 | 12833.0000 | 12833 | 12833 | 0.5692 | 0.5692 | 0.5692 | 0.0000 | 0 | 0 | 57.0000 | 57 | 57 | 3.0000 | 3 | 3 | 106 | 106 | 106 | 664.0000 | 664.0000 | 664.0000 | 2.9454 | 2.9454 | 2.9454 | 22544.0000 |  |  |
| nslkdd | B | train | 25 | 118813.6000 | 118813 | 118814 | 57170.4000 | 57170 | 57171 | 0.4812 | 0.4812 | 0.4812 | 389.8000 | 370 | 416 | 466.4800 | 442 | 505 | 402.0400 | 380 | 432 | 106 | 107 | 106 |  |  |  |  |  |  |  |  |  |
| nslkdd | B | test | 25 | 29703.4000 | 29703 | 29704 | 14292.6000 | 14292 | 14293 | 0.4812 | 0.4812 | 0.4812 | 23.8000 | 16 | 32 | 28.8400 | 19 | 38 | 24.5600 | 16 | 32 | 106 | 107 | 106 | 233.2400 | 191.0000 | 260.0000 | 0.7852 | 0.6430 | 0.8753 | 148517.0000 |  |  |
| nslkdd | C-naive | train | 10 | 125973.0000 | 125973 | 125973 | 60615.0000 | 60615 | 60615 | 0.4812 | 0.4812 | 0.4812 | 437.2000 | 416 | 467 | 520.8000 | 497 | 556 | 450.9000 | 428 | 484 | 106 | 107 | 106 |  |  |  |  |  |  |  |  |  |
| nslkdd | C-naive | test | 10 | 22544.0000 | 22544 | 22544 | 10848.0000 | 10848 | 10848 | 0.4812 | 0.4812 | 0.4812 | 14.8000 | 11 | 20 | 17.9000 | 11 | 22 | 15.0000 | 11 | 20 | 106 | 107 | 106 | 188.9000 | 160.0000 | 211.0000 | 0.8379 | 0.7097 | 0.9359 | 22544.0000 |  |  |
| nslkdd | C-group | train | 10 | 125973.0000 | 125973 | 125973 | 60615.0000 | 60615 | 60615 | 0.4812 | 0.4812 | 0.4812 | 518.9000 | 507 | 536 | 616.7000 | 608 | 635 | 534.3000 | 523 | 552 | 106 | 106 | 106 |  |  |  |  |  |  |  |  |  |
| nslkdd | C-group | test | 10 | 22544.0000 | 22544 | 22544 | 10848.0000 | 10848 | 10848 | 0.4812 | 0.4812 | 0.4812 | 91.1000 | 74 | 103 | 110.3000 | 92 | 119 | 94.7000 | 77 | 106 | 106 | 106 | 106 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 22544.0000 | 0.0000 | 0.0000 |

## T1_category_composition

| dataset | arm | portion | category | n_splits | count_mean | count_min | count_max | share_mean | share_min | share_max |
|---|---|---|---|---|---|---|---|---|---|---|
| unsw | A | train | Normal | 10 | 56000.0000 | 56000 | 56000 | 0.3194 | 0.3194 | 0.3194 |
| unsw | A | train | Generic | 10 | 40000.0000 | 40000 | 40000 | 0.2281 | 0.2281 | 0.2281 |
| unsw | A | train | Exploits | 10 | 33393.0000 | 33393 | 33393 | 0.1904 | 0.1904 | 0.1904 |
| unsw | A | train | Fuzzers | 10 | 18184.0000 | 18184 | 18184 | 0.1037 | 0.1037 | 0.1037 |
| unsw | A | train | DoS | 10 | 12264.0000 | 12264 | 12264 | 0.0699 | 0.0699 | 0.0699 |
| unsw | A | train | Reconnaissance | 10 | 10491.0000 | 10491 | 10491 | 0.0598 | 0.0598 | 0.0598 |
| unsw | A | train | Analysis | 10 | 2000.0000 | 2000 | 2000 | 0.0114 | 0.0114 | 0.0114 |
| unsw | A | train | Backdoor | 10 | 1746.0000 | 1746 | 1746 | 0.0100 | 0.0100 | 0.0100 |
| unsw | A | train | Shellcode | 10 | 1133.0000 | 1133 | 1133 | 0.0065 | 0.0065 | 0.0065 |
| unsw | A | train | Worms | 10 | 130.0000 | 130 | 130 | 0.0007 | 0.0007 | 0.0007 |
| unsw | A | test | Normal | 10 | 37000.0000 | 37000 | 37000 | 0.4494 | 0.4494 | 0.4494 |
| unsw | A | test | Generic | 10 | 18871.0000 | 18871 | 18871 | 0.2292 | 0.2292 | 0.2292 |
| unsw | A | test | Exploits | 10 | 11132.0000 | 11132 | 11132 | 0.1352 | 0.1352 | 0.1352 |
| unsw | A | test | Fuzzers | 10 | 6062.0000 | 6062 | 6062 | 0.0736 | 0.0736 | 0.0736 |
| unsw | A | test | DoS | 10 | 4089.0000 | 4089 | 4089 | 0.0497 | 0.0497 | 0.0497 |
| unsw | A | test | Reconnaissance | 10 | 3496.0000 | 3496 | 3496 | 0.0425 | 0.0425 | 0.0425 |
| unsw | A | test | Analysis | 10 | 677.0000 | 677 | 677 | 0.0082 | 0.0082 | 0.0082 |
| unsw | A | test | Backdoor | 10 | 583.0000 | 583 | 583 | 0.0071 | 0.0071 | 0.0071 |
| unsw | A | test | Shellcode | 10 | 378.0000 | 378 | 378 | 0.0046 | 0.0046 | 0.0046 |
| unsw | A | test | Worms | 10 | 44.0000 | 44 | 44 | 0.0005 | 0.0005 | 0.0005 |
| unsw | B | train | Normal | 25 | 74400.0000 | 74400 | 74400 | 0.3609 | 0.3609 | 0.3609 |
| unsw | B | train | Generic | 25 | 47096.8000 | 46932 | 47261 | 0.2285 | 0.2277 | 0.2293 |
| unsw | B | train | Exploits | 25 | 35620.0000 | 35499 | 35686 | 0.1728 | 0.1722 | 0.1731 |
| unsw | B | train | Fuzzers | 25 | 19396.8000 | 19269 | 19517 | 0.0941 | 0.0935 | 0.0947 |
| unsw | B | train | DoS | 25 | 13082.4000 | 12981 | 13228 | 0.0635 | 0.0630 | 0.0642 |
| unsw | B | train | Reconnaissance | 25 | 11189.6000 | 11114 | 11261 | 0.0543 | 0.0539 | 0.0546 |
| unsw | B | train | Analysis | 25 | 2141.6000 | 2101 | 2184 | 0.0104 | 0.0102 | 0.0106 |
| unsw | B | train | Backdoor | 25 | 1863.2000 | 1827 | 1891 | 0.0090 | 0.0089 | 0.0092 |
| unsw | B | train | Shellcode | 25 | 1208.8000 | 1182 | 1243 | 0.0059 | 0.0057 | 0.0060 |
| unsw | B | train | Worms | 25 | 139.2000 | 131 | 147 | 0.0007 | 0.0006 | 0.0007 |
| unsw | B | test | Normal | 25 | 18600.0000 | 18600 | 18600 | 0.3609 | 0.3609 | 0.3609 |
| unsw | B | test | Generic | 25 | 11774.2000 | 11610 | 11939 | 0.2285 | 0.2253 | 0.2317 |
| unsw | B | test | Exploits | 25 | 8905.0000 | 8839 | 9026 | 0.1728 | 0.1715 | 0.1751 |
| unsw | B | test | Fuzzers | 25 | 4849.2000 | 4729 | 4977 | 0.0941 | 0.0918 | 0.0966 |
| unsw | B | test | DoS | 25 | 3270.6000 | 3125 | 3372 | 0.0635 | 0.0606 | 0.0654 |
| unsw | B | test | Reconnaissance | 25 | 2797.4000 | 2726 | 2873 | 0.0543 | 0.0529 | 0.0557 |
| unsw | B | test | Analysis | 25 | 535.4000 | 493 | 576 | 0.0104 | 0.0096 | 0.0112 |
| unsw | B | test | Backdoor | 25 | 465.8000 | 438 | 502 | 0.0090 | 0.0085 | 0.0097 |
| unsw | B | test | Shellcode | 25 | 302.2000 | 268 | 329 | 0.0059 | 0.0052 | 0.0064 |
| unsw | B | test | Worms | 25 | 34.8000 | 27 | 43 | 0.0007 | 0.0005 | 0.0008 |
| unsw | C-naive | train | Normal | 10 | 63285.0000 | 63285 | 63285 | 0.3609 | 0.3609 | 0.3609 |
| unsw | C-naive | train | Generic | 10 | 40071.9000 | 39983 | 40147 | 0.2285 | 0.2280 | 0.2290 |
| unsw | C-naive | train | Exploits | 10 | 30264.2000 | 30171 | 30417 | 0.1726 | 0.1721 | 0.1735 |
| unsw | C-naive | train | Fuzzers | 10 | 16491.7000 | 16392 | 16638 | 0.0941 | 0.0935 | 0.0949 |
| unsw | C-naive | train | DoS | 10 | 11174.4000 | 11081 | 11268 | 0.0637 | 0.0632 | 0.0643 |
| unsw | C-naive | train | Reconnaissance | 10 | 9526.9000 | 9445 | 9619 | 0.0543 | 0.0539 | 0.0549 |
| unsw | C-naive | train | Analysis | 10 | 1817.8000 | 1792 | 1870 | 0.0104 | 0.0102 | 0.0107 |
| unsw | C-naive | train | Backdoor | 10 | 1573.6000 | 1547 | 1603 | 0.0090 | 0.0088 | 0.0091 |
| unsw | C-naive | train | Shellcode | 10 | 1016.1000 | 980 | 1045 | 0.0058 | 0.0056 | 0.0060 |
| unsw | C-naive | train | Worms | 10 | 119.4000 | 106 | 126 | 0.0007 | 0.0006 | 0.0007 |
| unsw | C-naive | test | Normal | 10 | 29715.0000 | 29715 | 29715 | 0.3609 | 0.3609 | 0.3609 |
| unsw | C-naive | test | Generic | 10 | 18799.1000 | 18724 | 18888 | 0.2283 | 0.2274 | 0.2294 |
| unsw | C-naive | test | Exploits | 10 | 14260.8000 | 14108 | 14354 | 0.1732 | 0.1714 | 0.1743 |
| unsw | C-naive | test | Fuzzers | 10 | 7754.3000 | 7608 | 7854 | 0.0942 | 0.0924 | 0.0954 |
| unsw | C-naive | test | DoS | 10 | 5178.6000 | 5085 | 5272 | 0.0629 | 0.0618 | 0.0640 |
| unsw | C-naive | test | Reconnaissance | 10 | 4460.1000 | 4368 | 4542 | 0.0542 | 0.0531 | 0.0552 |
| unsw | C-naive | test | Analysis | 10 | 859.2000 | 807 | 885 | 0.0104 | 0.0098 | 0.0107 |
| unsw | C-naive | test | Backdoor | 10 | 755.4000 | 726 | 782 | 0.0092 | 0.0088 | 0.0095 |
| unsw | C-naive | test | Shellcode | 10 | 494.9000 | 466 | 531 | 0.0060 | 0.0057 | 0.0064 |
| unsw | C-naive | test | Worms | 10 | 54.6000 | 48 | 68 | 0.0007 | 0.0006 | 0.0008 |
| unsw | C-group | train | Normal | 10 | 63285.0000 | 63285 | 63285 | 0.3609 | 0.3609 | 0.3609 |
| unsw | C-group | train | Generic | 10 | 40105.5000 | 38900 | 41381 | 0.2287 | 0.2219 | 0.2360 |
| unsw | C-group | train | Exploits | 10 | 30363.2000 | 29635 | 30623 | 0.1732 | 0.1690 | 0.1746 |
| unsw | C-group | train | Fuzzers | 10 | 16538.9000 | 16027 | 16956 | 0.0943 | 0.0914 | 0.0967 |
| unsw | C-group | train | DoS | 10 | 11169.2000 | 10943 | 11466 | 0.0637 | 0.0624 | 0.0654 |
| unsw | C-group | train | Reconnaissance | 10 | 9316.2000 | 8879 | 9893 | 0.0531 | 0.0506 | 0.0564 |
| unsw | C-group | train | Analysis | 10 | 1824.1000 | 1766 | 1871 | 0.0104 | 0.0101 | 0.0107 |
| unsw | C-group | train | Backdoor | 10 | 1586.3000 | 1543 | 1624 | 0.0090 | 0.0088 | 0.0093 |
| unsw | C-group | train | Shellcode | 10 | 1034.6000 | 1012 | 1094 | 0.0059 | 0.0058 | 0.0062 |
| unsw | C-group | train | Worms | 10 | 118.0000 | 106 | 129 | 0.0007 | 0.0006 | 0.0007 |
| unsw | C-group | test | Normal | 10 | 29715.0000 | 29715 | 29715 | 0.3609 | 0.3609 | 0.3609 |
| unsw | C-group | test | Generic | 10 | 18765.5000 | 17490 | 19971 | 0.2279 | 0.2124 | 0.2426 |
| unsw | C-group | test | Exploits | 10 | 14161.8000 | 13902 | 14890 | 0.1720 | 0.1689 | 0.1809 |
| unsw | C-group | test | Fuzzers | 10 | 7707.1000 | 7290 | 8219 | 0.0936 | 0.0885 | 0.0998 |
| unsw | C-group | test | DoS | 10 | 5183.8000 | 4887 | 5410 | 0.0630 | 0.0594 | 0.0657 |
| unsw | C-group | test | Reconnaissance | 10 | 4670.8000 | 4094 | 5108 | 0.0567 | 0.0497 | 0.0620 |
| unsw | C-group | test | Analysis | 10 | 852.9000 | 806 | 911 | 0.0104 | 0.0098 | 0.0111 |
| unsw | C-group | test | Backdoor | 10 | 742.7000 | 705 | 786 | 0.0090 | 0.0086 | 0.0095 |
| unsw | C-group | test | Shellcode | 10 | 476.4000 | 417 | 499 | 0.0058 | 0.0051 | 0.0061 |
| unsw | C-group | test | Worms | 10 | 56.0000 | 45 | 68 | 0.0007 | 0.0005 | 0.0008 |
| nslkdd | A | train | normal | 10 | 67343.0000 | 67343 | 67343 | 0.5346 | 0.5346 | 0.5346 |
| nslkdd | A | train | neptune | 10 | 41214.0000 | 41214 | 41214 | 0.3272 | 0.3272 | 0.3272 |
| nslkdd | A | train | satan | 10 | 3633.0000 | 3633 | 3633 | 0.0288 | 0.0288 | 0.0288 |
| nslkdd | A | train | ipsweep | 10 | 3599.0000 | 3599 | 3599 | 0.0286 | 0.0286 | 0.0286 |
| nslkdd | A | train | portsweep | 10 | 2931.0000 | 2931 | 2931 | 0.0233 | 0.0233 | 0.0233 |
| nslkdd | A | train | smurf | 10 | 2646.0000 | 2646 | 2646 | 0.0210 | 0.0210 | 0.0210 |
| nslkdd | A | train | nmap | 10 | 1493.0000 | 1493 | 1493 | 0.0119 | 0.0119 | 0.0119 |
| nslkdd | A | train | back | 10 | 956.0000 | 956 | 956 | 0.0076 | 0.0076 | 0.0076 |
| nslkdd | A | train | teardrop | 10 | 892.0000 | 892 | 892 | 0.0071 | 0.0071 | 0.0071 |
| nslkdd | A | train | warezclient | 10 | 890.0000 | 890 | 890 | 0.0071 | 0.0071 | 0.0071 |
| nslkdd | A | train | pod | 10 | 201.0000 | 201 | 201 | 0.0016 | 0.0016 | 0.0016 |
| nslkdd | A | train | guess_passwd | 10 | 53.0000 | 53 | 53 | 0.0004 | 0.0004 | 0.0004 |
| nslkdd | A | train | buffer_overflow | 10 | 30.0000 | 30 | 30 | 0.0002 | 0.0002 | 0.0002 |
| nslkdd | A | train | warezmaster | 10 | 20.0000 | 20 | 20 | 0.0002 | 0.0002 | 0.0002 |
| nslkdd | A | train | land | 10 | 18.0000 | 18 | 18 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | train | imap | 10 | 11.0000 | 11 | 11 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | train | rootkit | 10 | 10.0000 | 10 | 10 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | train | loadmodule | 10 | 9.0000 | 9 | 9 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | train | ftp_write | 10 | 8.0000 | 8 | 8 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | train | multihop | 10 | 7.0000 | 7 | 7 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | train | phf | 10 | 4.0000 | 4 | 4 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | A | train | perl | 10 | 3.0000 | 3 | 3 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | A | train | spy | 10 | 2.0000 | 2 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | A | test | normal | 10 | 9711.0000 | 9711 | 9711 | 0.4308 | 0.4308 | 0.4308 |
| nslkdd | A | test | neptune | 10 | 4657.0000 | 4657 | 4657 | 0.2066 | 0.2066 | 0.2066 |
| nslkdd | A | test | guess_passwd | 10 | 1231.0000 | 1231 | 1231 | 0.0546 | 0.0546 | 0.0546 |
| nslkdd | A | test | mscan | 10 | 996.0000 | 996 | 996 | 0.0442 | 0.0442 | 0.0442 |
| nslkdd | A | test | warezmaster | 10 | 944.0000 | 944 | 944 | 0.0419 | 0.0419 | 0.0419 |
| nslkdd | A | test | apache2 | 10 | 737.0000 | 737 | 737 | 0.0327 | 0.0327 | 0.0327 |
| nslkdd | A | test | satan | 10 | 735.0000 | 735 | 735 | 0.0326 | 0.0326 | 0.0326 |
| nslkdd | A | test | processtable | 10 | 685.0000 | 685 | 685 | 0.0304 | 0.0304 | 0.0304 |
| nslkdd | A | test | smurf | 10 | 665.0000 | 665 | 665 | 0.0295 | 0.0295 | 0.0295 |
| nslkdd | A | test | back | 10 | 359.0000 | 359 | 359 | 0.0159 | 0.0159 | 0.0159 |
| nslkdd | A | test | snmpguess | 10 | 331.0000 | 331 | 331 | 0.0147 | 0.0147 | 0.0147 |
| nslkdd | A | test | saint | 10 | 319.0000 | 319 | 319 | 0.0142 | 0.0142 | 0.0142 |
| nslkdd | A | test | mailbomb | 10 | 293.0000 | 293 | 293 | 0.0130 | 0.0130 | 0.0130 |
| nslkdd | A | test | snmpgetattack | 10 | 178.0000 | 178 | 178 | 0.0079 | 0.0079 | 0.0079 |
| nslkdd | A | test | portsweep | 10 | 157.0000 | 157 | 157 | 0.0070 | 0.0070 | 0.0070 |
| nslkdd | A | test | ipsweep | 10 | 141.0000 | 141 | 141 | 0.0063 | 0.0063 | 0.0063 |
| nslkdd | A | test | httptunnel | 10 | 133.0000 | 133 | 133 | 0.0059 | 0.0059 | 0.0059 |
| nslkdd | A | test | nmap | 10 | 73.0000 | 73 | 73 | 0.0032 | 0.0032 | 0.0032 |
| nslkdd | A | test | pod | 10 | 41.0000 | 41 | 41 | 0.0018 | 0.0018 | 0.0018 |
| nslkdd | A | test | buffer_overflow | 10 | 20.0000 | 20 | 20 | 0.0009 | 0.0009 | 0.0009 |
| nslkdd | A | test | multihop | 10 | 18.0000 | 18 | 18 | 0.0008 | 0.0008 | 0.0008 |
| nslkdd | A | test | named | 10 | 17.0000 | 17 | 17 | 0.0008 | 0.0008 | 0.0008 |
| nslkdd | A | test | ps | 10 | 15.0000 | 15 | 15 | 0.0007 | 0.0007 | 0.0007 |
| nslkdd | A | test | sendmail | 10 | 14.0000 | 14 | 14 | 0.0006 | 0.0006 | 0.0006 |
| nslkdd | A | test | rootkit | 10 | 13.0000 | 13 | 13 | 0.0006 | 0.0006 | 0.0006 |
| nslkdd | A | test | xterm | 10 | 13.0000 | 13 | 13 | 0.0006 | 0.0006 | 0.0006 |
| nslkdd | A | test | teardrop | 10 | 12.0000 | 12 | 12 | 0.0005 | 0.0005 | 0.0005 |
| nslkdd | A | test | xlock | 10 | 9.0000 | 9 | 9 | 0.0004 | 0.0004 | 0.0004 |
| nslkdd | A | test | land | 10 | 7.0000 | 7 | 7 | 0.0003 | 0.0003 | 0.0003 |
| nslkdd | A | test | xsnoop | 10 | 4.0000 | 4 | 4 | 0.0002 | 0.0002 | 0.0002 |
| nslkdd | A | test | ftp_write | 10 | 3.0000 | 3 | 3 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | test | loadmodule | 10 | 2.0000 | 2 | 2 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | test | perl | 10 | 2.0000 | 2 | 2 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | test | phf | 10 | 2.0000 | 2 | 2 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | test | sqlattack | 10 | 2.0000 | 2 | 2 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | test | udpstorm | 10 | 2.0000 | 2 | 2 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | test | worm | 10 | 2.0000 | 2 | 2 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | A | test | imap | 10 | 1.0000 | 1 | 1 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | B | train | normal | 25 | 61643.2000 | 61643 | 61644 | 0.5188 | 0.5188 | 0.5188 |
| nslkdd | B | train | neptune | 25 | 36696.8000 | 36633 | 36834 | 0.3089 | 0.3083 | 0.3100 |
| nslkdd | B | train | satan | 25 | 3494.4000 | 3451 | 3531 | 0.0294 | 0.0290 | 0.0297 |
| nslkdd | B | train | ipsweep | 25 | 2992.0000 | 2947 | 3041 | 0.0252 | 0.0248 | 0.0256 |
| nslkdd | B | train | smurf | 25 | 2648.8000 | 2594 | 2708 | 0.0223 | 0.0218 | 0.0228 |
| nslkdd | B | train | portsweep | 25 | 2470.4000 | 2439 | 2509 | 0.0208 | 0.0205 | 0.0211 |
| nslkdd | B | train | nmap | 25 | 1252.8000 | 1221 | 1301 | 0.0105 | 0.0103 | 0.0109 |
| nslkdd | B | train | back | 25 | 1052.0000 | 993 | 1086 | 0.0089 | 0.0084 | 0.0091 |
| nslkdd | B | train | guess_passwd | 25 | 1027.2000 | 1005 | 1056 | 0.0086 | 0.0085 | 0.0089 |
| nslkdd | B | train | mscan | 25 | 796.8000 | 773 | 824 | 0.0067 | 0.0065 | 0.0069 |
| nslkdd | B | train | warezmaster | 25 | 771.2000 | 752 | 804 | 0.0065 | 0.0063 | 0.0068 |
| nslkdd | B | train | teardrop | 25 | 723.2000 | 703 | 754 | 0.0061 | 0.0059 | 0.0063 |
| nslkdd | B | train | warezclient | 25 | 712.0000 | 691 | 733 | 0.0060 | 0.0058 | 0.0062 |
| nslkdd | B | train | apache2 | 25 | 589.6000 | 567 | 624 | 0.0050 | 0.0048 | 0.0053 |
| nslkdd | B | train | processtable | 25 | 548.0000 | 534 | 565 | 0.0046 | 0.0045 | 0.0048 |
| nslkdd | B | train | snmpguess | 25 | 264.8000 | 255 | 277 | 0.0022 | 0.0021 | 0.0023 |
| nslkdd | B | train | saint | 25 | 255.2000 | 242 | 271 | 0.0021 | 0.0020 | 0.0023 |
| nslkdd | B | train | mailbomb | 25 | 234.4000 | 222 | 247 | 0.0020 | 0.0019 | 0.0021 |
| nslkdd | B | train | pod | 25 | 193.6000 | 181 | 203 | 0.0016 | 0.0015 | 0.0017 |
| nslkdd | B | train | snmpgetattack | 25 | 142.4000 | 134 | 152 | 0.0012 | 0.0011 | 0.0013 |
| nslkdd | B | train | httptunnel | 25 | 106.4000 | 98 | 115 | 0.0009 | 0.0008 | 0.0010 |
| nslkdd | B | train | buffer_overflow | 25 | 40.0000 | 34 | 45 | 0.0003 | 0.0003 | 0.0004 |
| nslkdd | B | train | land | 25 | 20.0000 | 15 | 23 | 0.0002 | 0.0001 | 0.0002 |
| nslkdd | B | train | multihop | 25 | 20.0000 | 14 | 24 | 0.0002 | 0.0001 | 0.0002 |
| nslkdd | B | train | rootkit | 25 | 18.4000 | 15 | 21 | 0.0002 | 0.0001 | 0.0002 |
| nslkdd | B | train | named | 25 | 13.6000 | 11 | 16 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | B | train | ps | 25 | 12.0000 | 8 | 15 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | B | train | sendmail | 25 | 11.2000 | 10 | 14 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | B | train | xterm | 25 | 10.4000 | 8 | 13 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | B | train | imap | 25 | 9.6000 | 7 | 12 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | B | train | loadmodule | 25 | 8.8000 | 4 | 11 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | B | train | ftp_write | 25 | 8.8000 | 7 | 10 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | B | train | xlock | 25 | 7.2000 | 5 | 9 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | B | train | phf | 25 | 4.8000 | 3 | 6 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | B | train | perl | 25 | 4.0000 | 1 | 5 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | B | train | xsnoop | 25 | 3.2000 | 1 | 4 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | B | train | worm | 25 | 1.6000 | 0 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | B | train | sqlattack | 25 | 1.6000 | 1 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | B | train | spy | 25 | 1.6000 | 0 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | B | train | udpstorm | 25 | 1.6000 | 0 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | B | test | normal | 25 | 15410.8000 | 15410 | 15411 | 0.5188 | 0.5188 | 0.5188 |
| nslkdd | B | test | neptune | 25 | 9174.2000 | 9037 | 9238 | 0.3089 | 0.3042 | 0.3110 |
| nslkdd | B | test | satan | 25 | 873.6000 | 837 | 917 | 0.0294 | 0.0282 | 0.0309 |
| nslkdd | B | test | ipsweep | 25 | 748.0000 | 699 | 793 | 0.0252 | 0.0235 | 0.0267 |
| nslkdd | B | test | smurf | 25 | 662.2000 | 603 | 717 | 0.0223 | 0.0203 | 0.0241 |
| nslkdd | B | test | portsweep | 25 | 617.6000 | 579 | 649 | 0.0208 | 0.0195 | 0.0218 |
| nslkdd | B | test | nmap | 25 | 313.2000 | 265 | 345 | 0.0105 | 0.0089 | 0.0116 |
| nslkdd | B | test | back | 25 | 263.0000 | 229 | 322 | 0.0089 | 0.0077 | 0.0108 |
| nslkdd | B | test | guess_passwd | 25 | 256.8000 | 228 | 279 | 0.0086 | 0.0077 | 0.0094 |
| nslkdd | B | test | mscan | 25 | 199.2000 | 172 | 223 | 0.0067 | 0.0058 | 0.0075 |
| nslkdd | B | test | warezmaster | 25 | 192.8000 | 160 | 212 | 0.0065 | 0.0054 | 0.0071 |
| nslkdd | B | test | teardrop | 25 | 180.8000 | 150 | 201 | 0.0061 | 0.0050 | 0.0068 |
| nslkdd | B | test | warezclient | 25 | 178.0000 | 157 | 199 | 0.0060 | 0.0053 | 0.0067 |
| nslkdd | B | test | apache2 | 25 | 147.4000 | 113 | 170 | 0.0050 | 0.0038 | 0.0057 |
| nslkdd | B | test | processtable | 25 | 137.0000 | 120 | 151 | 0.0046 | 0.0040 | 0.0051 |
| nslkdd | B | test | snmpguess | 25 | 66.2000 | 54 | 76 | 0.0022 | 0.0018 | 0.0026 |
| nslkdd | B | test | saint | 25 | 63.8000 | 48 | 77 | 0.0021 | 0.0016 | 0.0026 |
| nslkdd | B | test | mailbomb | 25 | 58.6000 | 46 | 71 | 0.0020 | 0.0015 | 0.0024 |
| nslkdd | B | test | pod | 25 | 48.4000 | 39 | 61 | 0.0016 | 0.0013 | 0.0021 |
| nslkdd | B | test | snmpgetattack | 25 | 35.6000 | 26 | 44 | 0.0012 | 0.0009 | 0.0015 |
| nslkdd | B | test | httptunnel | 25 | 26.6000 | 18 | 35 | 0.0009 | 0.0006 | 0.0012 |
| nslkdd | B | test | buffer_overflow | 25 | 10.0000 | 5 | 16 | 0.0003 | 0.0002 | 0.0005 |
| nslkdd | B | test | land | 25 | 5.0000 | 2 | 10 | 0.0002 | 0.0001 | 0.0003 |
| nslkdd | B | test | multihop | 25 | 5.0000 | 1 | 11 | 0.0002 | 0.0000 | 0.0004 |
| nslkdd | B | test | rootkit | 25 | 4.6000 | 2 | 8 | 0.0002 | 0.0001 | 0.0003 |
| nslkdd | B | test | named | 25 | 3.4000 | 1 | 6 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | B | test | ps | 25 | 3.0000 | 0 | 7 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | B | test | sendmail | 25 | 2.8000 | 0 | 4 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | B | test | xterm | 25 | 2.6000 | 0 | 5 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | B | test | imap | 25 | 2.4000 | 0 | 5 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | B | test | loadmodule | 25 | 2.2000 | 0 | 7 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | B | test | ftp_write | 25 | 2.2000 | 1 | 4 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | B | test | xlock | 25 | 1.8000 | 0 | 4 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | B | test | phf | 25 | 1.2000 | 0 | 3 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | B | test | perl | 25 | 1.0000 | 0 | 4 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | B | test | xsnoop | 25 | 0.8000 | 0 | 3 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | B | test | worm | 25 | 0.4000 | 0 | 2 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | B | test | sqlattack | 25 | 0.4000 | 0 | 1 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | B | test | spy | 25 | 0.4000 | 0 | 2 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | B | test | udpstorm | 25 | 0.4000 | 0 | 2 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | C-naive | train | normal | 10 | 65358.0000 | 65358 | 65358 | 0.5188 | 0.5188 | 0.5188 |
| nslkdd | C-naive | train | neptune | 10 | 38898.9000 | 38808 | 39025 | 0.3088 | 0.3081 | 0.3098 |
| nslkdd | C-naive | train | satan | 10 | 3712.9000 | 3683 | 3771 | 0.0295 | 0.0292 | 0.0299 |
| nslkdd | C-naive | train | ipsweep | 10 | 3189.7000 | 3156 | 3208 | 0.0253 | 0.0251 | 0.0255 |
| nslkdd | C-naive | train | smurf | 10 | 2798.7000 | 2773 | 2825 | 0.0222 | 0.0220 | 0.0224 |
| nslkdd | C-naive | train | portsweep | 10 | 2608.3000 | 2579 | 2636 | 0.0207 | 0.0205 | 0.0209 |
| nslkdd | C-naive | train | nmap | 10 | 1320.1000 | 1303 | 1348 | 0.0105 | 0.0103 | 0.0107 |
| nslkdd | C-naive | train | back | 10 | 1115.4000 | 1076 | 1134 | 0.0089 | 0.0085 | 0.0090 |
| nslkdd | C-naive | train | guess_passwd | 10 | 1096.7000 | 1070 | 1126 | 0.0087 | 0.0085 | 0.0089 |
| nslkdd | C-naive | train | mscan | 10 | 847.7000 | 827 | 874 | 0.0067 | 0.0066 | 0.0069 |
| nslkdd | C-naive | train | warezmaster | 10 | 818.5000 | 803 | 842 | 0.0065 | 0.0064 | 0.0067 |
| nslkdd | C-naive | train | teardrop | 10 | 768.0000 | 755 | 783 | 0.0061 | 0.0060 | 0.0062 |
| nslkdd | C-naive | train | warezclient | 10 | 757.5000 | 738 | 769 | 0.0060 | 0.0059 | 0.0061 |
| nslkdd | C-naive | train | apache2 | 10 | 628.5000 | 611 | 643 | 0.0050 | 0.0049 | 0.0051 |
| nslkdd | C-naive | train | processtable | 10 | 580.6000 | 568 | 598 | 0.0046 | 0.0045 | 0.0047 |
| nslkdd | C-naive | train | snmpguess | 10 | 277.3000 | 267 | 284 | 0.0022 | 0.0021 | 0.0023 |
| nslkdd | C-naive | train | saint | 10 | 273.0000 | 266 | 280 | 0.0022 | 0.0021 | 0.0022 |
| nslkdd | C-naive | train | mailbomb | 10 | 246.8000 | 239 | 261 | 0.0020 | 0.0019 | 0.0021 |
| nslkdd | C-naive | train | pod | 10 | 204.8000 | 195 | 213 | 0.0016 | 0.0015 | 0.0017 |
| nslkdd | C-naive | train | snmpgetattack | 10 | 151.2000 | 145 | 159 | 0.0012 | 0.0012 | 0.0013 |
| nslkdd | C-naive | train | httptunnel | 10 | 111.2000 | 105 | 116 | 0.0009 | 0.0008 | 0.0009 |
| nslkdd | C-naive | train | buffer_overflow | 10 | 42.3000 | 38 | 47 | 0.0003 | 0.0003 | 0.0004 |
| nslkdd | C-naive | train | multihop | 10 | 21.6000 | 19 | 24 | 0.0002 | 0.0002 | 0.0002 |
| nslkdd | C-naive | train | land | 10 | 21.2000 | 19 | 25 | 0.0002 | 0.0002 | 0.0002 |
| nslkdd | C-naive | train | rootkit | 10 | 18.7000 | 17 | 22 | 0.0001 | 0.0001 | 0.0002 |
| nslkdd | C-naive | train | named | 10 | 14.6000 | 12 | 17 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-naive | train | ps | 10 | 12.8000 | 11 | 14 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-naive | train | sendmail | 10 | 11.5000 | 9 | 13 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-naive | train | xterm | 10 | 10.7000 | 9 | 13 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-naive | train | imap | 10 | 9.8000 | 9 | 12 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-naive | train | loadmodule | 10 | 9.6000 | 8 | 11 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-naive | train | ftp_write | 10 | 9.5000 | 9 | 10 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-naive | train | xlock | 10 | 7.7000 | 5 | 9 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | C-naive | train | phf | 10 | 5.5000 | 5 | 6 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-naive | train | perl | 10 | 4.3000 | 3 | 5 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-naive | train | xsnoop | 10 | 3.3000 | 3 | 4 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-naive | train | sqlattack | 10 | 1.7000 | 1 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-naive | train | spy | 10 | 1.5000 | 1 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-naive | train | worm | 10 | 1.5000 | 0 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-naive | train | udpstorm | 10 | 1.4000 | 0 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-naive | test | normal | 10 | 11696.0000 | 11696 | 11696 | 0.5188 | 0.5188 | 0.5188 |
| nslkdd | C-naive | test | neptune | 10 | 6972.1000 | 6846 | 7063 | 0.3093 | 0.3037 | 0.3133 |
| nslkdd | C-naive | test | satan | 10 | 655.1000 | 597 | 685 | 0.0291 | 0.0265 | 0.0304 |
| nslkdd | C-naive | test | ipsweep | 10 | 550.3000 | 532 | 584 | 0.0244 | 0.0236 | 0.0259 |
| nslkdd | C-naive | test | smurf | 10 | 512.3000 | 486 | 538 | 0.0227 | 0.0216 | 0.0239 |
| nslkdd | C-naive | test | portsweep | 10 | 479.7000 | 452 | 509 | 0.0213 | 0.0200 | 0.0226 |
| nslkdd | C-naive | test | nmap | 10 | 245.9000 | 218 | 263 | 0.0109 | 0.0097 | 0.0117 |
| nslkdd | C-naive | test | back | 10 | 199.6000 | 181 | 239 | 0.0089 | 0.0080 | 0.0106 |
| nslkdd | C-naive | test | guess_passwd | 10 | 187.3000 | 158 | 214 | 0.0083 | 0.0070 | 0.0095 |
| nslkdd | C-naive | test | mscan | 10 | 148.3000 | 122 | 169 | 0.0066 | 0.0054 | 0.0075 |
| nslkdd | C-naive | test | warezmaster | 10 | 145.5000 | 122 | 161 | 0.0065 | 0.0054 | 0.0071 |
| nslkdd | C-naive | test | teardrop | 10 | 136.0000 | 121 | 149 | 0.0060 | 0.0054 | 0.0066 |
| nslkdd | C-naive | test | warezclient | 10 | 132.5000 | 121 | 152 | 0.0059 | 0.0054 | 0.0067 |
| nslkdd | C-naive | test | apache2 | 10 | 108.5000 | 94 | 126 | 0.0048 | 0.0042 | 0.0056 |
| nslkdd | C-naive | test | processtable | 10 | 104.4000 | 87 | 117 | 0.0046 | 0.0039 | 0.0052 |
| nslkdd | C-naive | test | snmpguess | 10 | 53.7000 | 47 | 64 | 0.0024 | 0.0021 | 0.0028 |
| nslkdd | C-naive | test | mailbomb | 10 | 46.2000 | 32 | 54 | 0.0020 | 0.0014 | 0.0024 |
| nslkdd | C-naive | test | saint | 10 | 46.0000 | 39 | 53 | 0.0020 | 0.0017 | 0.0024 |
| nslkdd | C-naive | test | pod | 10 | 37.2000 | 29 | 47 | 0.0017 | 0.0013 | 0.0021 |
| nslkdd | C-naive | test | snmpgetattack | 10 | 26.8000 | 19 | 33 | 0.0012 | 0.0008 | 0.0015 |
| nslkdd | C-naive | test | httptunnel | 10 | 21.8000 | 17 | 28 | 0.0010 | 0.0008 | 0.0012 |
| nslkdd | C-naive | test | buffer_overflow | 10 | 7.7000 | 3 | 12 | 0.0003 | 0.0001 | 0.0005 |
| nslkdd | C-naive | test | rootkit | 10 | 4.3000 | 1 | 6 | 0.0002 | 0.0000 | 0.0003 |
| nslkdd | C-naive | test | land | 10 | 3.8000 | 0 | 6 | 0.0002 | 0.0000 | 0.0003 |
| nslkdd | C-naive | test | multihop | 10 | 3.4000 | 1 | 6 | 0.0002 | 0.0000 | 0.0003 |
| nslkdd | C-naive | test | sendmail | 10 | 2.5000 | 1 | 5 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-naive | test | named | 10 | 2.4000 | 0 | 5 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-naive | test | xterm | 10 | 2.3000 | 0 | 4 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-naive | test | imap | 10 | 2.2000 | 0 | 3 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | C-naive | test | ps | 10 | 2.2000 | 1 | 4 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-naive | test | ftp_write | 10 | 1.5000 | 1 | 2 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | C-naive | test | loadmodule | 10 | 1.4000 | 0 | 3 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | C-naive | test | xlock | 10 | 1.3000 | 0 | 4 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-naive | test | perl | 10 | 0.7000 | 0 | 2 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | C-naive | test | xsnoop | 10 | 0.7000 | 0 | 1 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-naive | test | udpstorm | 10 | 0.6000 | 0 | 2 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | C-naive | test | phf | 10 | 0.5000 | 0 | 1 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-naive | test | spy | 10 | 0.5000 | 0 | 1 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-naive | test | worm | 10 | 0.5000 | 0 | 2 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | C-naive | test | sqlattack | 10 | 0.3000 | 0 | 1 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | train | normal | 10 | 65358.0000 | 65358 | 65358 | 0.5188 | 0.5188 | 0.5188 |
| nslkdd | C-group | train | neptune | 10 | 38911.4000 | 38840 | 38950 | 0.3089 | 0.3083 | 0.3092 |
| nslkdd | C-group | train | satan | 10 | 3694.1000 | 3659 | 3720 | 0.0293 | 0.0290 | 0.0295 |
| nslkdd | C-group | train | ipsweep | 10 | 3175.4000 | 3149 | 3204 | 0.0252 | 0.0250 | 0.0254 |
| nslkdd | C-group | train | smurf | 10 | 2814.5000 | 2788 | 2837 | 0.0223 | 0.0221 | 0.0225 |
| nslkdd | C-group | train | portsweep | 10 | 2618.0000 | 2598 | 2648 | 0.0208 | 0.0206 | 0.0210 |
| nslkdd | C-group | train | nmap | 10 | 1324.6000 | 1304 | 1346 | 0.0105 | 0.0104 | 0.0107 |
| nslkdd | C-group | train | back | 10 | 1117.7000 | 1093 | 1134 | 0.0089 | 0.0087 | 0.0090 |
| nslkdd | C-group | train | guess_passwd | 10 | 1086.4000 | 1063 | 1105 | 0.0086 | 0.0084 | 0.0088 |
| nslkdd | C-group | train | mscan | 10 | 841.4000 | 827 | 856 | 0.0067 | 0.0066 | 0.0068 |
| nslkdd | C-group | train | warezmaster | 10 | 816.8000 | 805 | 832 | 0.0065 | 0.0064 | 0.0066 |
| nslkdd | C-group | train | teardrop | 10 | 767.8000 | 748 | 786 | 0.0061 | 0.0059 | 0.0062 |
| nslkdd | C-group | train | warezclient | 10 | 763.5000 | 749 | 778 | 0.0061 | 0.0059 | 0.0062 |
| nslkdd | C-group | train | apache2 | 10 | 627.1000 | 614 | 647 | 0.0050 | 0.0049 | 0.0051 |
| nslkdd | C-group | train | processtable | 10 | 577.9000 | 566 | 586 | 0.0046 | 0.0045 | 0.0047 |
| nslkdd | C-group | train | snmpguess | 10 | 279.0000 | 268 | 284 | 0.0022 | 0.0021 | 0.0023 |
| nslkdd | C-group | train | saint | 10 | 272.2000 | 264 | 285 | 0.0022 | 0.0021 | 0.0023 |
| nslkdd | C-group | train | mailbomb | 10 | 249.7000 | 241 | 260 | 0.0020 | 0.0019 | 0.0021 |
| nslkdd | C-group | train | pod | 10 | 204.9000 | 193 | 220 | 0.0016 | 0.0015 | 0.0017 |
| nslkdd | C-group | train | snmpgetattack | 10 | 150.3000 | 141 | 156 | 0.0012 | 0.0011 | 0.0012 |
| nslkdd | C-group | train | httptunnel | 10 | 112.5000 | 108 | 116 | 0.0009 | 0.0009 | 0.0009 |
| nslkdd | C-group | train | buffer_overflow | 10 | 43.3000 | 40 | 48 | 0.0003 | 0.0003 | 0.0004 |
| nslkdd | C-group | train | multihop | 10 | 21.0000 | 16 | 24 | 0.0002 | 0.0001 | 0.0002 |
| nslkdd | C-group | train | land | 10 | 20.7000 | 18 | 23 | 0.0002 | 0.0001 | 0.0002 |
| nslkdd | C-group | train | rootkit | 10 | 19.6000 | 17 | 23 | 0.0002 | 0.0001 | 0.0002 |
| nslkdd | C-group | train | named | 10 | 14.4000 | 12 | 15 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-group | train | ps | 10 | 13.5000 | 11 | 15 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-group | train | sendmail | 10 | 11.5000 | 10 | 13 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-group | train | xterm | 10 | 10.9000 | 9 | 13 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-group | train | imap | 10 | 9.8000 | 8 | 11 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-group | train | loadmodule | 10 | 9.5000 | 7 | 11 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-group | train | ftp_write | 10 | 9.4000 | 7 | 11 | 0.0001 | 0.0001 | 0.0001 |
| nslkdd | C-group | train | xlock | 10 | 6.7000 | 6 | 8 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | C-group | train | phf | 10 | 4.7000 | 3 | 6 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | train | perl | 10 | 4.2000 | 3 | 5 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | train | xsnoop | 10 | 3.5000 | 3 | 4 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | train | spy | 10 | 1.9000 | 1 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | train | worm | 10 | 1.9000 | 1 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | train | sqlattack | 10 | 1.8000 | 1 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | train | udpstorm | 10 | 1.5000 | 0 | 2 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | test | normal | 10 | 11696.0000 | 11696 | 11696 | 0.5188 | 0.5188 | 0.5188 |
| nslkdd | C-group | test | neptune | 10 | 6959.6000 | 6921 | 7031 | 0.3087 | 0.3070 | 0.3119 |
| nslkdd | C-group | test | satan | 10 | 673.9000 | 648 | 709 | 0.0299 | 0.0287 | 0.0314 |
| nslkdd | C-group | test | ipsweep | 10 | 564.6000 | 536 | 591 | 0.0250 | 0.0238 | 0.0262 |
| nslkdd | C-group | test | smurf | 10 | 496.5000 | 474 | 523 | 0.0220 | 0.0210 | 0.0232 |
| nslkdd | C-group | test | portsweep | 10 | 470.0000 | 440 | 490 | 0.0208 | 0.0195 | 0.0217 |
| nslkdd | C-group | test | nmap | 10 | 241.4000 | 220 | 262 | 0.0107 | 0.0098 | 0.0116 |
| nslkdd | C-group | test | guess_passwd | 10 | 197.6000 | 179 | 221 | 0.0088 | 0.0079 | 0.0098 |
| nslkdd | C-group | test | back | 10 | 197.3000 | 181 | 222 | 0.0088 | 0.0080 | 0.0098 |
| nslkdd | C-group | test | mscan | 10 | 154.6000 | 140 | 169 | 0.0069 | 0.0062 | 0.0075 |
| nslkdd | C-group | test | warezmaster | 10 | 147.2000 | 132 | 159 | 0.0065 | 0.0059 | 0.0071 |
| nslkdd | C-group | test | teardrop | 10 | 136.2000 | 118 | 156 | 0.0060 | 0.0052 | 0.0069 |
| nslkdd | C-group | test | warezclient | 10 | 126.5000 | 112 | 141 | 0.0056 | 0.0050 | 0.0063 |
| nslkdd | C-group | test | apache2 | 10 | 109.9000 | 90 | 123 | 0.0049 | 0.0040 | 0.0055 |
| nslkdd | C-group | test | processtable | 10 | 107.1000 | 99 | 119 | 0.0048 | 0.0044 | 0.0053 |
| nslkdd | C-group | test | snmpguess | 10 | 52.0000 | 47 | 63 | 0.0023 | 0.0021 | 0.0028 |
| nslkdd | C-group | test | saint | 10 | 46.8000 | 34 | 55 | 0.0021 | 0.0015 | 0.0024 |
| nslkdd | C-group | test | mailbomb | 10 | 43.3000 | 33 | 52 | 0.0019 | 0.0015 | 0.0023 |
| nslkdd | C-group | test | pod | 10 | 37.1000 | 22 | 49 | 0.0016 | 0.0010 | 0.0022 |
| nslkdd | C-group | test | snmpgetattack | 10 | 27.7000 | 22 | 37 | 0.0012 | 0.0010 | 0.0016 |
| nslkdd | C-group | test | httptunnel | 10 | 20.5000 | 17 | 25 | 0.0009 | 0.0008 | 0.0011 |
| nslkdd | C-group | test | buffer_overflow | 10 | 6.7000 | 2 | 10 | 0.0003 | 0.0001 | 0.0004 |
| nslkdd | C-group | test | land | 10 | 4.3000 | 2 | 7 | 0.0002 | 0.0001 | 0.0003 |
| nslkdd | C-group | test | multihop | 10 | 4.0000 | 1 | 9 | 0.0002 | 0.0000 | 0.0004 |
| nslkdd | C-group | test | rootkit | 10 | 3.4000 | 0 | 6 | 0.0002 | 0.0000 | 0.0003 |
| nslkdd | C-group | test | named | 10 | 2.6000 | 2 | 5 | 0.0001 | 0.0001 | 0.0002 |
| nslkdd | C-group | test | sendmail | 10 | 2.5000 | 1 | 4 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-group | test | xlock | 10 | 2.3000 | 1 | 3 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | C-group | test | imap | 10 | 2.2000 | 1 | 4 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-group | test | xterm | 10 | 2.1000 | 0 | 4 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-group | test | ftp_write | 10 | 1.6000 | 0 | 4 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-group | test | loadmodule | 10 | 1.5000 | 0 | 4 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-group | test | ps | 10 | 1.5000 | 0 | 4 | 0.0001 | 0.0000 | 0.0002 |
| nslkdd | C-group | test | phf | 10 | 1.3000 | 0 | 3 | 0.0001 | 0.0000 | 0.0001 |
| nslkdd | C-group | test | perl | 10 | 0.8000 | 0 | 2 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | C-group | test | udpstorm | 10 | 0.5000 | 0 | 2 | 0.0000 | 0.0000 | 0.0001 |
| nslkdd | C-group | test | xsnoop | 10 | 0.5000 | 0 | 1 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | test | sqlattack | 10 | 0.2000 | 0 | 1 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | test | spy | 10 | 0.1000 | 0 | 1 | 0.0000 | 0.0000 | 0.0000 |
| nslkdd | C-group | test | worm | 10 | 0.1000 | 0 | 1 | 0.0000 | 0.0000 | 0.0000 |

## T2_classifiers

| model_id | class | library | version | settings_verbatim | seed_application | score_source | deterministic_under_fixed_split_measured | n_fits | warnings_total | warning_texts |
|---|---|---|---|---|---|---|---|---|---|---|
| M01 | GaussianNB | scikit-learn | 1.9.0 | dict(var_smoothing=1e-9) | not seeded, GaussianNB takes no random_state | predict_proba | True | 110 | 0 |  |
| M02 | LogisticRegression | scikit-learn | 1.9.0 | dict(solver="lbfgs", max_iter=500, C=1.0, n_jobs=2) | random_state = cell seed (A, C-naive, C-group); Protocol B repeat r uses SEEDS_B[r] = 11, 22, 33, 44, 55 | predict_proba | True | 110 | 110 | 'n_jobs' has no effect since 1.8 and will be removed in 1.10. You provided 'n_jobs=2', please leave it unspecified. |
| M03 | RidgeClassifier | scikit-learn | 1.9.0 | dict(alpha=1.0, solver="auto") | random_state = cell seed (A, C-naive, C-group); Protocol B repeat r uses SEEDS_B[r] = 11, 22, 33, 44, 55 | decision_function | True | 110 | 0 |  |
| M04 | DecisionTreeClassifier | scikit-learn | 1.9.0 | dict(criterion="gini", max_depth=None, min_samples_split=2) | random_state = cell seed (A, C-naive, C-group); Protocol B repeat r uses SEEDS_B[r] = 11, 22, 33, 44, 55 | predict_proba | False | 110 | 0 |  |
| M05 | RandomForestClassifier | scikit-learn | 1.9.0 | dict(n_estimators=100, max_depth=None, n_jobs=2) | random_state = cell seed (A, C-naive, C-group); Protocol B repeat r uses SEEDS_B[r] = 11, 22, 33, 44, 55 | predict_proba | False | 110 | 0 |  |
| M06 | ExtraTreesClassifier | scikit-learn | 1.9.0 | dict(n_estimators=100, max_depth=None, n_jobs=2) | random_state = cell seed (A, C-naive, C-group); Protocol B repeat r uses SEEDS_B[r] = 11, 22, 33, 44, 55 | predict_proba | False | 110 | 0 |  |
| M07 | AdaBoostClassifier | scikit-learn | 1.9.0 | dict(n_estimators=100, learning_rate=1.0) | random_state = cell seed (A, C-naive, C-group); Protocol B repeat r uses SEEDS_B[r] = 11, 22, 33, 44, 55 | predict_proba | True | 110 | 0 |  |
| M08 | HistGradientBoostingClassifier | scikit-learn | 1.9.0 | dict(max_iter=200, learning_rate=0.1, max_leaf_nodes=31, early_stopping=False) | random_state = cell seed (A, C-naive, C-group); Protocol B repeat r uses SEEDS_B[r] = 11, 22, 33, 44, 55 | predict_proba | True | 110 | 0 |  |
| M09 | XGBClassifier | xgboost | 3.4.1 | dict(tree_method="hist", n_estimators=200, max_depth=6, learning_rate=0.3, n_jobs=2, eval_metric="logloss") | random_state = cell seed (A, C-naive, C-group); Protocol B repeat r uses SEEDS_B[r] = 11, 22, 33, 44, 55 | predict_proba | True | 110 | 0 |  |
| M10 | LGBMClassifier | lightgbm | 4.7.0 | dict(n_estimators=200, num_leaves=31, learning_rate=0.1, n_jobs=2, verbose=-1) | random_state = cell seed (A, C-naive, C-group); Protocol B repeat r uses SEEDS_B[r] = 11, 22, 33, 44, 55 | predict_proba | True | 110 | 0 |  |

## T3_per_model

| dataset | arm | model_id | mcc_mean | mcc_sd | accuracy_mean | accuracy_sd | macro_f1_mean | macro_f1_sd | mcc_mean_rank | balanced_accuracy_mean | roc_auc_mean | average_precision_mean | false_alarm_rate_mean | recall_attack_mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unsw | A | M01 | 0.4754 | 0.0000 | 0.6774 | 0.0000 | 0.6633 | 0.0000 | 10.0000 | 0.7054 | 0.8711 | 0.8913 | 0.0184 | 0.4292 |
| unsw | A | M02 | 0.6372 | 0.0000 | 0.8086 | 0.0000 | 0.7945 | 0.0000 | 9.0000 | 0.7902 | 0.9551 | 0.9657 | 0.3918 | 0.9722 |
| unsw | A | M03 | 0.6518 | 0.0000 | 0.8089 | 0.0000 | 0.7914 | 0.0000 | 8.0000 | 0.7876 | 0.9526 | 0.9636 | 0.4226 | 0.9979 |
| unsw | A | M04 | 0.7338 | 0.0016 | 0.8648 | 0.0007 | 0.8598 | 0.0008 | 6.0000 | 0.8544 | 0.8569 | 0.8165 | 0.2480 | 0.9568 |
| unsw | A | M05 | 0.7564 | 0.0010 | 0.8723 | 0.0005 | 0.8663 | 0.0005 | 2.2000 | 0.8596 | 0.9786 | 0.9816 | 0.2661 | 0.9853 |
| unsw | A | M06 | 0.7450 | 0.0014 | 0.8667 | 0.0007 | 0.8602 | 0.0008 | 5.0000 | 0.8537 | 0.9731 | 0.9733 | 0.2746 | 0.9820 |
| unsw | A | M07 | 0.6715 | 0.0000 | 0.8295 | 0.0000 | 0.8197 | 0.0000 | 7.0000 | 0.8143 | 0.9616 | 0.9709 | 0.3363 | 0.9648 |
| unsw | A | M08 | 0.7558 | 0.0000 | 0.8725 | 0.0000 | 0.8666 | 0.0000 | 2.8000 | 0.8601 | 0.9843 | 0.9886 | 0.2627 | 0.9828 |
| unsw | A | M09 | 0.7544 | 0.0000 | 0.8722 | 0.0000 | 0.8665 | 0.0000 | 4.0000 | 0.8601 | 0.9825 | 0.9872 | 0.2601 | 0.9802 |
| unsw | A | M10 | 0.7623 | 0.0000 | 0.8759 | 0.0000 | 0.8704 | 0.0000 | 1.0000 | 0.8638 | 0.9849 | 0.9890 | 0.2561 | 0.9837 |
| unsw | B | M01 | 0.5235 | 0.0018 | 0.7019 | 0.0020 | 0.7019 | 0.0020 | 10.0000 | 0.7614 | 0.9060 | 0.9395 | 0.0247 | 0.5474 |
| unsw | B | M02 | 0.7880 | 0.0001 | 0.9028 | 0.0001 | 0.8907 | 0.0001 | 8.0000 | 0.8781 | 0.9756 | 0.9854 | 0.2105 | 0.9667 |
| unsw | B | M03 | 0.7701 | 0.0000 | 0.8913 | 0.0000 | 0.8731 | 0.0000 | 9.0000 | 0.8519 | 0.9682 | 0.9816 | 0.2899 | 0.9936 |
| unsw | B | M04 | 0.8655 | 0.0009 | 0.9379 | 0.0004 | 0.9327 | 0.0005 | 6.0000 | 0.9329 | 0.9350 | 0.9384 | 0.0852 | 0.9510 |
| unsw | B | M05 | 0.8943 | 0.0002 | 0.9512 | 0.0001 | 0.9472 | 0.0001 | 1.0000 | 0.9479 | 0.9920 | 0.9953 | 0.0640 | 0.9597 |
| unsw | B | M06 | 0.8905 | 0.0004 | 0.9494 | 0.0002 | 0.9452 | 0.0002 | 3.0000 | 0.9461 | 0.9899 | 0.9933 | 0.0656 | 0.9578 |
| unsw | B | M07 | 0.8186 | 0.0017 | 0.9166 | 0.0008 | 0.9093 | 0.0009 | 7.0000 | 0.9078 | 0.9797 | 0.9886 | 0.1237 | 0.9393 |
| unsw | B | M08 | 0.8856 | 0.0002 | 0.9468 | 0.0001 | 0.9427 | 0.0001 | 5.0000 | 0.9452 | 0.9915 | 0.9953 | 0.0605 | 0.9510 |
| unsw | B | M09 | 0.8923 | 0.0007 | 0.9501 | 0.0003 | 0.9461 | 0.0004 | 2.0000 | 0.9479 | 0.9923 | 0.9958 | 0.0600 | 0.9557 |
| unsw | B | M10 | 0.8868 | 0.0005 | 0.9474 | 0.0002 | 0.9433 | 0.0003 | 4.0000 | 0.9459 | 0.9917 | 0.9955 | 0.0595 | 0.9512 |
| unsw | C-naive | M01 | 0.5232 | 0.0050 | 0.7022 | 0.0052 | 0.7022 | 0.0052 | 10.0000 | 0.7614 | 0.9119 | 0.9420 | 0.0257 | 0.5485 |
| unsw | C-naive | M02 | 0.7878 | 0.0019 | 0.9027 | 0.0009 | 0.8906 | 0.0010 | 8.0000 | 0.8782 | 0.9755 | 0.9853 | 0.2098 | 0.9662 |
| unsw | C-naive | M03 | 0.7697 | 0.0019 | 0.8911 | 0.0009 | 0.8728 | 0.0011 | 9.0000 | 0.8516 | 0.9681 | 0.9815 | 0.2902 | 0.9935 |
| unsw | C-naive | M04 | 0.8607 | 0.0023 | 0.9357 | 0.0010 | 0.9304 | 0.0011 | 6.0000 | 0.9306 | 0.9326 | 0.9364 | 0.0877 | 0.9489 |
| unsw | C-naive | M05 | 0.8917 | 0.0016 | 0.9499 | 0.0007 | 0.9458 | 0.0008 | 1.2000 | 0.9466 | 0.9916 | 0.9951 | 0.0652 | 0.9585 |
| unsw | C-naive | M06 | 0.8877 | 0.0017 | 0.9481 | 0.0008 | 0.9438 | 0.0009 | 3.3000 | 0.9448 | 0.9895 | 0.9930 | 0.0667 | 0.9564 |
| unsw | C-naive | M07 | 0.8180 | 0.0066 | 0.9164 | 0.0029 | 0.9089 | 0.0034 | 7.0000 | 0.9069 | 0.9796 | 0.9884 | 0.1269 | 0.9408 |
| unsw | C-naive | M08 | 0.8847 | 0.0016 | 0.9464 | 0.0008 | 0.9422 | 0.0008 | 5.0000 | 0.9449 | 0.9914 | 0.9953 | 0.0604 | 0.9502 |
| unsw | C-naive | M09 | 0.8909 | 0.0013 | 0.9494 | 0.0006 | 0.9454 | 0.0006 | 1.8000 | 0.9472 | 0.9920 | 0.9956 | 0.0609 | 0.9553 |
| unsw | C-naive | M10 | 0.8866 | 0.0023 | 0.9473 | 0.0011 | 0.9432 | 0.0012 | 3.7000 | 0.9458 | 0.9916 | 0.9954 | 0.0594 | 0.9510 |
| unsw | C-group | M01 | 0.5157 | 0.0140 | 0.6933 | 0.0127 | 0.6932 | 0.0128 | 10.0000 | 0.7555 | 0.9125 | 0.9441 | 0.0207 | 0.5317 |
| unsw | C-group | M02 | 0.7876 | 0.0034 | 0.9026 | 0.0014 | 0.8904 | 0.0015 | 8.0000 | 0.8778 | 0.9754 | 0.9852 | 0.2115 | 0.9670 |
| unsw | C-group | M03 | 0.7697 | 0.0024 | 0.8912 | 0.0011 | 0.8730 | 0.0014 | 9.0000 | 0.8518 | 0.9678 | 0.9813 | 0.2896 | 0.9932 |
| unsw | C-group | M04 | 0.8467 | 0.0044 | 0.9292 | 0.0021 | 0.9233 | 0.0022 | 6.0000 | 0.9238 | 0.9253 | 0.9298 | 0.0955 | 0.9431 |
| unsw | C-group | M05 | 0.8814 | 0.0035 | 0.9451 | 0.0017 | 0.9407 | 0.0018 | 3.3000 | 0.9418 | 0.9904 | 0.9945 | 0.0699 | 0.9536 |
| unsw | C-group | M06 | 0.8768 | 0.0042 | 0.9430 | 0.0020 | 0.9384 | 0.0021 | 5.0000 | 0.9395 | 0.9897 | 0.9940 | 0.0730 | 0.9520 |
| unsw | C-group | M07 | 0.8184 | 0.0057 | 0.9166 | 0.0026 | 0.9091 | 0.0029 | 7.0000 | 0.9069 | 0.9795 | 0.9883 | 0.1280 | 0.9418 |
| unsw | C-group | M08 | 0.8812 | 0.0044 | 0.9448 | 0.0021 | 0.9405 | 0.0022 | 2.9000 | 0.9429 | 0.9909 | 0.9951 | 0.0639 | 0.9497 |
| unsw | C-group | M09 | 0.8836 | 0.0045 | 0.9461 | 0.0022 | 0.9418 | 0.0023 | 1.2000 | 0.9434 | 0.9912 | 0.9952 | 0.0661 | 0.9529 |
| unsw | C-group | M10 | 0.8820 | 0.0043 | 0.9452 | 0.0021 | 0.9409 | 0.0022 | 2.6000 | 0.9433 | 0.9911 | 0.9951 | 0.0634 | 0.9501 |
| nslkdd | A | M01 | 0.3588 | 0.0000 | 0.5828 | 0.0000 | 0.5495 | 0.0000 | 10.0000 | 0.6325 | 0.6883 | 0.7286 | 0.0082 | 0.2733 |
| nslkdd | A | M02 | 0.5646 | 0.0000 | 0.7578 | 0.0000 | 0.7574 | 0.0000 | 9.0000 | 0.7782 | 0.7942 | 0.8658 | 0.0742 | 0.6306 |
| nslkdd | A | M03 | 0.5759 | 0.0000 | 0.7632 | 0.0000 | 0.7628 | 0.0000 | 8.0000 | 0.7837 | 0.8524 | 0.9020 | 0.0679 | 0.6353 |
| nslkdd | A | M04 | 0.6348 | 0.0122 | 0.7912 | 0.0081 | 0.7908 | 0.0083 | 3.4000 | 0.8125 | 0.8127 | 0.8287 | 0.0334 | 0.6584 |
| nslkdd | A | M05 | 0.6088 | 0.0093 | 0.7711 | 0.0064 | 0.7700 | 0.0066 | 6.9000 | 0.7957 | 0.9579 | 0.9594 | 0.0269 | 0.6182 |
| nslkdd | A | M06 | 0.6239 | 0.0136 | 0.7842 | 0.0057 | 0.7837 | 0.0057 | 5.4000 | 0.8063 | 0.9503 | 0.9533 | 0.0347 | 0.6472 |
| nslkdd | A | M07 | 0.6314 | 0.0000 | 0.7901 | 0.0000 | 0.7898 | 0.0000 | 3.6000 | 0.8111 | 0.9470 | 0.9478 | 0.0372 | 0.6595 |
| nslkdd | A | M08 | 0.6477 | 0.0000 | 0.7981 | 0.0000 | 0.7978 | 0.0000 | 1.3000 | 0.8193 | 0.9601 | 0.9656 | 0.0282 | 0.6667 |
| nslkdd | A | M09 | 0.6445 | 0.0000 | 0.7961 | 0.0000 | 0.7957 | 0.0000 | 2.3000 | 0.8174 | 0.9616 | 0.9618 | 0.0285 | 0.6634 |
| nslkdd | A | M10 | 0.6289 | 0.0000 | 0.7855 | 0.0000 | 0.7849 | 0.0000 | 5.1000 | 0.8081 | 0.9634 | 0.9670 | 0.0284 | 0.6447 |
| nslkdd | B | M01 | 0.6748 | 0.0002 | 0.8177 | 0.0002 | 0.8089 | 0.0002 | 10.0000 | 0.8107 | 0.8437 | 0.8354 | 0.0054 | 0.6269 |
| nslkdd | B | M02 | 0.9140 | 0.0002 | 0.9570 | 0.0001 | 0.9569 | 0.0001 | 8.0000 | 0.9565 | 0.9911 | 0.9906 | 0.0309 | 0.9440 |
| nslkdd | B | M03 | 0.8932 | 0.0002 | 0.9463 | 0.0001 | 0.9462 | 0.0001 | 9.0000 | 0.9455 | 0.9877 | 0.9845 | 0.0309 | 0.9218 |
| nslkdd | B | M04 | 0.9893 | 0.0003 | 0.9947 | 0.0001 | 0.9947 | 0.0001 | 6.0000 | 0.9947 | 0.9949 | 0.9919 | 0.0050 | 0.9943 |
| nslkdd | B | M05 | 0.9918 | 0.0002 | 0.9959 | 0.0001 | 0.9959 | 0.0001 | 4.0000 | 0.9959 | 0.9997 | 0.9997 | 0.0031 | 0.9949 |
| nslkdd | B | M06 | 0.9912 | 0.0002 | 0.9956 | 0.0001 | 0.9956 | 0.0001 | 5.0000 | 0.9956 | 0.9987 | 0.9981 | 0.0035 | 0.9946 |
| nslkdd | B | M07 | 0.9313 | 0.0007 | 0.9657 | 0.0004 | 0.9656 | 0.0004 | 7.0000 | 0.9655 | 0.9948 | 0.9945 | 0.0287 | 0.9596 |
| nslkdd | B | M08 | 0.9933 | 0.0001 | 0.9967 | 0.0001 | 0.9967 | 0.0001 | 2.4000 | 0.9966 | 0.9999 | 0.9999 | 0.0026 | 0.9958 |
| nslkdd | B | M09 | 0.9934 | 0.0002 | 0.9967 | 0.0001 | 0.9967 | 0.0001 | 2.2000 | 0.9967 | 0.9999 | 0.9999 | 0.0028 | 0.9962 |
| nslkdd | B | M10 | 0.9934 | 0.0002 | 0.9967 | 0.0001 | 0.9967 | 0.0001 | 1.4000 | 0.9967 | 0.9999 | 0.9999 | 0.0025 | 0.9959 |
| nslkdd | C-naive | M01 | 0.6768 | 0.0033 | 0.8190 | 0.0021 | 0.8104 | 0.0024 | 10.0000 | 0.8121 | 0.8456 | 0.8371 | 0.0056 | 0.6298 |
| nslkdd | C-naive | M02 | 0.9135 | 0.0024 | 0.9567 | 0.0012 | 0.9566 | 0.0012 | 8.0000 | 0.9563 | 0.9911 | 0.9908 | 0.0309 | 0.9435 |
| nslkdd | C-naive | M03 | 0.8925 | 0.0020 | 0.9460 | 0.0010 | 0.9458 | 0.0010 | 9.0000 | 0.9451 | 0.9877 | 0.9848 | 0.0308 | 0.9210 |
| nslkdd | C-naive | M04 | 0.9893 | 0.0011 | 0.9947 | 0.0005 | 0.9947 | 0.0005 | 6.0000 | 0.9947 | 0.9949 | 0.9919 | 0.0051 | 0.9944 |
| nslkdd | C-naive | M05 | 0.9916 | 0.0006 | 0.9958 | 0.0003 | 0.9958 | 0.0003 | 4.0000 | 0.9958 | 0.9997 | 0.9996 | 0.0031 | 0.9946 |
| nslkdd | C-naive | M06 | 0.9910 | 0.0007 | 0.9955 | 0.0003 | 0.9955 | 0.0003 | 5.0000 | 0.9955 | 0.9986 | 0.9978 | 0.0034 | 0.9944 |
| nslkdd | C-naive | M07 | 0.9307 | 0.0031 | 0.9654 | 0.0015 | 0.9653 | 0.0015 | 7.0000 | 0.9651 | 0.9948 | 0.9945 | 0.0285 | 0.9588 |
| nslkdd | C-naive | M08 | 0.9928 | 0.0004 | 0.9964 | 0.0002 | 0.9964 | 0.0002 | 2.4000 | 0.9964 | 0.9999 | 0.9999 | 0.0029 | 0.9956 |
| nslkdd | C-naive | M09 | 0.9933 | 0.0006 | 0.9967 | 0.0003 | 0.9967 | 0.0003 | 1.5000 | 0.9966 | 0.9999 | 0.9999 | 0.0028 | 0.9961 |
| nslkdd | C-naive | M10 | 0.9929 | 0.0007 | 0.9965 | 0.0003 | 0.9965 | 0.0003 | 2.1000 | 0.9964 | 0.9999 | 0.9999 | 0.0028 | 0.9957 |
| nslkdd | C-group | M01 | 0.6734 | 0.0028 | 0.8168 | 0.0015 | 0.8079 | 0.0016 | 10.0000 | 0.8099 | 0.8426 | 0.8342 | 0.0054 | 0.6252 |
| nslkdd | C-group | M02 | 0.9144 | 0.0020 | 0.9572 | 0.0010 | 0.9571 | 0.0010 | 8.0000 | 0.9567 | 0.9911 | 0.9905 | 0.0308 | 0.9442 |
| nslkdd | C-group | M03 | 0.8935 | 0.0025 | 0.9465 | 0.0013 | 0.9463 | 0.0013 | 9.0000 | 0.9456 | 0.9878 | 0.9848 | 0.0308 | 0.9220 |
| nslkdd | C-group | M04 | 0.9900 | 0.0009 | 0.9950 | 0.0005 | 0.9950 | 0.0005 | 6.0000 | 0.9950 | 0.9955 | 0.9929 | 0.0044 | 0.9944 |
| nslkdd | C-group | M05 | 0.9927 | 0.0009 | 0.9964 | 0.0004 | 0.9964 | 0.0004 | 3.7000 | 0.9963 | 0.9998 | 0.9997 | 0.0023 | 0.9950 |
| nslkdd | C-group | M06 | 0.9922 | 0.0007 | 0.9961 | 0.0004 | 0.9961 | 0.0004 | 4.8000 | 0.9961 | 0.9997 | 0.9995 | 0.0027 | 0.9948 |
| nslkdd | C-group | M07 | 0.9314 | 0.0011 | 0.9657 | 0.0006 | 0.9656 | 0.0006 | 7.0000 | 0.9654 | 0.9948 | 0.9946 | 0.0274 | 0.9583 |
| nslkdd | C-group | M08 | 0.9934 | 0.0008 | 0.9967 | 0.0004 | 0.9967 | 0.0004 | 2.9000 | 0.9967 | 0.9999 | 0.9999 | 0.0023 | 0.9957 |
| nslkdd | C-group | M09 | 0.9939 | 0.0007 | 0.9970 | 0.0003 | 0.9970 | 0.0003 | 1.3000 | 0.9969 | 0.9999 | 0.9999 | 0.0023 | 0.9962 |
| nslkdd | C-group | M10 | 0.9936 | 0.0008 | 0.9968 | 0.0004 | 0.9968 | 0.0004 | 2.3000 | 0.9968 | 0.9999 | 0.9999 | 0.0023 | 0.9959 |

## T4_rank_side_by_side

| dataset | model_id | rank_A | rank_B | rank_C-naive | rank_C-group | change_A_to_C-naive | change_A_to_C-group |
|---|---|---|---|---|---|---|---|
| unsw | M01 | 10.0000 | 10.0000 | 10.0000 | 10.0000 | 0.0000 | 0.0000 |
| unsw | M02 | 9.0000 | 8.0000 | 8.0000 | 8.0000 | -1.0000 | -1.0000 |
| unsw | M03 | 8.0000 | 9.0000 | 9.0000 | 9.0000 | 1.0000 | 1.0000 |
| unsw | M04 | 6.0000 | 6.0000 | 6.0000 | 6.0000 | 0.0000 | 0.0000 |
| unsw | M05 | 2.2000 | 1.0000 | 1.2000 | 3.3000 | -1.0000 | 1.1000 |
| unsw | M06 | 5.0000 | 3.0000 | 3.3000 | 5.0000 | -1.7000 | 0.0000 |
| unsw | M07 | 7.0000 | 7.0000 | 7.0000 | 7.0000 | 0.0000 | 0.0000 |
| unsw | M08 | 2.8000 | 5.0000 | 5.0000 | 2.9000 | 2.2000 | 0.1000 |
| unsw | M09 | 4.0000 | 2.0000 | 1.8000 | 1.2000 | -2.2000 | -2.8000 |
| unsw | M10 | 1.0000 | 4.0000 | 3.7000 | 2.6000 | 2.7000 | 1.6000 |
| unsw | top ranked | M10 | M05 | M05 | M09 |  |  |
| nslkdd | M01 | 10.0000 | 10.0000 | 10.0000 | 10.0000 | 0.0000 | 0.0000 |
| nslkdd | M02 | 9.0000 | 8.0000 | 8.0000 | 8.0000 | -1.0000 | -1.0000 |
| nslkdd | M03 | 8.0000 | 9.0000 | 9.0000 | 9.0000 | 1.0000 | 1.0000 |
| nslkdd | M04 | 3.4000 | 6.0000 | 6.0000 | 6.0000 | 2.6000 | 2.6000 |
| nslkdd | M05 | 6.9000 | 4.0000 | 4.0000 | 3.7000 | -2.9000 | -3.2000 |
| nslkdd | M06 | 5.4000 | 5.0000 | 5.0000 | 4.8000 | -0.4000 | -0.6000 |
| nslkdd | M07 | 3.6000 | 7.0000 | 7.0000 | 7.0000 | 3.4000 | 3.4000 |
| nslkdd | M08 | 1.3000 | 2.4000 | 2.4000 | 2.9000 | 1.1000 | 1.6000 |
| nslkdd | M09 | 2.3000 | 2.2000 | 1.5000 | 1.3000 | -0.8000 | -1.0000 |
| nslkdd | M10 | 5.1000 | 1.4000 | 2.1000 | 2.3000 | -3.0000 | -2.8000 |
| nslkdd | top ranked | M08 | M10 | M09 | M09 |  |  |

## T5_between_arm

| dataset | contrast | n_pairs | tau_b_mean | tau_b_ci_lo | tau_b_ci_hi | rho_mean | rho_ci_lo | rho_ci_hi |
|---|---|---|---|---|---|---|---|---|
| unsw | A vs C-naive | 100 | 0.7289 | 0.6782 | 0.7778 | 0.8550 | 0.8154 | 0.9030 |
| unsw | C-naive vs C-group | 100 | 0.8071 | 0.7884 | 0.8524 | 0.8999 | 0.8868 | 0.9310 |
| unsw | B vs C-naive | 50 | 0.9778 | 0.9378 | 0.9822 | 0.9939 | 0.9794 | 0.9952 |
| unsw | A vs B | 50 | 0.7244 | 0.6657 | 0.7733 | 0.8448 | 0.8024 | 0.8897 |
| nslkdd | A vs C-naive | 100 | 0.5333 | 0.5111 | 0.6372 | 0.7149 | 0.6890 | 0.8085 |
| nslkdd | C-naive vs C-group | 100 | 0.9244 | 0.8471 | 0.9182 | 0.9702 | 0.9250 | 0.9687 |
| nslkdd | B vs C-naive | 50 | 0.9333 | 0.8844 | 0.9458 | 0.9758 | 0.9503 | 0.9813 |
| nslkdd | A vs B | 50 | 0.5111 | 0.4978 | 0.6311 | 0.6912 | 0.6800 | 0.8044 |

## T6_within_arm

| dataset | arm | metric | tau_b_mean | tau_b_min | tau_b_max | tau_b_p5 | n_pairs | friedman_note | friedman_chi2 | friedman_p | iman_davenport_F | iman_davenport_p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unsw | A | mcc | 0.9842 | 0.9556 | 1.0000 | 0.9556 | 45 | Protocol A has one fixed split, so seeds change model randomness only. Seven models (M01, M02, M03, M07, M08, M09, M10) gave identical predictions at every seed; only M04, M05 and M06 varied. These values are a diagnostic, not a noise floor. Friedman and Wilcoxon were not run because seven models give constant values; within-A separability comes from the bootstrap intervals on each model's metric. |  |  |  |  |
| unsw | A | accuracy | 0.9635 | 0.9111 | 1.0000 | 0.9111 | 45 |  |  |  |  |  |
| unsw | A | macro_f1 | 0.9477 | 0.8667 | 1.0000 | 0.8667 | 45 |  |  |  |  |  |
| unsw | B | mcc | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 10 | Chi-square is at its maximum, N(k-1) = 45, because all five repeats rank the ten models identically. The Iman-Davenport F is infinite in the limit and its p-value is 0. | 45.0000 | 0.0000 | inf | 0.0000 |
| unsw | B | accuracy | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 10 |  |  |  |  |  |
| unsw | B | macro_f1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 10 |  |  |  |  |  |
| unsw | C-naive | mcc | 0.9635 | 0.9111 | 1.0000 | 0.9111 | 45 |  | 89.1927 | 0.0000 | 994.3784 | 0.0000 |
| unsw | C-naive | accuracy | 0.9822 | 0.9111 | 1.0000 | 0.9556 | 45 |  |  |  |  |  |
| unsw | C-naive | macro_f1 | 0.9635 | 0.9111 | 1.0000 | 0.9111 | 45 |  |  |  |  |  |
| unsw | C-group | mcc | 0.9170 | 0.8222 | 1.0000 | 0.8222 | 45 |  | 87.2727 | 0.0000 | 288.0000 | 0.0000 |
| unsw | C-group | accuracy | 0.9121 | 0.8222 | 1.0000 | 0.8222 | 45 |  |  |  |  |  |
| unsw | C-group | macro_f1 | 0.9141 | 0.8222 | 1.0000 | 0.8222 | 45 |  |  |  |  |  |
| nslkdd | A | mcc | 0.8558 | 0.7333 | 1.0000 | 0.7333 | 45 | Protocol A has one fixed split, so seeds change model randomness only. Seven models (M01, M02, M03, M07, M08, M09, M10) gave identical predictions at every seed; only M04, M05 and M06 varied. These values are a diagnostic, not a noise floor. Friedman and Wilcoxon were not run because seven models give constant values; within-A separability comes from the bootstrap intervals on each model's metric. |  |  |  |  |
| nslkdd | A | accuracy | 0.8430 | 0.6889 | 0.9556 | 0.6978 | 45 |  |  |  |  |  |
| nslkdd | A | macro_f1 | 0.8430 | 0.6889 | 0.9556 | 0.6978 | 45 |  |  |  |  |  |
| nslkdd | B | mcc | 0.9378 | 0.8667 | 1.0000 | 0.8867 | 10 |  | 44.2145 | 0.0000 | 225.1667 | 0.0000 |
| nslkdd | B | accuracy | 0.9376 | 0.8667 | 0.9888 | 0.8812 | 10 |  |  |  |  |  |
| nslkdd | B | macro_f1 | 0.9289 | 0.8667 | 1.0000 | 0.8667 | 10 |  |  |  |  |  |
| nslkdd | C-naive | mcc | 0.9398 | 0.8667 | 1.0000 | 0.8667 | 45 |  | 88.2764 | 0.0000 | 460.9367 | 0.0000 |
| nslkdd | C-naive | accuracy | 0.9537 | 0.8866 | 1.0000 | 0.8989 | 45 |  |  |  |  |  |
| nslkdd | C-naive | macro_f1 | 0.9427 | 0.8222 | 1.0000 | 0.8667 | 45 |  |  |  |  |  |
| nslkdd | C-group | mcc | 0.9052 | 0.7778 | 1.0000 | 0.7867 | 45 |  | 86.8582 | 0.0000 | 248.8125 | 0.0000 |
| nslkdd | C-group | accuracy | 0.9208 | 0.8090 | 1.0000 | 0.8409 | 45 |  |  |  |  |  |
| nslkdd | C-group | macro_f1 | 0.9141 | 0.8222 | 1.0000 | 0.8667 | 45 |  |  |  |  |  |

## T7_robustness

| dataset | contrast | metric | tau_b_mean_ten | tau_b_mean_seven | leak_rate_pct_Cnaive_mean | leak_rate_pct_Cgroup_mean |
|---|---|---|---|---|---|---|
| unsw | A vs C-naive | mcc | 0.7289 | 0.5143 |  |  |
| unsw | A vs C-naive | accuracy | 0.6782 | 0.4057 |  |  |
| unsw | A vs C-naive | macro_f1 | 0.7120 | 0.3829 |  |  |
| unsw | C-naive vs C-group | mcc | 0.8071 | 0.5867 | 44.3421 | 0.0000 |
| unsw | C-naive vs C-group | accuracy | 0.8071 | 0.5867 | 44.3421 | 0.0000 |
| unsw | C-naive vs C-group | macro_f1 | 0.8116 | 0.5962 | 44.3421 | 0.0000 |
| unsw | B vs C-naive | mcc | 0.9778 | 0.9524 |  |  |
| unsw | B vs C-naive | accuracy | 0.9911 | 0.9810 |  |  |
| unsw | B vs C-naive | macro_f1 | 0.9778 | 0.9524 |  |  |
| unsw | A vs B | mcc | 0.7244 | 0.5048 |  |  |
| unsw | A vs B | accuracy | 0.6844 | 0.4190 |  |  |
| unsw | A vs B | macro_f1 | 0.6933 | 0.3429 |  |  |
| nslkdd | A vs C-naive | mcc | 0.5333 | 0.0952 |  |  |
| nslkdd | A vs C-naive | accuracy | 0.5221 | 0.0865 |  |  |
| nslkdd | A vs C-naive | macro_f1 | 0.5236 | 0.0933 |  |  |
| nslkdd | C-naive vs C-group | mcc | 0.9244 | 0.8381 | 0.8379 | 0.0000 |
| nslkdd | C-naive vs C-group | accuracy | 0.9391 | 0.8680 | 0.8379 | 0.0000 |
| nslkdd | C-naive vs C-group | macro_f1 | 0.9316 | 0.8533 | 0.8379 | 0.0000 |
| nslkdd | B vs C-naive | mcc | 0.9333 | 0.8571 |  |  |
| nslkdd | B vs C-naive | accuracy | 0.9392 | 0.8688 |  |  |
| nslkdd | B vs C-naive | macro_f1 | 0.9324 | 0.8552 |  |  |
| nslkdd | A vs B | mcc | 0.5111 | 0.0476 |  |  |
| nslkdd | A vs B | accuracy | 0.5033 | 0.0477 |  |  |
| nslkdd | A vs B | macro_f1 | 0.5067 | 0.0571 |  |  |

## T8_distribution_shift

| dataset | partition | n_splits | train_attack_rate | test_attack_rate | attack_rate_diff_pp | tvd_attack_categories | test_categories_absent_from_train | mean_tau_b_A_vs_C-naive_mcc |
|---|---|---|---|---|---|---|---|---|
| unsw | publisher (A) | 10 | 0.6806 | 0.5506 | -13.0022 | 0.0811 | 0.0000 | 0.7289 |
| unsw | C-naive | 10 | 0.6391 | 0.6391 | 0.0009 | 0.0047 | 0.0000 |  |
| unsw | C-group | 10 | 0.6391 | 0.6391 | 0.0009 | 0.0226 | 0.0000 |  |
| nslkdd | publisher (A) | 10 | 0.4654 | 0.5692 | 10.3825 | 0.4825 | 17.0000 | 0.5333 |
| nslkdd | C-naive | 10 | 0.4812 | 0.4812 | 0.0018 | 0.0143 | 0.2000 |  |
| nslkdd | C-group | 10 | 0.4812 | 0.4812 | 0.0018 | 0.0113 | 0.1000 |  |
