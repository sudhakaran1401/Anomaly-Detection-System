from django.urls import path

from classification.api.views import (
    ClassificationAPIView,
    ClassificationResultsAPIView,
    ClassificationResultDetailAPIView,
    DownloadClassificationPDFAPIView,
    DeleteClassificationResultAPIView,
)

app_name = "classification"

urlpatterns = [

    path( "classify/", ClassificationAPIView.as_view(), ),
    
    path( "results/", ClassificationResultsAPIView.as_view(), ),

    path( "results/<int:pk>/", ClassificationResultDetailAPIView.as_view(), ),

    path( "results/<int:pk>/download/pdf/", DownloadClassificationPDFAPIView.as_view(), ),

    path( "results/<int:pk>/delete/", DeleteClassificationResultAPIView.as_view(), ),
]