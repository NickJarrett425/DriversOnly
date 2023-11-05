from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    # Add other fields as needed
