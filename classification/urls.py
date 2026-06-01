from anomaly import views
from django.urls import path


urlpatterns = [

    path( "classification/pdf/", views.download_classification_pdf, name="download_classification_pdf" )
]