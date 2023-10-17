from .models import UserProfile, DriverProfile
from .forms import RegisterUserForm, UserProfileForm, DriverProfileForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/about')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('about/')
        else:
            messages.success(request, ("There was an error logging in, please try again."))
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
            messages.success(request, ("You were successfully registered."))
            return redirect('/')
    else:
        form = RegisterUserForm()

    return render(request, 'registration/register_user.html', {'form':form,})

def view_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.user.is_superuser:
        return render(request, 'registration/admin_profile.html', {'profile': profile})
    else:
        return render(request, 'registration/profile.html', {'profile': profile})


def edit_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('login_user')

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if 'password_change' in request.POST:
            password_change_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_change_form.is_valid():
                password_change_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully!")
                return redirect('view_profile')
        else:
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)
        password_change_form = CustomPasswordChangeForm(request.user)

    if request.user.is_superuser:
        return render(request, 'registration/edit_admin_profile.html', {'profile': profile, 'form': form, 'password_change_form': password_change_form})
    else:
        return render(request, 'registration/edit_profile.html', {'profile': profile, 'form': form, 'password_change_form': password_change_form})


def view_driver_profile(request):
    try:
        driver, created = DriverProfile.objects.get_or_create(user=request.user)
    except DriverProfile.DoesNotExist:
        driver = None

    return render(request, 'registration/driver_profile.html', {'driver': driver})

def edit_driver_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('/')

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
            return redirect('view_driver_profile')
    else:
        driver_form = DriverProfileForm(instance=driver)

    return render(request, 'registration/edit_driver_profile.html', {'driver_form': driver_form, 'driver': driver})