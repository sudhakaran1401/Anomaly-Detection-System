# Anomaly Detection Benchmark Report

## Dataset

- Name: Breast Cancer Wisconsin (Diagnostic)
- Source: UCI Machine Learning Repository via scikit-learn
- License/citation: Street, W.N., Wolberg, W.H., Mangasarian, O.L. (1993)
- Rows evaluated: 569
- Numeric features: 30
- Normal/anomaly mapping: Malignant=1 anomaly; Benign=0 normal (proxy anomaly benchmark)

## Model comparison

```text
           model  seed  contamination threshold  accuracy  precision  recall  f1_score  specificity  false_positive_rate  false_negative_rate                                                                          confusion_matrix  anomaly_count  runtime_seconds
isolation_forest    42           0.05      None    0.6538     0.7586  0.1038    0.1826       0.9804               0.0196               0.8962   {'true_negative': 350, 'false_positive': 7, 'false_negative': 190, 'true_positive': 22}             29         0.091899
             lof    42           0.05      None    0.6292     0.5200  0.0613    0.1097       0.9664               0.0336               0.9387  {'true_negative': 345, 'false_positive': 12, 'false_negative': 199, 'true_positive': 13}             25         0.021484
   one_class_svm    42           0.05      None    0.6327     0.5053  0.6792    0.5795       0.6050               0.3950               0.3208 {'true_negative': 216, 'false_positive': 141, 'false_negative': 68, 'true_positive': 144}            285         0.015755
          dbscan    42           0.05      None    0.3726     0.3726  1.0000    0.5429       0.0000               1.0000               0.0000    {'true_negative': 0, 'false_positive': 357, 'false_negative': 0, 'true_positive': 212}            569         0.001630
```

## Contamination experiment

