from django.db import models
from dayplanner.services import yelp_client

# Create your models here.
class Venue(models.Model):
    yelp_id = models.CharField(max_length=100,unique=True)

    def raw_yelp_data(self):
        return yelp_client.fetch_by_id(self.yelp_id)
        

