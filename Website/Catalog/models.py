from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class Product(models.Model):
#     image = models.ImageField(upload_to='product_images/', null=True, blank=True)
#     name = models.CharField(max_length=255,blank=True)
#     artist = models.CharField(max_length=255, blank=True)
#     genre = models.CharField(max_length=255, blank=True)
#     description = models.TextField(max_length=250, blank=True)
#     point_price = models.IntegerField(default=0)
#     # Add other fields as needed

class Product(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.URLField(max_length=1024)
    # Add any other fields you need

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    # Add other fields like total price, etc.
