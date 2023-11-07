from django.urls import path
from .import views

urlpatterns = [
    path('', views.login_user, name="login"),
    path('logout_user/', views.logout_user, name="logout"),
    path('register_user/', views.register_user, name="register_user"),
    path('organization/drivers/list/', views.driver_list, name="driver_list"),
    path('organization/view/driver/<int:id>/', views.view_driver, name="view_driver"),
    path('organization/edit/driver/<int:id>/', views.edit_driver, name="edit_driver"),
    path('organization/add/sponsor_user', views.add_sponsor_user, name="add_sponsor_user"),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]