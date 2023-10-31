from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Application
from members.models import UserProfile
from .forms import ApplicationForm

def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = ApplicationForm()

    return render(request, 'application_form.html', {'form': form})

def application_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view your profile")
        return redirect('/')
    profile = UserProfile.objects.get(user=request.user)
    if not profile.is_sponsor:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')
    else:
        results = Application.objects.filter(sponsor_name=profile.sponsor_name, is_open=True)
        return render(request, 'application_list.html', {'results': results, 'profile': profile,})

def application_closed(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view your profile")
        return redirect('/')
    profile = UserProfile.objects.get(user=request.user)
    if not profile.is_sponsor:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')
    else:
        results = Application.objects.filter(sponsor_name=profile.sponsor_name, is_open=False)
        return render(request, 'application_closed.html', {'results': results, 'profile': profile,})
    
def application_review(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view your profile")
        return redirect('/')
    profile = UserProfile.objects.get(user=request.user)
    if not profile.is_sponsor:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')
    else:
        app_id = id
        application = Application.objects.get(id=app_id)
        return render(request, 'application_review.html', {'application': application,})

def application_deny(request, id):
    application = Application.objects.get(id=id)
    application.is_open = False
    application.save()
    return redirect('/application/list')
def application_approve(request, id):
    application = Application.objects.get(id=id)
    application.is_approved = True
    application.is_open = False
    application.save()
    return redirect('/application/list')

def success_page(request):
    return render(request, 'success.html')
