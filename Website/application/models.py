from django.db import models
from members.models import DriverProfile
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Define the custom validator functions
def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError("Phone number must contain only numeric characters.")

# Define a RegexValidator for the phone number format
phone_number_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits long.",
)
class Application(models.Model):
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True)
    sponsor_name = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    middle_initial = models.CharField(max_length=1, blank=True)
    email = models.EmailField(max_length=75, blank=False)
    phone = models.CharField(max_length=10, validators=[validate_phone_number, phone_number_validator])
    
    street_address = models.CharField(max_length= 85, blank=False)
    city = models.CharField(max_length=40, blank=False)
    state = models.CharField(max_length=2, blank=False)
    zipcode = models.CharField(max_length=5, blank=False)

    license_num = models.CharField(max_length=30, blank=False)
    plate_num = models.CharField(max_length=10, blank=False)
    year = models.PositiveIntegerField(null=False)
    make = models.CharField(max_length=25, blank=False)
    model = models.CharField(max_length=25, blank=False)
    vin = models.CharField(max_length=17, blank=False)
    provider_name = models.CharField(max_length=100, blank=False)
    policy_number = models.CharField(max_length=50, blank=False)
    date_created = models.DateTimeField(auto_now=True)
    application_reason = models.TextField(max_length=250, blank=True)

    is_open = models.BooleanField('application status', default=True)
    is_approved = models.BooleanField('approval status', default=False)
    is_waitlisted = models.BooleanField('waitlist status', default=False)
    

    def __str__(self):
        return f"{self.driver.user.username}'s application to {self.sponsor_name}"


