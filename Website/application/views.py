from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Application
from members.models import UserProfile, DriverProfile, SponsorUserProfile, SponsorList
from .forms import ApplicationForm, ApplicatonReasonForm

def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            driver = get_object_or_404(DriverProfile, user=request.user)
            instance.driver = driver
            instance.save()
            return redirect('/application/success')
    else:
        form = ApplicationForm()

    return render(request, 'application_form.html', {'form': form})

def success_page(request):
    return render(request, 'success.html')

def application_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view driver applications.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    if profile.is_driver:
        driver = DriverProfile.objects.get(user=request.user)
        results = Application.objects.filter(driver=driver, is_open=True)
        return render(request, 'application_list.html', {'results': results, 'profile': profile,})
    elif profile.is_sponsor:
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
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    if profile.is_driver:
        driver = DriverProfile.objects.get(user=request.user)
        results = Application.objects.filter(driver=driver, is_open=False)
        return render(request, 'application_closed.html', {'results': results, 'profile': profile,})
    elif profile.is_sponsor:
        sponsor = SponsorUserProfile.objects.get(user=request.user)
        results = Application.objects.filter(sponsor_name=sponsor.sponsor_name, is_open=False)
        return render(request, 'application_closed.html', {'results': results, 'profile': profile, 'sponsor': sponsor,})
    elif request.user.is_superuser:
        results = Application.objects.filter(is_open=False)
        return render(request, 'application_closed.html', {'results': results,})
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/application/list')

def application_review(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to review driver applications")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    if profile.is_driver:
        driver = DriverProfile.objects.get(user=request.user)
        app_id = id

        application = Application.objects.get(id=app_id)
        if application.driver != driver:
            messages.error(request, "You do not have the proper permissions to access this page.")
            if application.is_open:
                return redirect('/application/list')
            else:
                return redirect('/application/list/closed')
        else:
            return render(request, 'application_review.html', {'application': application, 'profile': profile,})
    if profile.is_sponsor:
        app_id = id
        application = Application.objects.get(id=app_id)
        return render(request, 'application_review.html', {'application': application, 'profile': profile,})
    elif request.user.is_superuser:
        app_id = id
        application = Application.objects.get(id=app_id)
        return render(request, 'application_review.html', {'application': application,})
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')

def application_deny(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to review driver applications")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    application = Application.objects.get(id=id)
    if not application.is_open and not request.user.is_superuser and not profile.is_driver:
        messages.success(request, "Unable to deny application, applicaton is already closed.")
        return redirect('/application/review/'+str(id))
    
    if request.user.is_superuser:
        application.is_open = False
        if request.method == 'POST':
            form = ApplicatonReasonForm(request.POST)

            if form.is_valid():
                application.application_reason = form.cleaned_data['application_reason']
                application.is_approved = False
                application.save()
                if request.user.is_superuser:
                    driver = DriverProfile.objects.get(user=application.driver.user)
                    sponsor = SponsorList.objects.get(sponsor_name=application.sponsor_name)
                    driver.sponsors.remove(sponsor)
                    driver.save()
                messages.success(request, "Application successfully denied")
                return redirect('/application/list')
        else:
            form = ApplicatonReasonForm()
    elif profile.is_sponsor:
        sponsor = SponsorUserProfile.objects.get(user=request.user)
        if sponsor.sponsor_name == application.sponsor_name:
            application.is_open = False
            if request.method == 'POST':
                form = ApplicatonReasonForm(request.POST)

                if form.is_valid():
                    application.application_reason = form.cleaned_data['application_reason']
                    application.is_approved = False
                    application.save()
                    if request.user.is_superuser:
                        driver = DriverProfile.objects.get(user=application.driver.user)
                        sponsor = SponsorList.objects.get(sponsor_name=application.sponsor_name)
                        driver.sponsors.remove(sponsor)
                        driver.save()
                    messages.success(request, "Application successfully denied")
                    return redirect('/application/list')
            else:
                form = ApplicatonReasonForm()
        else:
            messages.success(request, "Application is not for your sponsor organization")
            return redirect('/application/list')
    else:
        return redirect('/application/review/'+str(id))
    return render (request, 'application_reason.html', {'application': application, 'form': form})

def application_approve(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to review driver applications")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    application = Application.objects.get(id=id)
    if not application.is_open and not request.user.is_superuser:
        messages.success(request, "Unable to approve application, applicaton is already closed.")
        return redirect('/application/review/'+str(id))
    if profile.is_sponsor or request.user.is_superuser:
        application.is_approved = True
        application.is_open = False
        application.application_reason = ""
        application.save()

        driver = DriverProfile.objects.get(user=application.driver.user)
        sponsor = SponsorList.objects.get(sponsor_name=application.sponsor_name)
        driver.sponsors.add(sponsor)
        driver.save()
    elif not request.user.is_superuser:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/application/review/'+str(id))
    return redirect('/application/list')

def application_waitlist(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to review driver applications")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    application = Application.objects.get(id=id)
    profile = UserProfile.objects.get(user=request.user)
    if profile.is_sponsor or request.user.is_superuser:
        application.is_waitlisted = True
        application.is_open = True
        application.is_approved = False
        application.application_reason = "We are currently putting your application on waitlist."
        application.save()
        
        messages.success(request, "Application successfully added to the waitlist")
    elif profile.is_driver:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/application/review/'+str(id))
    return redirect('/application/list')

def application_edit(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to edit driver applications")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    if profile.is_sponsor or request.user.is_superuser:
        application = Application.objects.get(id=id)
        user=application.driver.user
        driver = DriverProfile.objects.get(user=user)
        if request.method == 'POST':
            form = ApplicationForm(request.POST, instance=application)
            if form.is_valid():
                application = form.save()
                application.save()
                return redirect('/application/review/'+str(id))
        else:

            form = ApplicationForm(instance=application)
        return render(request, 'application_edit.html', {'form': form, 'application': application, 'profile': profile,})
    elif profile.is_driver:
        application = Application.objects.get(id=id)
        user=application.driver.user
        driver = DriverProfile.objects.get(user=user)
        if request.method == 'POST':
            form = ApplicationForm(request.POST, instance=application)
            if form.is_valid():
                application = form.save()
                application.save()
                return redirect('/application/review/'+str(id))
        else:

            form = ApplicationForm(instance=application)
        return render(request, 'application_edit.html', {'form': form, 'application': application, 'driver': driver,})
    elif not request.user.is_superuser:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/application/review/'+str(id))
    