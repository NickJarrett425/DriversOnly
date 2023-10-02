from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from .forms import RegisterUserForm

@user_passes_test(lambda user: not user.username, login_url='/about', redirect_field_name=None)

def login_user(request):
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
    logout(request)
    messages.success(request, ("You were successfully logged out."))
    return redirect('/')

@user_passes_test(lambda user: not user.username, login_url='/about', redirect_field_name=None)
def register_user(request):
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