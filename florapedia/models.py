from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.

class Plant(models.Model):
    plant_name = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],blank=True)
    days_between_waterings = models.BigIntegerField()
    article =models.TextField()
    Family =models.CharField(max_length=50, blank=True)
    Tribe =models.CharField(max_length=50, blank=True)
    Genus =models.CharField(max_length=50, blank=True)
    growing_conditions=models.TextField()


