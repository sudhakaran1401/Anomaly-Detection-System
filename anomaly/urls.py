from django.urls import path
from . import views


urlpatterns = [

    path( "upload/", views.home, name="home"),

    path( "result/", views.dashboard, name="dashboard"),

    path( "download-csv/", views.download_csv, name="download_csv"),

    path( "download-pdf/", views.download_pdf, name="download_pdf"),

    path( "history/", views.history, name="history"),

    path( 'history/clear-all/', views.clear_history, name='clear_all_history' ),

    path( 'history/clear/<int:id>/', views.clear_history, name='clear_history' ),


]