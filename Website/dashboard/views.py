from django.shortcuts import render, redirect
from django.contrib import messages
from members.models import UserProfile
def dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your dashboard.")
        return redirect('/')
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if profile.is_driver:   
        return render(request, 'dashboard.html', {})
    else:
        messages.error(request, "Sorry, you are not authorized to access this page.")
        return redirect('/about')
