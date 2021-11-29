from django.db import models
from dayplanner.services import yelp_client
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Venue(models.Model):
    yelp_id = models.CharField(max_length=100, unique=True, null=False)

    def raw_yelp_data(self):
        return yelp_client.fetch_by_id(self.yelp_id)

    def yelp__name(self):
        return self.raw_yelp_data()["name"]

    def yelp__image_url(self):
        return self.raw_yelp_data()["image_url"]

    def yelp__rating(self):
        return self.raw_yelp_data()["rating"]


class FavoriteVenue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    created_at = models.TimeField("Created at", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "venue"], name="favoritevenue_unique_user_venue"
            )
        ]
