from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages

import logging
from django.contrib.auth.decorators import login_required
from anomaly.services.anomaly_service import AnomalyService
from core.services.file_service import FileService
from anomaly.services.session_service import SessionService
from anomaly.constants import SUPERVISED_MODELS, ANOMALY_MODELS
from core.ml.dataset_analyzer import DatasetAnalyzer
from classification.services.classification_service import ClassificationService
from classification.services.chart_service import ChartService
from classification.services.session_service import SessionService as ClassificationSessionService

logger = logging.getLogger("anomaly")

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(

            request,

            username=username,

            password=password
        )

        if user:

            login(request, user)

            return redirect("home")

        messages.error( request, "Invalid credentials" )

    return render( request, "registration/login.html" )

def logout_view(request):

    logout(request)

    return redirect("login")

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

        # ============================================
        # CLASSIFICATION MODELS
        # ============================================

        if model_name in SUPERVISED_MODELS:

            dataset_info = DatasetAnalyzer.analyze(df)

            if dataset_info["dataset_type"] != "labelled":
                raise ValueError(
                    f"{model_name} requires a labelled dataset."
                )

            result = ClassificationService.process(
                df=df,
                filename=file.name,
                model_name=model_name,
                scaler_type=scaler_type,
            )

            confusion_matrix_chart = (
                ChartService.generate_confusion_matrix(
                    result["classification_metrics"]["confusion_matrix"]
                )
            )

            ClassificationSessionService.save_classification_session(
                request=request,
                file_name=file.name,
                model_name=model_name,
                metrics=result["classification_metrics"],
                confusion_matrix_chart=confusion_matrix_chart,
            )

            return render(
                request,
                "classification_result.html",
                ClassificationSessionService.build_classification_context(
                    result=result,
                    file_name=file.name,
                    model_name=model_name,
                    confusion_matrix_chart=confusion_matrix_chart,
                ),
            )

        # ============================================
        # ANOMALY MODELS
        # ============================================

        elif model_name in ANOMALY_MODELS:

            result = AnomalyService.process_anomalies(
                df=df,
                filename=file.name,
                model_name=model_name,
                contamination=contamination,
                scaler_type=scaler_type,
            )

            SessionService.save_anomaly_session(
                request=request,
                result=result,
                file_name=file.name,
                model_name=model_name,
                scaler_type=scaler_type,
                contamination=contamination,
            )

            return render(
                request,
                "result.html",
                SessionService.build_anomaly_context(
                    result=result,
                    file_name=file.name,
                ),
            )

        else:
            raise ValueError("Invalid model selected.")

    except ValueError as e:

        logger.warning(str(e))

        return render(
            request,
            "home.html",
            {
                "error": str(e)
            }
        )

    except Exception:

        logger.exception("Unexpected processing error")

        return render(
            request,
            "home.html",
            {
                "error": "Unexpected processing error."
            }
        )