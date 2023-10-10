from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, DriverProfile, Vehicle

# STATE_CHOICES = (
#     ('AL', 'Alabama'),
#     ('AK', 'Alaska'),
#     ('AZ', 'Arizona'),
#     ('AR', 'Arkansas'),
#     ('CA', 'California'),
#     ('CO', 'Colorado'),
#     ('CT', 'Connecticut'),
#     ('DE', 'Delaware'),
#     ('DC', 'District Of Columbia'),
#     ('FL', 'Florida'),
#     ('GA', 'Georgia'),
#     ('HI', 'Hawaii'),
#     ('ID', 'Idaho'),
#     ('IL', 'Illinois'),
#     ('IN', 'Indiana'),
#     ('IA', 'Iowa'),
#     ('KS', 'Kansas'),
#     ('KY', 'Kentucky'),
#     ('LA', 'Louisiana'),
#     ('ME', 'Maine'),
#     ('MD', 'Maryland'),
#     ('MA', 'Massachusetts'),
#     ('MI', 'Michigan'),
#     ('MN', 'Minnesota'),
#     ('MS', 'Mississippi'),
#     ('MO', 'Missouri'),
#     ('MT', 'Montana'),
#     ('NE', 'Nebraska'),
#     ('NV', 'Nevada'),
#     ('NH', 'New Hampshire'),
#     ('NJ', 'New Jersey'),
#     ('NM', 'New Mexico'),
#     ('NY', 'New York'),
#     ('NC', 'North Carolina'),
#     ('ND', 'North Dakota'),
#     ('OH', 'Ohio'),
#     ('OK', 'Oklahoma'),
#     ('OR', 'Oregon'),
#     ('PA', 'Pennsylvania'),
#     ('RI', 'Rhode Island'),
#     ('SC', 'South Carolina'),
#     ('SD', 'South Dakota'),
#     ('TN', 'Tennessee'),
#     ('TX', 'Texas'),
#     ('UT', 'Utah'),
#     ('VT', 'Vermont'),
#     ('VA', 'Virginia'),
#     ('WA', 'Washington'),
#     ('WV', 'West Virginia'),
#     ('WI', 'Wisconsin'),
#     ('WY', 'Wyoming'),
# )

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
        fields = ['first_name', 'last_name', 'middle_initial', 'current_address']

class DriverProfileForm(forms.ModelForm):
    # state = forms.ChoiceField(choices=STATE_CHOICES)

    class Meta:
        model = DriverProfile
        fields = ['first_name', 'middle_initial', 'last_name', 'date_of_birth', 'street_address', 'city', 'state', 'zipcode', 'phone_number', 'drivers_license', 'emergency_contact_name', 'emergency_contact_phone']

# Create a form for the Vehicle model
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'vin', 'provider_name', 'policy_number']

class VehicleAddForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'vin', 'provider_name', 'policy_number']