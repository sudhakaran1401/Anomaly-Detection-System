from anomaly.models import DetectionHistory
from core.ml.dataset_analyzer import DatasetAnalyzer
from core.services.feature_engineering_services import FeatureEngineeringService
from classification.ml.classification import classify_dataset


class ClassificationService:

    @staticmethod
    def _save_classification_history( filename, model_name, scaler_type, total_records, target_column, metrics, ):

        DetectionHistory.objects.create(
            filename=filename,
            model_name=model_name,
            scaler_type=scaler_type,
            contamination=None,
            total_records=total_records,
            anomaly_count=0,
            dataset_type="labelled",
            target_column=target_column,
            precision=metrics.get("precision"),
            recall=metrics.get("recall"),
            f1_score=metrics.get("f1_score"),
        )

    @staticmethod
    def process( df, filename=None, model_name="random_forest", scaler_type="standard", ):

        df = FeatureEngineeringService.generate_features(df)

        dataset_info = DatasetAnalyzer.analyze(df)

        if dataset_info["dataset_type"] != "labelled":
            raise ValueError("Classification requires a labelled dataset.")

        result = classify_dataset(
            df=df,
            model_name=model_name,
            scaler_type=scaler_type,
        )

        ClassificationService._save_classification_history(
        filename=filename,
        model_name=model_name,
        scaler_type=scaler_type,
        total_records=len(df),
        target_column=dataset_info["target_column"],
        metrics=result["metrics"],
        )

        return {
            "dataset_type": "labelled",
            "model_name": result["model_name"],
            "classification_metrics": result["metrics"],
        }
    
    