from anomaly.models import AnomalyResult
from anomaly.models import DetectionHistory
from anomaly.ml.anomaly import detect_anomalies
from anomaly.ml.dataset_analyzer import DatasetAnalyzer
from anomaly.services.analytic_service import AnalyticsService
from anomaly.services.explainability_service import ExplainabilityService
from anomaly.services.report_service import ReportService
from anomaly.services.evaluation_service import EvaluationService
from anomaly.services.feature_engineering_services import FeatureEngineeringService
import numpy as np

class AnomalyService:

    @staticmethod
    def process_anomalies( df, filename=None, model_name="isolation_forest", contamination=0.05, scaler_type="standard" ):

        df = FeatureEngineeringService.generate_features(df)

        dataset_info = DatasetAnalyzer.analyze(df)

        dataset_type = dataset_info["dataset_type"]
        target_column = dataset_info["target_column"]

        detection_result = detect_anomalies(
            df,
            model_name=model_name,
            contamination=contamination,
            scaler_type=scaler_type,
            dataset_name=filename
        )

        if detection_result.get("dataset_type") == "labelled":

            AnomalyService._save_detection_history(
                filename=filename,
                model_name=detection_result["model_name"],
                scaler_type=scaler_type,
                contamination=contamination,
                total_records=len(df),
                anomaly_count=0,
                dataset_type="labelled",
                target_column=target_column,
                model_path=None
            )

            return {
                "dataset_type": "labelled",
                "model_name": detection_result["model_name"],
                "classification_metrics": detection_result["metrics"]
            }


        result_df = detection_result["df"]
        model_path = detection_result["model_path"]

        result_df = AnomalyService._add_anomaly_reasons(result_df)

        total = len(result_df)

        anomalies = len(
            result_df[
                result_df["result"] == "Anomaly"
            ]
        )

        normal = total - anomalies

        evaluation = EvaluationService.evaluate(
            predictions=np.where(
                result_df["result"] == "Anomaly",
                1,
                0
            ),
            scores=result_df["anomaly_score"]
        )

        AnomalyService._save_detection_history(
            filename=filename,
            model_name=model_name,
            scaler_type=scaler_type,
            contamination=contamination,
            total_records=total,
            anomaly_count=anomalies,
            dataset_type=dataset_type,
            target_column=target_column,
            model_path=model_path,
            evaluation=evaluation
        )

        AnomalyResult.objects.create( total=total, normal=normal, anomalies=anomalies )

        scatter_data = result_df[
            [
                "pca_x",
                "pca_y",
                "result",
                "anomaly_score"
            ]
        ].to_dict(orient="records")

        score_data = (result_df["anomaly_score"].fillna(0).tolist() )

        saved_path = ReportService.save_result_dataframe( result_df )

        return {
            "result_df": result_df,
            "scatter_data": scatter_data,
            "score_data": score_data,
            "saved_path": saved_path,
            "total": total,
            "anomalies": anomalies,
            "normal": normal,
            "evaluation": evaluation
        }

    @staticmethod
    def _add_anomaly_reasons(result_df):

        numeric_columns = result_df.select_dtypes( include=["number"] ).columns

        column_stats = ( AnalyticsService.generate_column_stats( result_df, numeric_columns ) )

        result_df["reason"] = ( ExplainabilityService.generate_explanations( result_df, numeric_columns, column_stats ) )

        return result_df

    @staticmethod
    def _save_detection_history(
        filename,
        model_name,
        scaler_type,
        contamination,
        total_records,
        anomaly_count,
        dataset_type,
        target_column,
        model_path=None,
        evaluation=None
    ):

        DetectionHistory.objects.create(
            filename=filename,
            model_name=model_name,
            scaler_type=scaler_type,
            contamination=contamination,
            total_records=total_records,
            anomaly_count=anomaly_count,
            dataset_type=dataset_type,
            target_column=target_column,
            model_path=model_path,
            precision=(
                evaluation.get("precision")
                if evaluation
                else None
            ),
            recall=(
                evaluation.get("recall")
                if evaluation
                else None
            ),
            f1_score=(
                evaluation.get("f1_score")
                if evaluation
                else None
            ),
        )