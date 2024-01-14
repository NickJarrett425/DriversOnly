from django.urls import path
from .views import *

urlpatterns = [
    path('search/', search_catalog, name='search_catalog'),
    path('view/item/', view_item, name='view_item'),
    path('choose/', choose_catalog, name='choose_catalog'),
    # ... other url patterns ...
]
