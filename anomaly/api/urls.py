from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ( AnomalyResultViewSet, AnalyzeAPIView )

router = DefaultRouter()

router.register( r"results", AnomalyResultViewSet, basename="results" )

urlpatterns = [

    path("", include(router.urls)),

    path( "analyze/", AnalyzeAPIView.as_view(), name="analyze-api" ),
]