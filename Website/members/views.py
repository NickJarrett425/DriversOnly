from .models import UserProfile, DriverProfile
from .forms import RegisterUserForm, UserProfileForm, DriverProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from report.models import login_log

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/about')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            login_attempt = login_log(username=username, login_success="True")
            login_attempt.save()
            return redirect('about/')
        else:
            messages.success(request, ("There was an error logging in, please try again."))
            login_attempt = login_log(username=username, login_success="False")
            login_attempt.save()
            return redirect('/')
    else:
        return render(request, 'registration/login.html', {})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, ("You were successfully logged out."))       
    else:
        messages.success(request, ("You are not currently logged in to an account."))   
    return redirect('/')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/about')
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            try:
                driver, created = DriverProfile.objects.get_or_create(user=request.user)
            except DriverProfile.DoesNotExist:
                driver = None
            driver.first_name = form.cleaned_data['first_name']
            driver.last_name = form.cleaned_data['last_name']
            driver.email = form.cleaned_data['email']
            driver.is_driver = True
            driver.user = request.user
            driver.save()
            login_attempt = login_log(username=username, login_success="True")
            login_attempt.save()
            messages.success(request, ("You were successfully registered."))
            return redirect('/')
    else:
        form = RegisterUserForm()

    return render(request, 'registration/register_user.html', {'form':form,})

def view_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view your profile")
        return redirect('/')
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if profile.is_driver:
        try:
            driver = DriverProfile.objects.get(user=request.user)
        except DriverProfile.DoesNotExist:
            driver = None

        return render(request, 'registration/profile.html', {'profile': profile, 'driver': driver})
    else:
        return render(request, 'registration/profile.html', {'profile': profile})

def edit_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('login_user')
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if profile.is_driver:
        try:
            driver = DriverProfile.objects.get(user=request.user)
        except DriverProfile.DoesNotExist:
            driver = None

        if request.method == 'POST':
            driver_form = DriverProfileForm(request.POST, instance=driver)

            if driver_form.is_valid():
                driver = driver_form.save(commit=False)
                driver.user = request.user
                driver.save()

                messages.success(request, "Profile updated successfully!")
                return redirect('view_profile')
        else:
            driver_form = DriverProfileForm(instance=driver)

        return render(request, 'registration/edit_profile.html', {'driver_form': driver_form, 'driver': driver, 'profile': profile})
    
    else:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('view_profile')
        else:
            form = UserProfileForm(instance=profile)
        return render(request, 'registration/edit_profile.html', {'profile': profile, 'form': form})