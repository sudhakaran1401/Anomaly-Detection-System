from django.urls import path
from . import views

urlpatterns = [

    path( "download-pdf/", views.download_classification_pdf, name="download_classification_pdf", ),
]