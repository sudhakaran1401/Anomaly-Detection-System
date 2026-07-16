from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from classification.api.serializer import ( FileUploadSerializer, ClassificationResultSerializer, )
from classification.models import ClassificationResult
from classification.services.classification_service import ( ClassificationService, )

from classification.services.chart_service import ChartService
from classification.services.pdf_service import PDFService

from core.services.file_service import FileService

class ClassificationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = FileUploadSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        model_name = request.data.get( "model_name", "random_forest", )

        scaler_type = request.data.get( "scaler_type", "standard", )

        try:

            FileService.validate_csv_file(file)

            df = FileService.read_csv_file(file)

            result = ClassificationService.process(
                df=df,
                filename=file.name,
                model_name=model_name,
                scaler_type=scaler_type,
            )

            metrics = result["classification_metrics"]

            chart = ChartService.generate_confusion_matrix( metrics["confusion_matrix"] )

            classification = ClassificationResult.objects.create(

                user=request.user,

                file_name=file.name,

                model_name=result["model_name"],

                target_column="Target",

                accuracy=metrics["accuracy"],

                precision=metrics["precision"],

                recall=metrics["recall"],

                f1_score=metrics["f1"],

                roc_auc=metrics["roc_auc"],

                confusion_matrix=metrics["confusion_matrix"],

                summary=metrics["summary"],

                dataset_summary=metrics["dataset_summary"],

                confusion_matrix_chart=chart,
            )

            return Response(

                {

                    "success": True,

                    "message": "Classification completed successfully.",

                    "result": ClassificationResultSerializer(
                        classification
                    ).data,

                },

                status=status.HTTP_200_OK,

            )

        except Exception as e:

            return Response(

                {

                    "success": False,

                    "message": str(e),

                },

                status=status.HTTP_400_BAD_REQUEST,

            )

class ClassificationResultsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = ClassificationResult.objects.filter( user=request.user )

        serializer = ClassificationResultSerializer( queryset, many=True, )

        return Response(
            {
                "success": True,
                "count": queryset.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ClassificationResultDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        result = get_object_or_404( ClassificationResult, pk=pk, user=request.user, )

        serializer = ClassificationResultSerializer(result)

        return Response(
            {
                "success": True,
                "result": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class DownloadClassificationPDFAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        result = get_object_or_404( ClassificationResult, pk=pk, user=request.user, )

        report = {

            "filename": result.file_name,

            "model_name": result.model_name,

            "metrics": {

                "accuracy": result.accuracy,

                "precision": result.precision,

                "recall": result.recall,

                "f1": result.f1_score,

                "roc_auc": result.roc_auc,

                "confusion_matrix": result.confusion_matrix,

                "summary": result.summary,

                "dataset_summary": result.dataset_summary,

            },

            "confusion_matrix_chart": result.confusion_matrix_chart,

        }

        return PDFService.generate_classification_pdf(report)


class DeleteClassificationResultAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        result = get_object_or_404( ClassificationResult, pk=pk, user=request.user, )

        result.delete()

        return Response(
            {
                "success": True,
                "message": "Classification result deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )