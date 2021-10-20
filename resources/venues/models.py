from django.db import models

# Create your models here.
class Venue(models.Model):
    yelp_id = models.CharField(max_length=100,unique=True,null=False)


