from django.db import models
# Create your models here.
class Org(models.model)
    #can be used to tie to another model, currently only using this sponsor org model
    #username = models.OnetoOneField(User, on_delete = models.CASCADE)
    user = models.charField()
    email = models.EmailField()
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    pointConversion = models.DecimalField()
    negativePoint = models.BooleanField()
    address = models.TextField()
    phoneNumber = models.TextField()

    fields = ['username', 'email', 'pointConvert', 'negativePointToggle', 'address', 'PhoneNumber']