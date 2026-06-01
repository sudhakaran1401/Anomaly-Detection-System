from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.tree import DecisionTreeClassifier

class ModelFactory:

    @staticmethod
    def get_model( model_name, contamination=0.05, **params ):

        models = {

            "isolation_forest": IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=params.get( "n_estimators", 100 )
            ),

            "lof": LocalOutlierFactor(
                contamination=contamination,
                novelty=True
            ),

            "svm": OneClassSVM(
                kernel="rbf",
                gamma=params.get( "gamma", "auto" )
            ),

            "dbscan": DBSCAN(
                eps=params.get( "eps", 0.5 ),
                min_samples=params.get( "min_samples", 5 )
            ),

            "random_forest": RandomForestClassifier(
                n_estimators=100,
                random_state=42
            ),

            "logistic_regression": LogisticRegression(
                max_iter=1000
            ),

            "decision_tree": DecisionTreeClassifier(
                random_state=42
            ),

            "xgboost": XGBClassifier( 
                n_estimators=100, 
                learning_rate=0.1, 
                max_depth=5, 
                random_state=42 )
        }

        if model_name not in models:
            raise ValueError(
                f"Unsupported model '{model_name}'. "
                f"Available models: {', '.join(models.keys())}"
            )

        return models[model_name]