from members.models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from report.models import login_log
from django.core.mail import send_mail
from django.conf import settings

# def navbar_points(request):
#     if not request.user.is_authenticated:
#         return {}
    
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
    
#     if profile.is_driver:
#         try:
#             driver = DriverProfile.objects.get(user=request.user)
#             # points = driver.points
#             return {'profile': profile,}
#         except DriverProfile.DoesNotExist:
#             None
    
#     return {'profile': profile}

def current_sponsor(request):
    if not request.user.is_authenticated:
        return {}
    
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if profile.is_driver:
        try:
            driver = DriverProfile.objects.get(user=request.user)
        except DriverProfile.DoesNotExist:
            pass
        sponsor_id = driver.selected_sponsor_id
        sponsor = SponsorList.objects.get(id=sponsor_id)
        sponsor_name = sponsor.sponsor_name
        return {'profile': profile, 'sponsor_name': sponsor_name, 'driver': driver}
    
    return {'profile': profile}