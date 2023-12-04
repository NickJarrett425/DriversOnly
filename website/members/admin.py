from django.contrib import admin
from .models import DriverProfile, UserProfile, SponsorUserProfile, SponsorList, SponsorOrganization

admin.site.register(UserProfile)
admin.site.register(DriverProfile)
admin.site.register(SponsorUserProfile)
admin.site.register(SponsorList)
admin.site.register(SponsorOrganization)