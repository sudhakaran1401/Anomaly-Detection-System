import time
import tracemalloc

import numpy as np

from anomaly.ml.anomaly_model_factory import AnomalyModelFactory


class PerformanceService:
    """Repeatable local performance benchmark for anomaly models."""

    MODELS = ("isolation_forest", "lof", "one_class_svm", "dbscan")

    @classmethod
    def benchmark(cls, sizes=(100, 500, 1000), random_state=42):
        rng = np.random.default_rng(random_state)
        rows = []

        for size in sizes:
            X = rng.normal(size=(size, 5))
            for model_name in cls.MODELS:
                tracemalloc.start()
                started = time.perf_counter()
                model = AnomalyModelFactory.get_model(
                    model_name,
                    contamination=0.05,
                    n_samples=size,
                )
                model.fit(X)
                elapsed = time.perf_counter() - started
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                rows.append({
                    "dataset_size": size,
                    "model": model_name,
                    "runtime_seconds": round(elapsed, 6),
                    "peak_memory_mb": round(peak / (1024 * 1024), 4),
                })

        return rows
