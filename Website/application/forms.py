from django import forms
from .models import Application
from members.models import SponsorList

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['sponsor_name', 'first_name', 'last_name', 'middle_initial', 'email', 'phone', 'street_address', 'city', 'state', 'zipcode', 'license_num', 'plate_num', 'year', 'make', 'model', 'vin', 'provider_name', 'policy_number']

    sponsor_name = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['sponsor_name'].choices = self.get_choices()

    def get_choices(self):
        choices = SponsorList.objects.values_list('sponsor_name', 'sponsor_name').distinct()
        return choices

class ApplicatonReasonForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['application_reason']

    def __init__(self, *args, **kwargs):
        super(ApplicatonReasonForm, self).__init__(*args, **kwargs)

        self.fields['application_reason'].widget.attrs['class'] = 'form-control'