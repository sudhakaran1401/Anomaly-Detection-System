class SessionService:
     
    @staticmethod
    def save_classification_session( request, file_name, model_name, metrics, confusion_matrix_chart ):

        request.session["classification_report"] = {
            "filename": file_name,
            "model_name": model_name,
            "metrics": metrics,
            "confusion_matrix_chart": confusion_matrix_chart,
        }

    @staticmethod
    def save_anomaly_session( request, result, file_name, model_name, scaler_type, contamination ):

        request.session["result_file"] = result["saved_path"]
        request.session["uploaded_filename"] = file_name
        request.session["model_name"] = model_name
        request.session["scaler_type"] = scaler_type
        request.session["contamination"] = contamination

    @staticmethod

    def build_classification_context(result, file_name, model_name, confusion_matrix_chart):

        return {
            "metrics": result["classification_metrics"],
            "filename": file_name,
            "confusion_matrix_chart": confusion_matrix_chart,
            "model_name": model_name,
        }


    @staticmethod
    def build_anomaly_context(result, file_name):

        return {
            "columns": list(result["result_df"].columns),
            "data": result["result_df"].to_dict(orient="records"),
            "total": result["total"],
            "anomalies": result["anomalies"],
            "normal": result["normal"],
            "scatter_data": result["scatter_data"],
            "score_data": result["score_data"],
            "evaluation": result.get("evaluation"),
            "filename": file_name,
        }