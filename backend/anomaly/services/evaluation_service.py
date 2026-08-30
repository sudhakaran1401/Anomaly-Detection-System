import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


class EvaluationService:

    @staticmethod
    def evaluate(predictions, scores=None, y_true=None):
        """Return basic detection statistics and optional supervised metrics.

        Predictions use the project's convention: 1 = anomaly, 0 = normal.
        If ground-truth labels are supplied, precision/recall/F1/accuracy and
        a confusion matrix are calculated. Unlabelled datasets only receive
        descriptive anomaly statistics.
        """
        predictions = np.asarray(predictions)
        anomaly_count = int(np.sum(predictions == 1))
        total_records = len(predictions)

        results = {
            "total_records": total_records,
            "anomaly_count": anomaly_count,
            "anomaly_percentage": (
                round(anomaly_count / total_records * 100, 2)
                if total_records
                else 0.0
            ),
        }

        if scores is not None:
            scores = np.asarray(scores, dtype=float)
            finite_scores = scores[np.isfinite(scores)]
            if finite_scores.size:
                results["average_score"] = round(float(np.mean(finite_scores)), 4)
                results["lowest_score"] = round(float(np.min(finite_scores)), 4)

        if y_true is not None:
            supervised = EvaluationService.evaluate_supervised(
                y_true=y_true,
                predictions=predictions,
            )
            results.update(supervised)

        return results

    @staticmethod
    def evaluate_supervised(y_true, predictions):
        """Calculate classification-style metrics for labelled anomaly data.

        Ground truth is normalized to the project's convention: 1 = anomaly,
        0 = normal. Labels may be numeric (0/1) or common textual values.
        """
        true_labels = EvaluationService.normalize_labels(y_true)
        predicted_labels = np.asarray(predictions).astype(int)

        if len(true_labels) != len(predicted_labels):
            raise ValueError("Ground-truth labels and predictions must have the same length.")

        if len(true_labels) == 0:
            raise ValueError("Ground-truth labels cannot be empty.")

        accuracy = accuracy_score(true_labels, predicted_labels)
        precision = precision_score(
            true_labels, predicted_labels, zero_division=0
        )
        recall = recall_score(
            true_labels, predicted_labels, zero_division=0
        )
        f1 = f1_score(
            true_labels, predicted_labels, zero_division=0
        )

        tn, fp, fn, tp = confusion_matrix(
            true_labels,
            predicted_labels,
            labels=[0, 1],
        ).ravel()

        specificity = tn / (tn + fp) if (tn + fp) else 0.0

        return {
            "accuracy": round(float(accuracy), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
            "specificity": round(float(specificity), 4),
            "false_positive_rate": round(
                float(fp / (fp + tn)) if (fp + tn) else 0.0, 4
            ),
            "false_negative_rate": round(
                float(fn / (fn + tp)) if (fn + tp) else 0.0, 4
            ),
            "confusion_matrix": {
                "true_negative": int(tn),
                "false_positive": int(fp),
                "false_negative": int(fn),
                "true_positive": int(tp),
            },
        }

    @staticmethod
    def normalize_labels(labels):
        """Normalize common anomaly labels to 0 (normal) and 1 (anomaly)."""
        values = np.asarray(labels)

        normalized = []
        anomaly_values = {
            "1", "true", "yes", "y", "anomaly", "anomalous",
            "outlier", "fraud", "attack", "abnormal"
        }
        normal_values = {
            "0", "false", "no", "n", "normal", "inlier", "legitimate"
        }

        for value in values:
            if pd_isna(value):
                raise ValueError("Ground-truth labels contain missing values.")

            if isinstance(value, (bool, np.bool_)):
                normalized.append(int(value))
                continue

            if isinstance(value, (int, np.integer, float, np.floating)):
                if value in (0, 1):
                    normalized.append(int(value))
                    continue
                raise ValueError(
                    "Ground-truth numeric labels must contain only 0 and 1."
                )

            text = str(value).strip().lower()
            if text in anomaly_values:
                normalized.append(1)
            elif text in normal_values:
                normalized.append(0)
            else:
                raise ValueError(
                    f"Unsupported ground-truth label value: {value}"
                )

        return np.asarray(normalized, dtype=int)


def pd_isna(value):
    """Small dependency-free missing-value check for scalar labels."""
    try:
        return bool(np.isnan(value))
    except (TypeError, ValueError):
        return False
