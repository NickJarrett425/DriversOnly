from django.db import models

# Create your models here.

class log(models.Model):
    Datestamp = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=150,null=False,blank=False,default="test")

class login_log(models.Model):
    Datestamp = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=150,null=False,blank=False,default="test")
    login_success = models.BooleanField(null=False)

class password_change_log(log):
    password_change_type = models.BooleanField(null=False)