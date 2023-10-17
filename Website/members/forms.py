from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, DriverProfile


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'middle_initial', 'email']

class DriverProfileForm(UserProfileForm):
    class Meta:
        model = DriverProfile
        fields = ['first_name', 'last_name', 'middle_initial', 'email', 'street_address', 'city', 'state', 'zipcode', 'phone_number', 'email', 'date_of_birth', 'drivers_license', 'year', 'make', 'model', 'vin', 'provider_name', 'policy_number', 'emergency_contact_name', 'emergency_contact_phone']
