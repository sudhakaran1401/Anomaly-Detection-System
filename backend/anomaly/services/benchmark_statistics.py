import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon


class BenchmarkStatistics:
    """Statistical summaries for repeated benchmark runs."""

    METRICS = ("accuracy", "precision", "recall", "f1_score", "specificity")

    @staticmethod
    def summarize(repeated_runs):
        rows = []
        for model, group in repeated_runs.groupby("model"):
            row = {"model": model, "runs": len(group)}
            for metric in BenchmarkStatistics.METRICS:
                values = group[metric].astype(float)
                row[f"{metric}_mean"] = round(float(values.mean()), 4)
                row[f"{metric}_std"] = round(float(values.std(ddof=1)) if len(values) > 1 else 0.0, 4)
                row[f"{metric}_min"] = round(float(values.min()), 4)
                row[f"{metric}_max"] = round(float(values.max()), 4)
            row["runtime_mean_seconds"] = round(float(group["runtime_seconds"].mean()), 6)
            row["runtime_std_seconds"] = round(
                float(group["runtime_seconds"].std(ddof=1)) if len(group) > 1 else 0.0, 6
            )
            rows.append(row)
        return pd.DataFrame(rows)

    @staticmethod
    def friedman_test(repeated_runs, metric="f1_score"):
        pivot = repeated_runs.pivot(index="seed", columns="model", values=metric).dropna()
        if pivot.shape[0] < 2 or pivot.shape[1] < 3:
            return {"statistic": None, "p_value": None, "note": "At least 2 runs and 3 models are required."}
        statistic, p_value = friedmanchisquare(*[pivot[col].to_numpy() for col in pivot.columns])
        return {
            "metric": metric,
            "statistic": round(float(statistic), 6),
            "p_value": round(float(p_value), 6),
            "significant_at_0_05": bool(p_value < 0.05),
        }

    @staticmethod
    def pairwise_wilcoxon(repeated_runs, metric="f1_score"):
        pivot = repeated_runs.pivot(index="seed", columns="model", values=metric).dropna()
        models = list(pivot.columns)
        rows = []
        for i, left in enumerate(models):
            for right in models[i + 1:]:
                try:
                    statistic, p_value = wilcoxon(
                        pivot[left], pivot[right], zero_method="wilcox"
                    )
                    rows.append({
                        "metric": metric,
                        "model_a": left,
                        "model_b": right,
                        "statistic": round(float(statistic), 6),
                        "p_value": round(float(p_value), 6),
                        "significant_at_0_05": bool(p_value < 0.05),
                    })
                except ValueError:
                    rows.append({
                        "metric": metric,
                        "model_a": left,
                        "model_b": right,
                        "statistic": None,
                        "p_value": None,
                        "significant_at_0_05": False,
                    })
        return pd.DataFrame(rows)
