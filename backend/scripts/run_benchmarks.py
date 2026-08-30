#!/usr/bin/env python
"""Run the complete Phase 2 benchmark suite.

Examples:
    python scripts/run_benchmarks.py --dataset website_phishing
    python scripts/run_benchmarks.py --dataset kddcup99
    python scripts/run_benchmarks.py --dataset website_phishing --output benchmark/results
"""

import argparse
from pathlib import Path
import json

from benchmark.datasets import DATASET_LOADERS
from anomaly.services.benchmark_service import BenchmarkService
from anomaly.services.benchmark_statistics import BenchmarkStatistics
from anomaly.services.benchmark_report_service import BenchmarkReportService


def run(dataset_name, output):
    loader = DATASET_LOADERS[dataset_name]
    df, metadata = loader()
    metadata["rows"] = len(df)
    metadata["features"] = len(df.columns) - 1

    target = "label" if "label" in df.columns else "Result"

    comparison = BenchmarkService.compare_models(
        df, target_column=target, contamination=0.05, seed=42
    )

    contamination = BenchmarkService.contamination_experiment(
        df, target_column=target, seed=42
    )

    threshold = BenchmarkService.threshold_experiment(
        df, target_column=target, model_name="isolation_forest", seed=42
    )

    ensemble = BenchmarkService.ensemble_evaluation(
        df, target_column=target, contamination=0.05, seed=42
    )

    repeated = BenchmarkService.repeated_runs(
        df, target_column=target, seeds=(7, 21, 42, 84, 168)
    )
    summary = BenchmarkStatistics.summarize(repeated)
    friedman = BenchmarkStatistics.friedman_test(repeated, metric="f1_score")
    pairwise = BenchmarkStatistics.pairwise_wilcoxon(repeated, metric="f1_score")

    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)

    BenchmarkReportService.write_csv(comparison, output / "model_comparison.csv")
    BenchmarkReportService.write_csv(contamination, output / "contamination_experiment.csv")
    BenchmarkReportService.write_csv(threshold, output / "threshold_experiment.csv")
    BenchmarkReportService.write_csv(repeated, output / "repeated_runs.csv")
    BenchmarkReportService.write_csv(summary, output / "statistical_summary.csv")
    BenchmarkReportService.write_csv(pairwise, output / "pairwise_wilcoxon.csv")

    BenchmarkReportService.write_json(
        {"dataset": metadata, "ensemble": ensemble, "friedman": friedman},
        output / "benchmark_metadata.json",
    )
    BenchmarkReportService.write_markdown(
        output / "benchmark_report.md",
        metadata,
        comparison,
        contamination,
        threshold,
        ensemble,
        summary,
        friedman,
        pairwise,
    )

    print(f"Benchmark complete: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=sorted(DATASET_LOADERS), default="website_phishing")
    parser.add_argument("--output", default="benchmark/results")
    args = parser.parse_args()
    run(args.dataset, args.output)
