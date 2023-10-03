from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('ebay-api-data/', views.ebay_api_data, name='ebay_api_data'),
]