```text
           model  seed  contamination threshold  accuracy  precision  recall  f1_score  specificity  false_positive_rate  false_negative_rate                                                                          confusion_matrix  anomaly_count  runtime_seconds
isolation_forest    42           0.01      None    0.6344     0.8333  0.0236    0.0459       0.9972               0.0028               0.9764    {'true_negative': 356, 'false_positive': 1, 'false_negative': 207, 'true_positive': 5}              6         0.087734
             lof    42           0.01      None    0.6309     0.6667  0.0189    0.0367       0.9944               0.0056               0.9811    {'true_negative': 355, 'false_positive': 2, 'false_negative': 208, 'true_positive': 4}              6         0.007199
   one_class_svm    42           0.01      None    0.6327     0.5053  0.6792    0.5795       0.6050               0.3950               0.3208 {'true_negative': 216, 'false_positive': 141, 'false_negative': 68, 'true_positive': 144}            285         0.016723
          dbscan    42           0.01      None    0.3726     0.3726  1.0000    0.5429       0.0000               1.0000               0.0000    {'true_negative': 0, 'false_positive': 357, 'false_negative': 0, 'true_positive': 212}            569         0.001421
isolation_forest    42           0.03      None    0.6485     0.8333  0.0708    0.1304       0.9916               0.0084               0.9292   {'true_negative': 354, 'false_positive': 3, 'false_negative': 197, 'true_positive': 15}             18         0.084160
             lof    42           0.03      None    0.6274     0.5000  0.0377    0.0702       0.9776               0.0224               0.9623    {'true_negative': 349, 'false_positive': 8, 'false_negative': 204, 'true_positive': 8}             16         0.005988
   one_class_svm    42           0.03      None    0.6327     0.5053  0.6792    0.5795       0.6050               0.3950               0.3208 {'true_negative': 216, 'false_positive': 141, 'false_negative': 68, 'true_positive': 144}            285         0.014234
          dbscan    42           0.03      None    0.3726     0.3726  1.0000    0.5429       0.0000               1.0000               0.0000    {'true_negative': 0, 'false_positive': 357, 'false_negative': 0, 'true_positive': 212}            569         0.001362
isolation_forest    42           0.05      None    0.6538     0.7586  0.1038    0.1826       0.9804               0.0196               0.8962   {'true_negative': 350, 'false_positive': 7, 'false_negative': 190, 'true_positive': 22}             29         0.087505
             lof    42           0.05      None    0.6292     0.5200  0.0613    0.1097       0.9664               0.0336               0.9387  {'true_negative': 345, 'false_positive': 12, 'false_negative': 199, 'true_positive': 13}             25         0.006129
   one_class_svm    42           0.05      None    0.6327     0.5053  0.6792    0.5795       0.6050               0.3950               0.3208 {'true_negative': 216, 'false_positive': 141, 'false_negative': 68, 'true_positive': 144}            285         0.015193
          dbscan    42           0.05      None    0.3726     0.3726  1.0000    0.5429       0.0000               1.0000               0.0000    {'true_negative': 0, 'false_positive': 357, 'false_negative': 0, 'true_positive': 212}            569         0.001305
isolation_forest    42           0.10      None    0.6608     0.6667  0.1792    0.2825       0.9468               0.0532               0.8208  {'true_negative': 338, 'false_positive': 19, 'false_negative': 174, 'true_positive': 38}             57         0.090947
             lof    42           0.10      None    0.6169     0.4400  0.1038    0.1679       0.9216               0.0784               0.8962  {'true_negative': 329, 'false_positive': 28, 'false_negative': 190, 'true_positive': 22}             50         0.006415
   one_class_svm    42           0.10      None    0.6327     0.5053  0.6792    0.5795       0.6050               0.3950               0.3208 {'true_negative': 216, 'false_positive': 141, 'false_negative': 68, 'true_positive': 144}            285         0.017580
          dbscan    42           0.10      None    0.3726     0.3726  1.0000    0.5429       0.0000               1.0000               0.0000    {'true_negative': 0, 'false_positive': 357, 'false_negative': 0, 'true_positive': 212}            569         0.001539
isolation_forest    42           0.15      None    0.6837     0.6860  0.2783    0.3960       0.9244               0.0756               0.7217  {'true_negative': 330, 'false_positive': 27, 'false_negative': 153, 'true_positive': 59}             86         0.081888
             lof    42           0.15      None    0.6081     0.4267  0.1509    0.2230       0.8796               0.1204               0.8491  {'true_negative': 314, 'false_positive': 43, 'false_negative': 180, 'true_positive': 32}             75         0.006127
   one_class_svm    42           0.15      None    0.6327     0.5053  0.6792    0.5795       0.6050               0.3950               0.3208 {'true_negative': 216, 'false_positive': 141, 'false_negative': 68, 'true_positive': 144}            285         0.013433
          dbscan    42           0.15      None    0.3726     0.3726  1.0000    0.5429       0.0000               1.0000               0.0000    {'true_negative': 0, 'false_positive': 357, 'false_negative': 0, 'true_positive': 212}            569         0.001349
isolation_forest    42           0.20      None    0.6977     0.6754  0.3632    0.4724       0.8964               0.1036               0.6368  {'true_negative': 320, 'false_positive': 37, 'false_negative': 135, 'true_positive': 77}            114         0.091354
             lof    42           0.20      None    0.6063     0.4412  0.2123    0.2866       0.8403               0.1597               0.7877  {'true_negative': 300, 'false_positive': 57, 'false_negative': 167, 'true_positive': 45}            102         0.006528
   one_class_svm    42           0.20      None    0.6327     0.5053  0.6792    0.5795       0.6050               0.3950               0.3208 {'true_negative': 216, 'false_positive': 141, 'false_negative': 68, 'true_positive': 144}            285         0.013497
          dbscan    42           0.20      None    0.3726     0.3726  1.0000    0.5429       0.0000               1.0000               0.0000    {'true_negative': 0, 'false_positive': 357, 'false_negative': 0, 'true_positive': 212}            569         0.001747
```

## Score-threshold experiment

