from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('', include('members.urls')),
    path('catalog/', include('Catalog.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('application/', include ('application.urls')),
    path('report/', include('report.urls')),
]
