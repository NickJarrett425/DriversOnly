from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UpdateOrgForm

from django.contrib.messages.views import SuccessMessageMixin

def OrgProfile(request):
    if request.method == 'POST':
        Org_form = UpdateOrgForm(request.POST, instance=request.user)

        if Org_form.is_valid():
            Org_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        Org_form = UpdateOrgForm(request.POST, instance=request.user)

    return render(request, 'orgCreate.html', {'Org_form': Org_form})




class SponsorOrgEmail(SuccessMessageMixin, ):
    template_name = 'OrgCreate.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')