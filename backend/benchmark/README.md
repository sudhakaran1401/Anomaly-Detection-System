# Phase 2 Benchmark Suite

This suite completes the ML evaluation and benchmarking phase.

## Included real-world datasets

1. **UCI Website Phishing (dataset 379)**
   - 1,353 instances
   - 9 integer features
   - Legitimate = normal
   - Phishy = anomaly
   - Suspicious rows are excluded because their ground truth is ambiguous.
   - Source: UCI Machine Learning Repository.
   - DOI: 10.24432/C5B301.

2. **KDD Cup 1999 (10% subset)**
   - Public intrusion-detection benchmark.
   - `normal.` = normal.
   - All attack categories = anomaly.
   - A reproducible stratified sample is used to keep local runtime practical.

## Experiments

The runner produces:

- `model_comparison.csv`
- `contamination_experiment.csv`
- `threshold_experiment.csv`
- `repeated_runs.csv`
- `statistical_summary.csv`
- `pairwise_wilcoxon.csv`
- `benchmark_metadata.json`
- `benchmark_report.md`

The benchmark compares Isolation Forest, LOF, One-Class SVM and DBSCAN.

It also evaluates a majority-vote ensemble, contamination settings, score thresholds, repeated random seeds, runtime, and statistical differences.

## Reproducibility

All experiments use explicit seeds. Dataset sampling is deterministic. The exact parameter grids are stored in the output tables.

## Running

From `backend/`:

```bash
python scripts/run_benchmarks.py --dataset website_phishing
python scripts/run_benchmarks.py --dataset kddcup99
```

The Website Phishing dataset is downloaded from UCI the first time it is used. KDD Cup 1999 is retrieved through scikit-learn.

For academic reporting, cite the original dataset sources rather than treating the benchmark output as a new dataset.


3. **Breast Cancer Wisconsin (Diagnostic)**
   - 569 instances and 30 numeric features.
   - Bundled with scikit-learn, so it can run without an external download.
   - Malignant is treated as anomaly and benign as normal.
   - This is explicitly a **proxy anomaly benchmark**, because the original task is supervised diagnosis.

The first two datasets are the primary anomaly-oriented benchmarks; the breast-cancer dataset provides an offline, reproducible real-world sanity benchmark.
