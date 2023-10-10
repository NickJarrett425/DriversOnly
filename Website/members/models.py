from django.db import models
from django import forms
from django.contrib.auth.models import User

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

class Vehicle(models.Model):
    make = models.CharField(max_length=25)
    model = models.CharField(max_length=25)
    year = models.PositiveIntegerField(null=True)
    vin = models.CharField(max_length=17)
    provider_name = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    middle_initial = models.CharField(max_length=1, blank=True)
    current_address = models.TextField(blank=True)

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # sponsor = models.ForeignKey('Sponsor', on_delete=models.CASCADE)
    # points = models.IntegerField(default=0)
    first_name = models.CharField(max_length=30, blank=True)
    middle_initial = models.CharField(max_length=1, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=40, blank=True)
    # state = forms.ChoiceField(choices=STATE_CHOICES)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=15, blank=True)
    drivers_license = models.CharField(max_length=15, blank=True)
    
    # Vehicle information (One driver can have multiple vehicles)
    vehicles = models.ManyToManyField(Vehicle, blank=True)
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)