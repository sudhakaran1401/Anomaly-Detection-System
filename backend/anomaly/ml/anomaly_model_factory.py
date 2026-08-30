from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM


class AnomalyModelFactory:

    @staticmethod
    def get_model(model_name, contamination=0.05, **params):
        if not 0 < float(contamination) < 0.5:
            raise ValueError("Contamination must be greater than 0 and less than 0.5.")

        models = {
            "isolation_forest": IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=params.get("n_estimators", 100),
            ),
            "lof": LocalOutlierFactor(
                n_neighbors=max(2, min(int(params.get("n_neighbors", 20)), max(2, int(params.get("n_samples", 3)) - 1))),
                contamination=contamination,
                novelty=True,
            ),
            "svm": OneClassSVM(
                kernel="rbf",
                gamma=params.get("gamma", "auto"),
            ),
            "one_class_svm": OneClassSVM(
                kernel="rbf",
                gamma=params.get("gamma", "auto"),
            ),
            "dbscan": DBSCAN(
                eps=params.get("eps", 0.5),
                min_samples=params.get("min_samples", 5),
            ),
        }

        if model_name not in models:
            available = ", ".join(models.keys())
            raise ValueError(
                f"Unsupported anomaly model '{model_name}'. Available models: {available}"
            )

        return models[model_name]
