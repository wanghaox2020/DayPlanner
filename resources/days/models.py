from django.db import models
from django.contrib.auth.models import User
from resources.venues.models import Venue



class Day(models.Model):
    # primary key is auto generated by django
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    venues = models.ManyToManyField(Venue, through='DayVenue')

class DayVenue(models.Model):
    day = models.ForeignKey(Day,on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE)
    pos = models.IntegerField()

