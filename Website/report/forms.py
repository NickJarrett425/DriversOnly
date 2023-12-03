from django import forms


class login_filter(forms.Form):
    #reqired

    #optional   
    user = forms.CharField(max_length=50,required=False,initial=None)
    start_date_range = forms.DateField(required=False,initial=None)
    end_date_range = forms.DateField(required=False,initial=None)

    def clean(self):
        cleaned_data = super().clean()
        start_date_range = cleaned_data.get('start_date_range')
        end_date_range = cleaned_data.get('end_date_range')

        if start_date_range and not end_date_range:
            self.add_error('end_date_range','Both Date Feilds are reqired. Please fill the field below.')
        elif end_date_range and not start_date_range:
            self.add_error('start_date_range','Both Date Feilds are reqired. Please fill the field below.')
        return cleaned_data
        
        