from django.urls import path
from .import views
from members.views import UserDelete
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('organization/drivers/list', views.driver_list, name="driver_list"),
    path('organization/view/driver/<int:id>', views.view_driver, name="view_driver"),
    path('organization/edit/driver/<int:id>', views.edit_driver, name="edit_driver"),
    path('organization/edit/driver/<int:id>/points', views.add_points, name="add_points"),
    path('organization/add/sponsor_user', views.add_sponsor_user, name="add_sponsor_user"),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/sponsors/list/', views.sponsor_list, name='sponsors_list'),
    path('profile/sponsors/confirmation/<int:id>', views.leave_sponsor_confirm, name='leave_sponsor_confirm'),
    path('profile/sponsors/leave/<int:id>', views.leave_sponsor, name='leave_sponsor'),
    path('register_user/', views.register_user, name="register_user"),
    path('enter_email/', views.enter_email, name="enter_email"),

    path('deleteUser/', UserDelete.as_view(), name = 'deleteUser'),
    path('organizationUpdate/', views.organizationUpdate, name = 'organizationUpdate'),

    path('OrgCreateEntry/', views.organizationCreateUser.as_view(), name = 'OrgCreateLogin'),
    path('OrganizationInvitation/', views.organizationInvitation.as_view(), name = 'organizationInvitation'),

    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='confirm.html',),name='password_reset_confirm'),
    path('password_reset/', views.PasswordReset.as_view(), name = 'password_reset'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name = 'password_reset_complete'),

    path('Organization_Sponsor_list/', views.Organization_Sponsorlist.as_view(), name = 'Organization_Sponsor_list'),
    path('Organization_Driver_list/', views.Organization_Driverlist.as_view(), name = 'Organization_Driver_list'),
    path('Organization_Profile/', views.OrganizationProfile.as_view(), name = 'OrganizationProfile'),
]