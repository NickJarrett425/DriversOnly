from django.contrib import admin
from .models import DriverProfile, UserProfile

admin.site.register(UserProfile)
admin.site.register(DriverProfile)