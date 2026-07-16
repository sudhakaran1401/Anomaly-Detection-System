from sklearn.model_selection import train_test_split

from core.ml.dataset_analyzer import DatasetAnalyzer
from core.ml.scaler_factory import ScalerFactory

from classification.ml.classification_model_factory import ClassificationModelFactory
from classification.ml.supervised_predictor import SupervisedPredictor


def classify_dataset(df, model_name, scaler_type="standard"):
    dataset_info = DatasetAnalyzer.analyze(df)

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

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = ClassificationModelFactory.get_model(model_name)

    metrics = SupervisedPredictor.run(
        model,
        X_train,
        X_test,
        y_train,
        y_test,
    )

    return {
        "dataset_type": "labelled",
        "model_name": model_name,
        "metrics": metrics,
    }


def remove_leakage_columns(X, target_column):
    leakage_columns = [
        column
        for column in X.columns
        if target_column.lower() in column.lower()
    ]

    return X.drop(columns=leakage_columns, errors="ignore")