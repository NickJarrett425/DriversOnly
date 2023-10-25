from django.db import models

# Create your models here.

class login_log(models.Model):
    Datestamp = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=150,null=False,blank=False,default="test")
    login_success = models.BooleanField(null=False)