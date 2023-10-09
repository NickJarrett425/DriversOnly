from django.contrib import admin
from django.urls import path
from Catalog.views import search_catalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search_catalog, name='search_catalog'),
]
