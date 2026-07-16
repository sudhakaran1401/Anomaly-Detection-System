from django.urls import path, include

from rest_framework.routers import DefaultRouter

from anomaly.api.views import ( AnomalyResultViewSet, AnalyzeAPIView, DetectionHistoryViewSet, DownloadCSVAPIView, DownloadPDFAPIView )

router = DefaultRouter()

router.register( r"results", AnomalyResultViewSet, basename="results", )

router.register( r"history", DetectionHistoryViewSet, basename="history", )

urlpatterns = [

    path("", include(router.urls)),

    path( "analyze/", AnalyzeAPIView.as_view(), name="analyze-api", ),

    path( "download/csv/", DownloadCSVAPIView.as_view(), name="download-csv", ),

    path( "download/pdf/", DownloadPDFAPIView.as_view(), name="download-pdf", ),

]