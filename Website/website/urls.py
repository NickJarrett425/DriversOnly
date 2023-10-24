from django.contrib import admin
from django.urls import path, include
from Catalog.views import search_catalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('', include('members.urls')),
    path('search/', search_catalog, name='search_catalog'),
    path('dashboard/', include('dashboard.urls'))
]
