from django import forms

report_types = (
    ("1","Login"),
)

class report_filtering(forms.Form):
    #reqired
    report_type = forms.ChoiceField(choices=report_types)

    #optional   
    user = forms.CharField(max_length=50,required=False)
    start_date_range = forms.DateField(required=False)
    end_date_range = forms.DateField(required=False)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     report_types = cleaned_data.get('report_type')
    #     user = cleaned_data.get('user')
    #     start_date_range = cleaned_data.get('start_date_range')
    #     end_date_range = cleaned_data.get('end_date_range')

    #     if start_date_range and not end_date_range:
    #         raise forms.ValidationError("End date is reqired with start date")
    #     if end_date_range and not start_date_range:
    #         raise forms.ValidationError("Start date is reqired with End date")
        
        