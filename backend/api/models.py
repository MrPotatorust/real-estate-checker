from django.db import models
# Create your models here.


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField(null=True)
    sq_m = models.FloatField(null=True)
    img = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    rentable = models.BooleanField(null=True)
    property_type = models.CharField(max_length=100, null=True)
    site = models.IntegerField()
    datetime = models.DateTimeField()

    class Meta:
        db_table = 'property_listings_merged'

    def __str__(self):
        return self.title