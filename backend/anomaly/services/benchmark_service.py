import time
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor

from anomaly.ml.anomaly_model_factory import AnomalyModelFactory
from anomaly.services.evaluation_service import EvaluationService


@dataclass
class BenchmarkRun:
    model: str
    seed: int
    contamination: float
    threshold: float | None
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    specificity: float
    false_positive_rate: float
    false_negative_rate: float
    true_negative: int
    false_positive: int
    false_negative: int
    true_positive: int
    anomaly_count: int
    runtime_seconds: float


class BenchmarkService:
    """Framework-independent, reproducible anomaly-model benchmarking."""

    SUPPORTED_MODELS = (
        "isolation_forest",
        "lof",
        "one_class_svm",
        "dbscan",
    )

    @staticmethod
    def _prepare(df, target_column):
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' was not found.")

        y = EvaluationService.normalize_labels(df[target_column].to_numpy())
        X = df.drop(columns=[target_column]).select_dtypes(include=["number"]).copy()

        if X.empty:
            raise ValueError("Benchmark dataset must contain numeric feature columns.")

        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.dropna(axis=1, how="all")
        X = X.fillna(X.mean()).fillna(0)

        if X.shape[1] == 0:
            raise ValueError("Benchmark dataset has no usable numeric features.")

        return X.to_numpy(dtype=float), y

    @classmethod
    def _fit_predict(cls, X, model_name, contamination, seed):
        # Factory uses deterministic defaults. Override random_state where supported.
        model = AnomalyModelFactory.get_model(
            model_name=model_name,
            contamination=contamination,
            n_samples=len(X),
        )
        if hasattr(model, "random_state"):
            model.random_state = seed

        scaler = StandardScaler()
        scaled = scaler.fit_transform(X)

        start = time.perf_counter()
        model.fit(scaled)

        if model_name == "lof":
            labels = model.predict(scaled)
        elif model_name == "dbscan":
            labels = model.labels_
        else:
            labels = model.predict(scaled)

        runtime = time.perf_counter() - start

        predictions = (np.asarray(labels) == -1).astype(int)

        # A comparable continuous anomaly score: larger means more anomalous.
        if hasattr(model, "decision_function"):
            raw = np.asarray(model.decision_function(scaled), dtype=float)
            scores = -raw
        elif model_name == "dbscan":
            # DBSCAN has no decision function; use distance to nearest core point
            # when available, otherwise use binary anomaly status.
            if getattr(model, "components_", None) is not None and len(model.components_):
                from sklearn.metrics import pairwise_distances
                distances = pairwise_distances(scaled, model.components_)
                scores = distances.min(axis=1)
            else:
                scores = predictions.astype(float)
        else:
            scores = predictions.astype(float)

        return predictions, scores, runtime

    @classmethod
    def evaluate_model(cls, df, target_column, model_name, contamination=0.05, seed=42):
        X, y_true = cls._prepare(df, target_column)
        predictions, scores, runtime = cls._fit_predict(
            X, model_name, contamination, seed
        )
        metrics = EvaluationService.evaluate_supervised(y_true, predictions)

        return {
            "model": model_name,
            "seed": seed,
            "contamination": contamination,
            "threshold": None,
            **metrics,
            "anomaly_count": int(predictions.sum()),
            "runtime_seconds": round(runtime, 6),
            "scores": scores,
        }

    @classmethod
    def compare_models(
        cls,
        df,
        target_column,
        scaler_type="standard",
        contamination=0.05,
        dataset_name="benchmark.csv",
        seed=42,
    ):
        # scaler_type/dataset_name are retained for API compatibility with v1.
        del scaler_type, dataset_name
        rows = []
        for model_name in cls.SUPPORTED_MODELS:
            result = cls.evaluate_model(
                df, target_column, model_name, contamination, seed
            )
            row = {k: v for k, v in result.items() if k != "scores"}
            rows.append(row)
        return pd.DataFrame(rows)

    @classmethod
    def contamination_experiment(
        cls,
        df,
        target_column,
        contaminations=(0.01, 0.03, 0.05, 0.10, 0.15, 0.20),
        models=None,
        seed=42,
    ):
        models = tuple(models or cls.SUPPORTED_MODELS)
        rows = []
        for contamination in contaminations:
            for model_name in models:
                result = cls.evaluate_model(
                    df, target_column, model_name, contamination, seed
                )
                rows.append({
                    k: v for k, v in result.items() if k != "scores"
                })
        return pd.DataFrame(rows)

    @classmethod
    def threshold_experiment(
        cls,
        df,
        target_column,
        model_name,
        quantiles=(0.90, 0.95, 0.97, 0.99),
        contamination=0.05,
        seed=42,
    ):
        X, y_true = cls._prepare(df, target_column)
        _, scores, runtime = cls._fit_predict(
            X, model_name, contamination, seed
        )

        rows = []
        for quantile in quantiles:
            threshold = float(np.quantile(scores, quantile))
            predictions = (scores >= threshold).astype(int)
            metrics = EvaluationService.evaluate_supervised(y_true, predictions)
            rows.append({
                "model": model_name,
                "seed": seed,
                "contamination": contamination,
                "threshold_quantile": quantile,
                "threshold": round(threshold, 8),
                **metrics,
                "anomaly_count": int(predictions.sum()),
                "runtime_seconds": round(runtime, 6),
            })
        return pd.DataFrame(rows)

    @classmethod
    def ensemble_evaluation(
        cls,
        df,
        target_column,
        models=None,
        contamination=0.05,
        seed=42,
        min_votes=None,
    ):
        X, y_true = cls._prepare(df, target_column)
        models = tuple(models or cls.SUPPORTED_MODELS)

        if "dbscan" in models:
            # DBSCAN has no predict(X) method, so it cannot participate in the
            # project's existing WeightedEnsembleDetector implementation.
            models = tuple(m for m in models if m != "dbscan")

        from anomaly.ml.ensembles.weighted_ensemble import WeightedEnsembleDetector

        model_objects = []
        for model_name in models:
            model = AnomalyModelFactory.get_model(
                model_name=model_name,
                contamination=contamination,
                n_samples=len(X),
            )
            if hasattr(model, "random_state"):
                model.random_state = seed
            model_objects.append(model)

        scaler = StandardScaler()
        scaled = scaler.fit_transform(X)

        weights = np.ones(len(model_objects), dtype=float) / len(model_objects)
        threshold = 0.5 if min_votes is None else min_votes / len(model_objects)

        start = time.perf_counter()
        ensemble = WeightedEnsembleDetector(
            models=model_objects,
            weights=weights.tolist(),
            threshold=threshold,
        )
        ensemble.fit(scaled)
        ensemble_predictions = ensemble.predict(scaled)
        runtime = time.perf_counter() - start

        metrics = EvaluationService.evaluate_supervised(
            y_true, ensemble_predictions
        )
        return {
            "model": "weighted_ensemble",
            "models": list(models),
            "weights": weights.tolist(),
            "seed": seed,
            "contamination": contamination,
            "threshold": threshold,
            **metrics,
            "anomaly_count": int(ensemble_predictions.sum()),
            "runtime_seconds": round(runtime, 6),
        }

    @classmethod
    def repeated_runs(
        cls,
        df,
        target_column,
        seeds=(7, 21, 42, 84, 168),
        contamination=0.05,
        models=None,
    ):
        models = tuple(models or cls.SUPPORTED_MODELS)
        rows = []
        for seed in seeds:
            for model_name in models:
                result = cls.evaluate_model(
                    df, target_column, model_name, contamination, seed
                )
                rows.append({
                    k: v for k, v in result.items() if k != "scores"
                })
        return pd.DataFrame(rows)
