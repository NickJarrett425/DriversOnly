from django.shortcuts import render, redirect
from django.contrib import messages
from members.models import UserProfile, SponsorUserProfile
def dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your dashboard.")
        return redirect('/')
    
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')

    if profile.is_driver or request.user.is_superuser:   
        return render(request, 'dashboard.html', {})
    elif profile.is_sponsor:
        sponsor = SponsorUserProfile.objects.get(user=request.user)
        return render(request, 'dashboard.html', {'sponsor': sponsor})
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')
