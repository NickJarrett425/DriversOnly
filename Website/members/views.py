from .models import UserProfile, DriverProfile, Vehicle
from .forms import RegisterUserForm, UserProfileForm, DriverProfileForm, VehicleForm, VehicleAddForm
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
        redirect('about')  
        return render(request, 'registration/profile.html', {'profile': profile})

def edit_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('login_user')
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)
    if request.user.is_superuser:
        return render(request, 'registration/edit_admin_profile.html', {'profile': profile, 'form': form})
    else:
        return render(request, 'registration/edit_profile.html', {'profile': profile, 'form': form})

def view_driver_profile(request):
    try:
        driver, created = DriverProfile.objects.get_or_create(user=request.user)
        vehicles = driver.vehicles.all()
    except DriverProfile.DoesNotExist:
        driver = None
        vehicles = None

    return render(request, 'registration/driver_profile.html', {'driver': driver, 'vehicles': vehicles})

def edit_driver_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('/')

    try:
        driver = DriverProfile.objects.get(user=request.user)
        vehicle = Vehicle.objects.get(driverprofile=request.user.driverprofile)
    except DriverProfile.DoesNotExist:
        driver = None
        vehicle = None

    if request.method == 'POST':
        driver_form = DriverProfileForm(request.POST, instance=driver)
        vehicle_form = VehicleForm(request.POST, instance=vehicle)

        if driver_form.is_valid(): # and vehicle_form.is_valid():
            driver = driver_form.save(commit=False)
            driver.user = request.user
            driver.save()

            if vehicle_form.is_valid():
                vehicle = vehicle_form.save(commit=False)
                vehicle.user_profile = request.user.driverprofile
                vehicle.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('view_driver_profile')
    else:
        driver_form = DriverProfileForm(instance=driver)
        vehicle_form = VehicleForm(instance=vehicle)

    return render(request, 'registration/edit_driver_profile.html', {
        'driver_form': driver_form,
        'vehicle_form': vehicle_form,
        'driver': driver,
        'vehicle': vehicle,
    })

def add_vehicle(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = VehicleAddForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user_profile = request.user.driverprofile
            vehicle.save()
            
            request.user.driverprofile.vehicles.add(vehicle)
            return redirect('view_driver_profile')
    else:
        form = VehicleAddForm()
    
    return render(request, 'registration/add_vehicle.html', {'form': form})