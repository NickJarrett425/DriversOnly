from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Application
from members.models import UserProfile, DriverProfile, SponsorUserProfile, SponsorList
from .forms import ApplicationForm

def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            instance = form.save()
            driver = DriverProfile.objects.get(user=request.user)
            application = Application.objects.get(id = instance.id)
            application.driver = driver
            application.save()
            return redirect('success_page')
    else:
        form = ApplicationForm()

    return render(request, 'application_form.html', {'form': form})

def application_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view driver applications.")
        return redirect('/')
    profile = UserProfile.objects.get(user=request.user)
    if profile.is_sponsor:
        sponsor = SponsorUserProfile.objects.get(user=request.user)
        results = Application.objects.filter(sponsor_name=sponsor.sponsor_name, is_open=True)
        return render(request, 'application_list.html', {'results': results, 'sponsor': sponsor})
    elif request.user.is_superuser:
        results = Application.objects.filter(is_open=True)
        return render(request, 'application_list.html', {'results': results,})    
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')
        

def application_closed(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view driver applications.")
        return redirect('/')
    profile = UserProfile.objects.get(user=request.user)
    if profile.is_sponsor:
        sponsor = SponsorUserProfile.objects.get(user=request.user)
        results = Application.objects.filter(sponsor_name=sponsor.sponsor_name, is_open=False)
        return render(request, 'application_closed.html', {'results': results, 'sponsor': sponsor,})
    elif request.user.is_superuser:
        results = Application.objects.filter(is_open=False)
        return render(request, 'application_closed.html', {'results': results,})
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')
    
def application_review(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to review driver applications")
        return redirect('/')
    profile = UserProfile.objects.get(user=request.user)
    if profile.is_sponsor:
        app_id = id
        application = Application.objects.get(id=app_id)
        return render(request, 'application_review.html', {'application': application,})
    elif request.user.is_superuser:
        app_id = id
        application = Application.objects.get(id=app_id)
        return render(request, 'application_review.html', {'application': application,})
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')

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

    driver = DriverProfile.objects.get(user=application.driver.user)
    sponsor = SponsorList.objects.get(sponsor_name=application.sponsor_name)
    driver.sponsors.add(sponsor)
    driver.save()
    return redirect('/application/list')

def success_page(request):
    return render(request, 'success.html')
