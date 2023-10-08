from .models import UserProfile
from .forms import UserProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

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
    
    return render(request, 'registration/edit_profile.html', {'profile': profile, 'form': form})
