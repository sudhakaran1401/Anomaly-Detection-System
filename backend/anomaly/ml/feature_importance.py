import pandas as pd

class FeatureImportanceService:

    @staticmethod
    def get_importance(model, feature_names):

        if not hasattr(model, "feature_importances_"):
            return None

        return pd.DataFrame({

            "feature": feature_names,

            "importance":
            model.feature_importances_

        }).sort_values(
            by="importance",
            ascending=False
        )