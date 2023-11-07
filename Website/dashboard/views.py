from django.shortcuts import render, redirect
from django.contrib import messages
from members.models import UserProfile, SponsorUserProfile
def dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your dashboard.")
        return redirect('/')
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if profile.is_driver or request.user.is_superuser:   
        return render(request, 'dashboard.html', {})
    elif profile.is_sponsor:
        sponsor = SponsorUserProfile.objects.get(user=request.user)
        return render(request, 'dashboard.html', {'sponsor': sponsor})
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')
