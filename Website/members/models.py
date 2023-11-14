from django.db import models
from django.contrib.auth.models import User
# Encryption at rest
from django_cryptography.fields import encrypt

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = encrypt(models.CharField(max_length=30, blank=True))
    last_name = encrypt(models.CharField(max_length=30, blank=True))
    middle_initial = encrypt(models.CharField(max_length=1, blank=True))
    email = models.EmailField(max_length=75, blank=True)
    is_driver = models.BooleanField('driver status', default=False)
    is_sponsor = models.BooleanField('sponsor status', default=False)

    def __str__(self):
        return self.user.username

class SponsorUserProfile(UserProfile):
    sponsor_name = models.CharField(max_length=25)

    def __str__(self):
        return self.user.username

class SponsorList(models.Model):
    sponsor_name = models.CharField(max_length=25, unique=True)
    point_conversion = models.FloatField(default=0.01)
    # point_neg = models.BooleanField('negative points', default=False) # Can negative point values be accepted?

    def __str__(self):
        return self.sponsor_name

class DriverProfile(UserProfile):
    points = models.IntegerField(default=0)
    sponsors = models.ManyToManyField(SponsorList, related_name='sponsored_users')
    street_address = encrypt(models.CharField(max_length= 85, blank=True))
    city = encrypt(models.CharField(max_length=40, blank=True))
    state = encrypt(models.CharField(max_length=2, blank=True))
    zipcode = encrypt(models.CharField(max_length=5, blank=True))
    phone_number = encrypt(models.CharField(max_length=15, blank=True))
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

    def __str__(self):
        return self.user.username

# class SponsorPoints(models.Model):
#     driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True)
#     sponsor_list = models.ForeignKey(SponsorList, on_delete=models.SET_NULL, null=True)
#     points = models.IntegerField(default=0,)

class PointReason(models.Model):
    point_amt = models.IntegerField(default=0)
    point_reason = models.TextField(max_length=250, blank=True)
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True)
    sponsor = models.ForeignKey(SponsorUserProfile, on_delete=models.SET_NULL, null=True)
    is_add = models.BooleanField('point change type', default=True)
