import logging

from anomaly.services.pca_service import PCAService
from anomaly.ml.anomaly_model_factory import AnomalyModelFactory
from anomaly.ml.predictor import Predictor
from core.ml.scaler_factory import ScalerFactory
from core.ml.dataset_analyzer import DatasetAnalyzer

logger = logging.getLogger("anomaly")


def detect_anomalies( df, model_name="isolation_forest", contamination=0.05, scaler_type="standard", dataset_name="dataset", ):

    dataset_info = DatasetAnalyzer.analyze(df)

    return run_anomaly_pipeline(
        df=df,
        dataset_info=dataset_info,
        model_name=model_name,
        contamination=contamination,
        scaler_type=scaler_type,
        dataset_name=dataset_name,
    )


def run_anomaly_pipeline( df, dataset_info, model_name, contamination, scaler_type, dataset_name, ):

    result_df = df.copy()

    numeric_df = result_df.select_dtypes(include=["number"]).copy()

    if dataset_info["dataset_type"] == "labelled":
        target_column = dataset_info["target_column"]
        numeric_df = numeric_df.drop(columns=[target_column], errors="ignore")

    if numeric_df.empty:
        result_df["result"] = "Normal"
        return {
            "df": result_df,
            "model_path": None,
        }

    numeric_df = numeric_df.fillna(numeric_df.mean())

    if len(numeric_df) < 2:
        result_df["result"] = "Normal"
        return {
            "df": result_df,
            "model_path": None,
        }

    scaler = ScalerFactory.get_scaler(scaler_type)

    scaled_data = scaler.fit_transform(numeric_df)

    model = AnomalyModelFactory.get_model(
        model_name=model_name,
        contamination=contamination,
    )

    predictions, model_path = Predictor.save_and_predict(
        model,
        scaled_data,
        model_name,
        dataset_name,
    )

    result_df["anomaly_score"] = get_anomaly_scores(
        model,
        scaled_data,
    )

    add_pca_columns(
        result_df,
        scaled_data,
    )

    result_df["result"] = [
        "Anomaly" if prediction == -1 else "Normal"
        for prediction in predictions
    ]

    return {
        "df": result_df,
        "model_path": model_path,
    }


def get_anomaly_scores(model, scaled_data):

    if hasattr(model, "decision_function"):
        try:
            return model.decision_function(scaled_data)
        except Exception as exception:
            logger.warning(str(exception))

    return 0


def add_pca_columns(df, scaled_data):

    reduced_data = PCAService.reduce(scaled_data)

    df["pca_x"] = reduced_data[:, 0]
    df["pca_y"] = reduced_data[:, 1]