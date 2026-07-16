from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier


class ClassificationModelFactory:

    @staticmethod
    def get_model(model_name):

        models = {

            "random_forest": RandomForestClassifier(
                n_estimators=100,
                random_state=42,
            ),

            "decision_tree": DecisionTreeClassifier(
                random_state=42,
            ),

            "logistic_regression": LogisticRegression(
                max_iter=1000,
            ),

            "xgboost": XGBClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42,
            ),
        }

        if model_name not in models:
            raise ValueError(f"Unsupported classification model: {model_name}")

        return models[model_name]