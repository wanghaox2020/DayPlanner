from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from .models import Venue, FavoriteVenue

User = get_user_model()


class FavoriteVenueTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            email="test_user@test.test",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.venue = Venue.objects.create(yelp_id="abc")

    def test_favorite_count(self):
        fav = FavoriteVenue.objects.create(user=self.user, venue=self.venue)
        self.assertEqual(self.venue.favoritevenue_set.count(), 1)

        fav.delete()
        self.assertEqual(self.venue.favoritevenue_set.count(), 0)
