from django.urls import path
from . import views

urlpatterns = [
    # Path Converters
    # int: numbers
    # str: strings
    # path: whole urls /
    # slug: hyphen-and_underscores_stuff
    # UUID: universally unique identifer (usernames & such)

    path('', views.application_form, name='application_form'),
    path('list/', views.application_list, name='application_list'),
    path('list/closed', views.application_closed, name='application_closed'),
    path('review/<int:id>/', views.application_review, name='application_review'),
    path('review/<int:id>/edit', views.application_edit, name='application_edit'),
    path('review/<int:id>/deny/', views.application_deny, name='application_deny'),
    path('review/<int:id>/approve/', views.application_approve, name='application_approve'),
    path('review/<int:id>/waitlist/', views.application_waitlist, name='application_waitlist'),
    path('success/', views.success_page, name='success_page'),
]