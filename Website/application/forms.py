from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['sponsor_name', 'first_name', 'last_name', 'middle_initial', 'email', 'phone', 'street_address', 'city', 'state', 'zipcode', 'license_num', 'plate_num', 'year', 'make', 'model', 'vin', 'provider_name', 'policy_number']

class ApplicatonReasonForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['application_reason']

    def __init__(self, *args, **kwargs):
        super(ApplicatonReasonForm, self).__init__(*args, **kwargs)

        self.fields['application_reason'].widget.attrs['class'] = 'form-control'