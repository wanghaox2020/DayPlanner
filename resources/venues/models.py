from django.db import models

# Create your models here.
class Venue(models.Model):
    yelp_id = models.CharField(max_length=100,unique=True)

    @staticmethod
    def for_yelp_id(yelp_id):
        venue, created = Venue.objects.get_or_create(yelp_id=yelp_id)
        return venue if created else False
