from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('search/', search_catalog, name='search_catalog'),
    path('view/item/', view_item, name='view_item'),
    path('choose/', choose_catalog, name='choose_catalog'),
   
    path('catalog/add_to_cart/',views.add_to_cart, name='add_to_cart'),
    path('view/cart/', view_cart, name='view_cart'),


    # urls.py

    # urls.py

    # ... other url patterns ...
]
