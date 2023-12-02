from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, DriverProfile, SponsorUserProfile, SponsorList, PointReason


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
        fields = ['first_name', 'middle_initial', 'last_name', 'phone_number', 'email', 'date_of_birth', 'street_address', 'city', 'state', 'zipcode', 'drivers_license', 'year', 'make', 'model', 'vin', 'provider_name', 'policy_number', 'emergency_contact_name', 'emergency_contact_phone']
    def __init__(self, *args, **kwargs):
        super(DriverProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['class'] = 'form-control-sm'
        self.fields['middle_initial'].widget.attrs['class'] = 'form-control-sm'
        self.fields['last_name'].widget.attrs['class'] = 'form-control-sm'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control-sm'
        self.fields['email'].widget.attrs['class'] = 'form-control-sm'
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-control-sm'
        self.fields['street_address'].widget.attrs['class'] = 'form-control-sm'
        self.fields['city'].widget.attrs['class'] = 'form-control-sm'
        self.fields['state'].widget.attrs['class'] = 'form-control-sm'
        self.fields['zipcode'].widget.attrs['class'] = 'form-control-sm'
        self.fields['drivers_license'].widget.attrs['class'] = 'form-control-sm'
        self.fields['year'].widget.attrs['class'] = 'form-control-sm'
        self.fields['make'].widget.attrs['class'] = 'form-control-sm'
        self.fields['model'].widget.attrs['class'] = 'form-control-sm'
        self.fields['vin'].widget.attrs['class'] = 'form-control-sm'
        self.fields['provider_name'].widget.attrs['class'] = 'form-control-sm'
        self.fields['policy_number'].widget.attrs['class'] = 'form-control-sm'
        self.fields['emergency_contact_name'].widget.attrs['class'] = 'form-control-sm'
        self.fields['emergency_contact_phone'].widget.attrs['class'] = 'form-control-sm'

class AssignSponsorForm(forms.ModelForm):
    class Meta:
        model = SponsorUserProfile
        fields = ('sponsor_name',)
    
    sponsor_name = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(AssignSponsorForm, self).__init__(*args, **kwargs)
        self.fields['sponsor_name'].choices = self.get_choices()

    def get_choices(self):
        choices = SponsorList.objects.values_list('sponsor_name', 'sponsor_name').distinct()
        return choices
    
class ChooseSponsorForm(forms.Form):
    sponsor_choices = forms.ChoiceField(label='Select Sponsor')

    def __init__(self, *args, **kwargs):
        sponsor_queryset = kwargs.pop('sponsor_queryset', None)
        super(ChooseSponsorForm, self).__init__(*args, **kwargs)
        
        if sponsor_queryset:
            sponsor_choices = [(sponsor.id, sponsor.sponsor_name) for sponsor in sponsor_queryset]
            self.fields['sponsor_choices'].choices = [('', '--- Select Sponsor ---')] + sponsor_choices
    
class PointReasonForm(forms.ModelForm):

    class Meta:
        model = PointReason
        fields = ['point_amt', 'is_add', 'point_reason',]

    def __init__(self, *args, **kwargs):
        super(PointReasonForm, self).__init__(*args, **kwargs)

        self.fields['point_amt'].widget.attrs['class'] = 'form-control'
        self.fields['is_add'].widget = forms.HiddenInput()
        self.fields['point_reason'].widget.attrs['class'] = 'form-control'

class EmailForm(forms.Form):
    email = forms.EmailField(label='Enter your email', max_length=75)