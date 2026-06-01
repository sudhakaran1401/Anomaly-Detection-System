from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
import numpy as np
import pandas as pd

class SupervisedPredictor:

    @staticmethod
    def run( model, X_train, X_test, y_train, y_test ):

        model.fit( X_train, y_train )

        predictions = model.predict( X_test )

        results_df = pd.DataFrame({
            "actual": y_test,
            "predicted": predictions
        })

        results_df["actual"] = results_df["actual"].map({
            0: "Normal",
            1: "Anomaly"
        })

        results_df["predicted"] = results_df["predicted"].map({
            0: "Normal",
            1: "Anomaly"
        })

        results_df["status"] = np.where(
            results_df["actual"] == results_df["predicted"],
            "Correct",
            "Misclassified"
        )

        accuracy = accuracy_score( y_test, predictions )

        precision = precision_score( y_test, predictions, zero_division=0 )

        recall = recall_score( y_test, predictions, zero_division=0 )

        f1 = f1_score( y_test, predictions, zero_division=0 )

        cm = confusion_matrix( y_test, predictions ).tolist()

        TN = cm[0][0]
        FP = cm[0][1]
        FN = cm[1][0]
        TP = cm[1][1]


        dataset_summary = {
            "total_dataset_records": len(X_train) + len(X_test),
            "training_records": len(X_train),
            "testing_records": len(X_test),
        }

        summary = {
            "total_records": TN + FP + FN + TP,
            "normal_records": TN + FP,
            "anomaly_records": TP + FN,
            "detected_anomalies": TP,
            "missed_anomalies": FN,
            "false_alarms": FP
        }

        roc_auc = None

        if hasattr(model, "predict_proba"):

            probabilities = ( model.predict_proba(X_test)[:, 1] )

            roc_auc = roc_auc_score( y_test, probabilities )

        return {

            "accuracy": round( accuracy, 4 ),

            "precision": round( precision, 4 ),

            "recall": round( recall, 4 ),

            "f1": round( f1, 4 ),

            "roc_auc": ( round(roc_auc, 4) if roc_auc is not None else None ),

            "confusion_matrix": cm,

            "summary": summary,

            "dataset_summary": dataset_summary
        }