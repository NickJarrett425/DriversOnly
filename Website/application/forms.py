from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['driver', 'sponsor_name', 'first_name', 'last_name', 'middle_initial', 'email', 'phone', 'street_address', 'city', 'state', 'zipcode', 'license_num', 'plate_num', 'year', 'make', 'model', 'vin', 'provider_name', 'policy_number']