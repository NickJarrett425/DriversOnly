from django.db import models
class about(models.Model):
    nick = models.CharField("Nick's Name", max_length=20)
    david = models.CharField("David's Name", max_length=20)
    neil = models.CharField("Neil's Name", max_length=20)
    dhruvisha = models.CharField("Dhruvisha's Name", max_length=20)
    version = models.CharField("Sprint Number:", max_length=10)
    release_date = models.DateField("Release Date")
    product_name = models.CharField("Product Name", max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.version