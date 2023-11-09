from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('orgUpdate/', orgCreate.as_view(), name='orgCreate'),
    path('createConfirm', createConfirm.as_view(), name = 'createConfirm'),
]