```text
           model  seed  contamination  threshold_quantile  threshold  accuracy  precision  recall  f1_score  specificity  false_positive_rate  false_negative_rate                                                                         confusion_matrix  anomaly_count  runtime_seconds
isolation_forest    42           0.05                0.90  -0.037010    0.6608     0.6667  0.1792    0.2825       0.9468               0.0532               0.8208 {'true_negative': 338, 'false_positive': 19, 'false_negative': 174, 'true_positive': 38}             57         0.089208
isolation_forest    42           0.05                0.95   0.000000    0.6538     0.7586  0.1038    0.1826       0.9804               0.0196               0.8962  {'true_negative': 350, 'false_positive': 7, 'false_negative': 190, 'true_positive': 22}             29         0.089208
isolation_forest    42           0.05                0.97   0.026648    0.6485     0.8333  0.0708    0.1304       0.9916               0.0084               0.9292  {'true_negative': 354, 'false_positive': 3, 'false_negative': 197, 'true_positive': 15}             18         0.089208
isolation_forest    42           0.05                0.99   0.084050    0.6344     0.8333  0.0236    0.0459       0.9972               0.0028               0.9764   {'true_negative': 356, 'false_positive': 1, 'false_negative': 207, 'true_positive': 5}              6         0.089208
```

## Ensemble evaluation

```json
{
  "model": "weighted_ensemble",
  "models": [
    "isolation_forest",
    "lof",
    "one_class_svm"
  ],
  "weights": [
    0.3333333333333333,
    0.3333333333333333,
    0.3333333333333333
  ],
  "seed": 42,
  "contamination": 0.05,
  "threshold": 0.5,
  "accuracy": 0.652,
  "precision": 0.6842,
  "recall": 0.1226,
  "f1_score": 0.208,
  "specificity": 0.9664,
  "false_positive_rate": 0.0336,
  "false_negative_rate": 0.8774,
  "confusion_matrix": {
    "true_negative": 345,
    "false_positive": 12,
    "false_negative": 186,
    "true_positive": 26
  },
  "anomaly_count": 38,
  "runtime_seconds": 0.105344
}
```

## Repeated-run statistics

```text
           model  runs  accuracy_mean  accuracy_std  accuracy_min  accuracy_max  precision_mean  precision_std  precision_min  precision_max  recall_mean  recall_std  recall_min  recall_max  f1_score_mean  f1_score_std  f1_score_min  f1_score_max  specificity_mean  specificity_std  specificity_min  specificity_max  runtime_mean_seconds  runtime_std_seconds
          dbscan     5         0.3726        0.0000        0.3726        0.3726          0.3726         0.0000         0.3726         0.3726       1.0000      0.0000      1.0000      1.0000         0.5429        0.0000        0.5429        0.5429            0.0000           0.0000           0.0000           0.0000              0.001666             0.000372
isolation_forest     5         0.6587        0.0047        0.6538        0.6643          0.8069         0.0463         0.7586         0.8621       0.1104      0.0063      0.1038      0.1179         0.1942        0.0111        0.1826        0.2075            0.9843           0.0038           0.9804           0.9888              0.084182             0.001696
             lof     5         0.6292        0.0000        0.6292        0.6292          0.5200         0.0000         0.5200         0.5200       0.0613      0.0000      0.0613      0.0613         0.1097        0.0000        0.1097        0.1097            0.9664           0.0000           0.9664           0.9664              0.006746             0.000669
   one_class_svm     5         0.6327        0.0000        0.6327        0.6327          0.5053         0.0000         0.5053         0.5053       0.6792      0.0000      0.6792      0.6792         0.5795        0.0000        0.5795        0.5795            0.6050           0.0000           0.6050           0.6050              0.013592             0.000266
```

## Friedman test

```json
{
  "metric": "f1_score",
  "statistic": 15.0,
  "p_value": 0.001817,
  "significant_at_0_05": true
}
```

## Pairwise Wilcoxon tests

```text
  metric          model_a          model_b  statistic  p_value  significant_at_0_05
f1_score           dbscan isolation_forest        0.0   0.0625                False
f1_score           dbscan              lof        0.0   0.0625                False
f1_score           dbscan    one_class_svm        0.0   0.0625                False
f1_score isolation_forest              lof        0.0   0.0625                False
f1_score isolation_forest    one_class_svm        0.0   0.0625                False
f1_score              lof    one_class_svm        0.0   0.0625                False
```

## Reproducibility

- All experiments use explicit random seeds.
- Dataset preprocessing is deterministic.
- Contamination and score-threshold grids are recorded in the output tables.
- Runtime is measured around model fitting and prediction.
