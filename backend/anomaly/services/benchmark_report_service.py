from pathlib import Path
import json
import pandas as pd


class BenchmarkReportService:
    """Persist benchmark tables and a human-readable Markdown report."""

    @staticmethod
    def write_csv(df, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        return str(path)

    @staticmethod
    def write_json(payload, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, default=str))
        return str(path)

    @staticmethod
    def write_markdown(
        path,
        dataset_metadata,
        comparison,
        contamination,
        threshold,
        ensemble,
        summary,
        friedman,
        pairwise,
    ):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        def table(df):
            if df is None or len(df) == 0:
                return "_No results._"
            return "```text\n" + df.to_string(index=False) + "\n```"

        lines = [
            "# Anomaly Detection Benchmark Report",
            "",
            "## Dataset",
            "",
            f"- Name: {dataset_metadata.get('name')}",
            f"- Source: {dataset_metadata.get('source')}",
            f"- License/citation: {dataset_metadata.get('citation')}",
            f"- Rows evaluated: {dataset_metadata.get('rows')}",
            f"- Numeric features: {dataset_metadata.get('features')}",
            f"- Normal/anomaly mapping: {dataset_metadata.get('label_mapping')}",
            "",
            "## Model comparison",
            "",
            table(comparison),
            "",
            "## Contamination experiment",
            "",
            table(contamination),
            "",
            "## Score-threshold experiment",
            "",
            table(threshold),
            "",
            "## Ensemble evaluation",
            "",
            "```json",
            json.dumps(ensemble, indent=2),
            "```",
            "",
            "## Repeated-run statistics",
            "",
            table(summary),
            "",
            "## Friedman test",
            "",
            "```json",
            json.dumps(friedman, indent=2),
            "```",
            "",
            "## Pairwise Wilcoxon tests",
            "",
            table(pairwise),
            "",
            "## Reproducibility",
            "",
            "- All experiments use explicit random seeds.",
            "- Dataset preprocessing is deterministic.",
            "- Contamination and score-threshold grids are recorded in the output tables.",
            "- Runtime is measured around model fitting and prediction.",
            "",
        ]
        path.write_text("\n".join(lines))
        return str(path)
