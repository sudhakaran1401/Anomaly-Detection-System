from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from anomaly.models import AnomalyResult
from anomaly.api.serializer import AnomalyResultSerializer, FileUploadSerializer
from anomaly.services.file_service import FileService
from anomaly.services.anomaly_service import AnomalyService


class AnomalyResultViewSet(ModelViewSet):

    serializer_class = AnomalyResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return ( AnomalyResult.objects.all().order_by("-created_at") )


class AnalyzeAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = FileUploadSerializer( data=request.data )

        if not serializer.is_valid():

            return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )

        file = serializer.validated_data["file"]

        try:

            FileService.validate_csv_file(file)

            df = FileService.read_csv_file(file)

            result = AnomalyService.process_anomalies( df, filename=file.name )

            result_df = result["result_df"]

            return Response({

                "total": result["total"],

                "anomalies": result["anomalies"],

                "normal": result["normal"],

                "columns": list(result_df.columns),

                "data": result_df.to_dict(
                    orient="records"
                )
            })

        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:

            return Response(
                {
                    "error":
                    "Unexpected processing error."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )