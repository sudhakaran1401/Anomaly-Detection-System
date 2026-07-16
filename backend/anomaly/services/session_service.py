class SessionService:

    @staticmethod
    def save_anomaly_session(
        request,
        result,
        file_name,
        model_name,
        scaler_type,
        contamination,
    ):

        request.session["result_file"] = result["saved_path"]
        request.session["uploaded_filename"] = file_name
        request.session["model_name"] = model_name
        request.session["scaler_type"] = scaler_type
        request.session["contamination"] = contamination

    @staticmethod
    def build_anomaly_context(result, file_name):

        return {

            "columns": list(result["result_df"].columns),

            "data": result["result_df"].to_dict(
                orient="records"
            ),

            "total": result["total"],

            "anomalies": result["anomalies"],

            "normal": result["normal"],

            "scatter_data": result["scatter_data"],

            "normal_score_data": result["normal_score_data"],

            "anomaly_score_data": result["anomaly_score_data"],

            "score_data": result["score_data"],

            "evaluation": result.get("evaluation"),

            "filename": file_name,
        }