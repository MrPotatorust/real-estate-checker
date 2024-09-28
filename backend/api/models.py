from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class FinalCard(models.Model):
    city = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=300)
    img = models.CharField(max_length=300)
    location_description = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    sq_meters = models.FloatField()
    price = models.FloatField()
    
