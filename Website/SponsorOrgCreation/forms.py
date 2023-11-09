from django import forms
from .models import Org


class UpdateOrgForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    pointConvert = forms.DecimalField
    negativePointToggle = models.BooleanField()
    address = forms.CharField(required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    PhoneNumber = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Org
        fields = ['username', 'email', 'pointConvert', 'negativePointToggle', 'address', 'PhoneNumber']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
