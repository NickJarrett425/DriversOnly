from django.contrib import admin
from django.urls import path
from .views import search_catalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search_catalog, name='search_catalog'),  # Single URL for search
    # path('search/<int:id>/', view_item, name='view_item'),
    # ... other url patterns ...
]
