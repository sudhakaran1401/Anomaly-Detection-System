from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM


class AnomalyModelFactory:

    @staticmethod
    def get_model(model_name, contamination=0.05, **params):

        models = {

            "isolation_forest": IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=params.get("n_estimators", 100),
            ),

            "lof": LocalOutlierFactor(
                contamination=contamination,
                novelty=True,
            ),

            "svm": OneClassSVM(
                kernel="rbf",
                gamma=params.get("gamma", "auto"),
            ),

            "dbscan": DBSCAN(
                eps=params.get("eps", 0.5),
                min_samples=params.get("min_samples", 5),
            ),
        }

        if model_name not in models:
            raise ValueError(
                f"Unsupported anomaly model '{model_name}'. "
                f"Available models: {', '.join(models.keys())}"
            )

        return models[model_name]