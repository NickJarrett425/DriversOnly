from members.models import UserProfile, DriverProfile
from django.contrib import messages
from django.shortcuts import redirect


def navbar_points(request):
    if not request.user.is_authenticated:
        return {}
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if profile.is_driver:
        try:
            driver = DriverProfile.objects.get(user=request.user)
            points = driver.points
            return {'profile': profile, 'points': points}
        except DriverProfile.DoesNotExist:
            None
    
    return {'profile': profile}