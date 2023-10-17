from django.db import models
from django.contrib.auth.models import User, AbstractUser




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    middle_initial = models.CharField(max_length=1, blank=True)
    email = models.EmailField(max_length=75, blank=True)
    is_driver = models.BooleanField('driver status', default=False)
    is_sponsor = models.BooleanField('sponsor status', default=False)

class DriverProfile(UserProfile):
    points = models.IntegerField(default=0, blank=True)
    street_address = models.CharField(max_length= 85, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=5, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    drivers_license = models.CharField(max_length=15, blank=True)
    
    # Vehicle information
    year = models.PositiveIntegerField(null=True)
    make = models.CharField(max_length=25, blank=True)
    model = models.CharField(max_length=25, blank=True)
    vin = models.CharField(max_length=17, blank=True)
    provider_name = models.CharField(max_length=100, blank=True)
    policy_number = models.CharField(max_length=50, blank=True)
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)