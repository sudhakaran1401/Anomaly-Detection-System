export function getPerformanceInsight(metrics) {
    const accuracy = Number(metrics.accuracy ?? 0);
    const precision = Number(metrics.precision ?? 0);
    const recall = Number(metrics.recall ?? 0);
    const f1 = Number(metrics.f1 ?? 0);
    const rocAuc = Number(metrics.roc_auc ?? 0);

    const average =
        (accuracy + precision + recall + f1 + rocAuc) / 5;

    if (average >= 0.95) {
        return {
            className: "alert-success",
            title: "Excellent Model Performance",
            message:
                "The classifier achieved excellent overall performance. Accuracy, precision, recall, F1-score, and ROC-AUC indicate highly reliable predictions with minimal false positives and false negatives."
        };
    }

    if (average >= 0.85) {
        return {
            className: "alert-success",
            title: "Very Good Model Performance",
            message:
                "The classifier performs very well across all evaluation metrics and is expected to generalize well."
        };
    }

    if (average >= 0.75) {
        return {
            className: "alert-warning",
            title: "Good Model Performance",
            message:
                "The model performs well but additional tuning may further improve prediction quality."
        };
    }

    if (average >= 0.60) {
        return {
            className: "alert-warning",
            title: "Fair Model Performance",
            message:
                "The model is usable but there is room for improvement through better features or tuning."
        };
    }

    return {
        className: "alert-danger",
        title: "Poor Model Performance",
        message:
            "Model performance is below expectations. Consider improving data quality, feature engineering, or hyperparameter tuning."
    };
}