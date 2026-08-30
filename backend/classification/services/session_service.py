class SessionService:

    @staticmethod
    def save_classification_session( request, file_name, model_name, metrics, confusion_matrix_chart, ):

        request.session["classification_report"] = {

            "filename": file_name,

            "model_name": model_name,

            "metrics": metrics,

            "confusion_matrix_chart": confusion_matrix_chart,
        }

    @staticmethod
    def build_classification_context( result, file_name, model_name, confusion_matrix_chart, ):

        return {

            "metrics": result["classification_metrics"],

            "filename": file_name,

            "model_name": model_name,

            "dataset_type": result["dataset_type"],

            "confusion_matrix_chart": confusion_matrix_chart,
        }