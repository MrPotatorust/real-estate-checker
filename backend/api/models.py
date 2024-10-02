from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Person(models.Model):
    city = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    imgs = ArrayField(models.CharField(max_length=100), blank=True)
