from django.contrib import admin
from .models import DriverProfile, UserProfile, SponsorUserProfile, SponsorList

admin.site.register(UserProfile)
admin.site.register(DriverProfile)
admin.site.register(SponsorUserProfile)
admin.site.register(SponsorList)