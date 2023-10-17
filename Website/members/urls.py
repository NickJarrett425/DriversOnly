from django.urls import path
from .import views

urlpatterns = [
    path('', views.login_user, name="login"),
    path('logout_user/', views.logout_user, name="logout"),
    path('register_user/', views.register_user, name="register_user"),

    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),


    path('admin_profile/', views.view_profile, name='view_admin_profile'),
    path('admin_profile/edit/', views.edit_profile, name='edit_admin_profile'),
    # Keeping Driver Profile separate for now
    path('driver_profile/', views.view_driver_profile, name='view_driver_profile'),
    path('driver_profile/edit/', views.edit_driver_profile, name='edit_driver_profile'),
]