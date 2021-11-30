from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from resources.days.models import Day, DayVenue
from resources.categories.models import Category, DayCategory

# Create your tests here.
from resources.venues.models import Venue


class TestExplore(TestCase):
    def setUp(self):
        self.client = Client()
        self.explore_url = "/explore/"
        self.search_empty = {"search_input": ""}
        self.search_test = {"search_input": "test"}
        User = get_user_model()
        self.test_username = "test"
        self.test_password = "test"
        self.test_user = User.objects.create_user(
            username=self.test_username,
            email="test2@test.test",
            password=self.test_password,
            first_name="test",
            last_name="test",
        )
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        self.test_cat = Category.objects.create(cat="TestCat")
        self.venue = Venue.objects.create(yelp_id="abc")
        DayCategory.objects.create(day=self.test_day, cat=self.test_cat)

    def test_explore_index(self):
        response = self.client.get(self.explore_url)
        self.assertEqual(response.status_code, 200)

    def test_explore_day_fail(self):
        response = self.client.get(self.explore_url + "0")
        self.assertEqual(response.status_code, 404)

    def test_explore_day_success(self):
        response = self.client.get(self.explore_url + str(self.test_day.id))
        self.assertEqual(response.status_code, 200)

    def test_explore_day_searchEmpty(self):
        response = self.client.post("/explore/search", self.search_empty)
        self.assertEqual(response.status_code, 200)

    def test_explore_day_search(self):
        response = self.client.post("/explore/search", self.search_test)
        self.assertEqual(response.status_code, 200)

    def test_explore_categories(self):
        response = self.client.get("/explore/search/" + self.test_cat.cat)
        self.assertEqual(response.status_code, 200)

    def test_fork(self):
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get("/explore/" + str(self.test_day.id) + "/fork")
        self.assertEqual(response.status_code, 302)

    def test_favorite_day(self):
        # test Add fav day
        last_url = "/explore/"
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(
            "/explore/favorite_day/" + str(self.test_day.id) + "?" + last_url
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.test_day.favoriteday_set.filter(user=self.test_user).count(), 1
        )

        # test remove fav day
        response = self.client.get(
            "/explore/unfavorite_day/" + str(self.test_day.id) + "?" + last_url
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.test_day.favoriteday_set.filter(user=self.test_user).count(), 0
        )

    def test_favorite_venue(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        dv = DayVenue.objects.create(day=self.test_day, venue=self.venue, pos=1)
        # test Add fav venue
        last_url = "/explore/" + str(self.test_day.id)
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(
            "/explore/favorite_venue/" + str(dv.id) + "?" + last_url
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            dv.venue.favoritevenue_set.filter(user=self.test_user).count(), 1
        )

        # test remove fav venue
        response = self.client.get(
            "/explore/unfavorite_venue/" + str(dv.id) + "?" + last_url
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            dv.venue.favoritevenue_set.filter(user=self.test_user).count(), 0
        )

    def test_favorite_venue_withoutLogin(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        dv = DayVenue.objects.create(day=self.test_day, venue=self.venue, pos=1)
        # test Add fav venue
        last_url = "/explore/" + str(self.test_day.id)
        response = self.client.get(
            "/explore/favorite_venue/" + str(dv.id) + "?" + last_url
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            dv.venue.favoritevenue_set.filter(user=self.test_user).count(), 0
        )

        # test remove fav venue
        response = self.client.get(
            "/explore/unfavorite_venue/" + str(dv.id) + "?" + last_url
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            dv.venue.favoritevenue_set.filter(user=self.test_user).count(), 0
        )

    def test_favorite_day_withoutLogin(self):
        # test Add fav day
        last_url = "/explore/"
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        response = self.client.get(
            "/explore/favorite_day/" + str(self.test_day.id) + "?" + last_url
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.test_day.favoriteday_set.filter(user=self.test_user).count(), 0
        )

        # test remove fav day
        response = self.client.get(
            "/explore/unfavorite_day/" + str(self.test_day.id) + "?" + last_url
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.test_day.favoriteday_set.filter(user=self.test_user).count(), 0
        )



