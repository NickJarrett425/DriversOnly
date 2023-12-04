from django.urls import path
from .import views

urlpatterns = [
    path('login_report', views.all_login_attempts, name="login_report"),
    path('login_report/downcsv', views.all_login_attempts_download_csv, name="login_report_download_csv"),
    path('login_report/downpdf', views.all_login_attempts_download_pdf, name="login_report_download_pdf"),
]