import os

from django.conf import settings
from django.http import HttpResponse

import pandas as pd

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import ( OpenApiExample, extend_schema, )

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from anomaly.api.serializer import ( AnomalyResultSerializer, DetectionHistorySerializer, FileUploadSerializer, )
from anomaly.models import ( AnomalyResult, DetectionHistory, )

from anomaly.services.anomaly_service import AnomalyService
from anomaly.services.pdf_service import PdfService
from anomaly.services.pseudo_label_service import PseudoLabelService
from anomaly.services.session_service import SessionService

from core.services.file_service import FileService


class AnomalyResultViewSet(ModelViewSet):
    """
    API for viewing and managing anomaly detection results.
    """

    serializer_class = AnomalyResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AnomalyResult.objects.all().order_by("-created_at")


class AnalyzeAPIView(GenericAPIView):
    """
    Upload a CSV file and perform anomaly detection.
    """

    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = ( MultiPartParser, FormParser, )

    @extend_schema(
        summary="Analyze CSV Dataset",
        description="Upload a CSV dataset and perform anomaly detection.",
        request=FileUploadSerializer,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Successful Response",
                value={
                    "success": True,
                    "message": "Anomaly detection completed successfully.",
                    "data": {
                        "filename": "sales.csv",
                        "total": 1000,
                        "anomalies": 32,
                        "normal": 968,
                    },
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        file = serializer.validated_data["file"]

        try:
            FileService.validate_csv_file(file)

            df = FileService.read_csv_file(file)

            model_name = request.data.get( "model_name", "isolation_forest", )

            scaler_type = request.data.get( "scaler_type", "standard", )

            contamination = float( request.data.get( "contamination", 0.05, ) )

            result = AnomalyService.process_anomalies(
                df=df,
                filename=file.name,
                model_name=model_name,
                scaler_type=scaler_type,
                contamination=contamination,
            )

            SessionService.save_anomaly_session(
                request=request,
                result=result,
                file_name=file.name,
                model_name=model_name,
                scaler_type=scaler_type,
                contamination=contamination,
            )

            context = SessionService.build_anomaly_context( result=result, file_name=file.name, )

            return Response(
                {
                    "success": True,
                    "message": "Anomaly detection completed successfully.",
                    "data": context,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print(e)

            return Response(
                {
                    "success": False,
                    "message": "Unexpected processing error.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DetectionHistoryViewSet(viewsets.ModelViewSet):
    queryset = DetectionHistory.objects.all().order_by("-created_at")

    serializer_class = DetectionHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    @action( detail=False, methods=["delete"], url_path="clear", )

    def clear(self, request):

        deleted_count, _ = self.get_queryset().delete()

        return Response(
            {
                "success": True,
                "message": (f"{deleted_count} history record(s) deleted successfully."),
            },
            status=status.HTTP_200_OK,
        )


class DownloadCSVAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        results_dir = os.path.join( settings.MEDIA_ROOT, "results", )

        if not os.path.exists(results_dir):
            return HttpResponse( "Results folder not found.", status=404, )

        csv_files = [
            os.path.join(results_dir, file)
            for file in os.listdir(results_dir)
            if file.endswith(".csv")
        ]

        if not csv_files:
            return HttpResponse( "No processed files found.", status=404, )

        latest_file = max( csv_files, key=os.path.getmtime, )

        df = pd.read_csv(latest_file)

        df = PseudoLabelService.generate(df)

        filename = os.path.basename(latest_file)

        response = HttpResponse( content_type="text/csv", )

        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        df.to_csv( response, index=False, )

        return response


class DownloadPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        results_dir = os.path.join( settings.MEDIA_ROOT, "results", )

        if not os.path.exists(results_dir):
            return HttpResponse( "Results folder not found.", status=404, )

        csv_files = [
            os.path.join(results_dir, file)
            for file in os.listdir(results_dir)
            if file.endswith(".csv")
        ]

        if not csv_files:
            return HttpResponse( "No processed files found.", status=404, )

        latest_file = max( csv_files, key=os.path.getmtime, )

        request.session["result_file"] = latest_file

        metadata = {
            "uploaded_filename": request.GET.get( "filename", "Unknown", ),

            "model_name": request.GET.get( "model_name", "Unknown", ),

            "scaler_type": request.GET.get( "scaler_type", "Unknown", ),

            "contamination": request.GET.get( "contamination", "N/A", ),
        }

        return PdfService.generate_anomaly_pdf( request=request, metadata=metadata, )
