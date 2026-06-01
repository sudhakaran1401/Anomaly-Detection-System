import logging
from sklearn.model_selection import train_test_split
from anomaly.constants import SUPERVISED_MODELS, ANOMALY_MODELS
from anomaly.services.pca_service import PCAService
from anomaly.ml.model_factory import ModelFactory
from anomaly.ml.predictor import Predictor
from anomaly.ml.scaler_factory import ScalerFactory
from anomaly.ml.dataset_analyzer import DatasetAnalyzer
from anomaly.ml.supervised_predictor import SupervisedPredictor


logger = logging.getLogger("anomaly")

def detect_anomalies( df, model_name="isolation_forest", contamination=0.05, scaler_type="standard", dataset_name="dataset"):

    dataset_info = DatasetAnalyzer.analyze(df)

    if model_name in SUPERVISED_MODELS:

        return run_supervised_pipeline(
            df=df,
            dataset_info=dataset_info,
            model_name=model_name,
            scaler_type=scaler_type,
        )

    return run_anomaly_pipeline(
        df=df,
        dataset_info=dataset_info,
        model_name=model_name,
        contamination=contamination,
        scaler_type=scaler_type,
        dataset_name=dataset_name,
    )


# ==================================================
# SUPERVISED PIPELINE
# ==================================================


def run_supervised_pipeline(df, dataset_info, model_name, scaler_type):

    if dataset_info["dataset_type"] != "labelled":
        raise ValueError(f"{model_name} requires a labelled dataset.")

    numeric_df = df.select_dtypes(include=["number"]).copy()

    target_column = dataset_info["target_column"]

    y = df[target_column]

    X = numeric_df.drop(columns=[target_column], errors="ignore")

    X = remove_leakage_columns(X, target_column)

    if X.empty:
        raise ValueError("No numeric features available for training.")

    scaler = ScalerFactory.get_scaler(scaler_type)

    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split( X_scaled, y, test_size=0.2, random_state=42 )

    model = ModelFactory.get_model(model_name)

    result = SupervisedPredictor.run(model, X_train, X_test, y_train, y_test)

    return {"dataset_type": "labelled", "model_name": model_name, "metrics": result}


# ==================================================
# ANOMALY PIPELINE
# ==================================================


def run_anomaly_pipeline( df, dataset_info, model_name, contamination, scaler_type, dataset_name ):

    result_df = df.copy()

    numeric_df = result_df.select_dtypes(include=["number"]).copy()

    if dataset_info["dataset_type"] == "labelled":
        target_column = dataset_info["target_column"]

        numeric_df = numeric_df.drop(columns=[target_column], errors="ignore")

    if numeric_df.empty:
        result_df["result"] = "Normal"

        return {"df": result_df, "model_path": None}

    numeric_df = numeric_df.fillna(numeric_df.mean())

    if len(numeric_df) < 2:
        result_df["result"] = "Normal"

        return {"df": result_df, "model_path": None}

    scaler = ScalerFactory.get_scaler(scaler_type)

    scaled_data = scaler.fit_transform(numeric_df)

    model = ModelFactory.get_model(model_name=model_name, contamination=contamination)

    predictions, model_path = Predictor.save_and_predict( model, scaled_data, model_name, dataset_name )

    result_df["anomaly_score"] = get_anomaly_scores(model, scaled_data)

    add_pca_columns(result_df, scaled_data)

    result_df["result"] = [
        "Anomaly" if pred == -1 else "Normal" for pred in predictions
    ]

    return {"df": result_df, "model_path": model_path}


# ==================================================
# HELPERS
# ==================================================


def remove_leakage_columns(X, target_column):
    leakage_columns = [col for col in X.columns if target_column.lower() in col.lower()]

    logger.info( "Leakage columns removed: %s", leakage_columns )

    return X.drop(columns=leakage_columns, errors="ignore")


def get_anomaly_scores(model, scaled_data):
    scores = 0

    if hasattr(model, "decision_function"):
        try:
            scores = model.decision_function(scaled_data)
        except Exception as e:
            logger.warning(str(e))
    return scores


def add_pca_columns(df, scaled_data):
    reduced_data = PCAService.reduce(scaled_data)

    df["pca_x"] = reduced_data[:, 0]
    df["pca_y"] = reduced_data[:, 1]
