import os
import pandas as pd
import logging
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from anomaly.models import DetectionHistory
from anomaly.services.chart_service import ChartService
from anomaly.services.pdf_service import PdfService
from anomaly.services.session_service import SessionService
from classification.service.pdf_service import PDFService
from .services.file_service import FileService
from .services.anomaly_service import AnomalyService

logger = logging.getLogger("anomaly")

@login_required
def home(request):

    if request.method != "POST" or not request.FILES.get("file"):
        return render(request, "home.html")

    file = request.FILES["file"]

    model_name = request.POST.get("model_name", "isolation_forest")

    contamination = float(request.POST.get("contamination", 0.05))

    scaler_type = request.POST.get("scaler_type", "standard")

    logger.info(f"File upload started: {file.name}")

    try:
        FileService.validate_csv_file(file)

        df = FileService.read_csv_file(file)

        result = AnomalyService.process_anomalies(
            df,
            filename=file.name,
            model_name=model_name,
            contamination=contamination,
            scaler_type=scaler_type,
        )

        logger.info(f"Anomaly detection completed for file: {file.name}")

        if result.get("dataset_type") == "labelled":
            confusion_matrix_chart = ChartService.generate_confusion_matrix(
                result["classification_metrics"]["confusion_matrix"]
            )

            SessionService.save_classification_session(
                request=request,
                file_name=file.name,
                model_name=model_name,
                metrics=result["classification_metrics"],
                confusion_matrix_chart=confusion_matrix_chart,
            )

            return render( request, "classification_result.html",
                          
                SessionService.build_classification_context(
                    result=result,
                    file_name=file.name,
                    model_name=model_name,
                    confusion_matrix_chart=confusion_matrix_chart,
                ),
            )

        SessionService.save_anomaly_session(
            request=request,
            result=result,
            file_name=file.name,
            model_name=model_name,
            scaler_type=scaler_type,
            contamination=contamination,
        )

        return render( request, "result.html", SessionService.build_anomaly_context(result=result, file_name=file.name), )

    except ValueError as e:
        logger.warning(str(e))

        return render(request, "home.html", {"error": str(e)})

    except Exception:
        logger.exception("Unexpected anomaly processing error")

        return render(request, "home.html", {"error": "Unexpected processing error."})


@login_required
def download_csv(request):

    file_path = request.session.get("result_file")

    if not file_path or not os.path.exists(file_path):
        return HttpResponse("No data found")

    df = pd.read_csv(file_path)

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = 'attachment; filename="results.csv"'

    df.to_csv(path_or_buf=response, index=False)

    return response


@login_required
def download_pdf(request):

    return PdfService.generate_anomaly_pdf(request)

@login_required
def history(request):

    history_data = DetectionHistory.objects.order_by("-created_at")[:20]

    return render(request, "history.html", {"history_data": history_data})


@login_required
def dashboard(request):

    return render(request, "result.html")


@login_required
def clear_history(request, id=None):

    if id:
        history = get_object_or_404(DetectionHistory, id=id)

        history.delete()

    else:
        DetectionHistory.objects.filter().delete()

    return redirect("history")


@login_required
def download_classification_pdf(request):

    report = request.session.get("classification_report")

    if not report:
        return redirect("home")

    return PDFService.generate_classification_pdf(report)
