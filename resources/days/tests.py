from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Day, DayVenue, FavoriteDay
from resources.venues.models import Venue
from django.test import Client
from dayplanner.services.yelp_client import YelpRequest

User = get_user_model()


class DayModelTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_1 = User.objects.create_user(
            username="test_user_1",
            email="test_user_1@test.com",
            password="test",
            first_name="test_user_1",
            last_name="test_user_1",
        )

        self.venue_1 = Venue.objects.create(yelp_id="abc")
        self.venue_2 = Venue.objects.create(yelp_id="xyz")

        self.day_1 = Day.objects.create(
            creator=self.user_1, name="abc", description="xyz"
        )

        DayVenue.objects.create(day=self.day_1, venue=self.venue_1, pos=1)
        DayVenue.objects.create(day=self.day_1, venue=self.venue_2, pos=2)

    def test_fork(self):
        user_2 = User.objects.create_user(
            username="test_user_2",
            email="test_user_2@test.com",
            password="test",
            first_name="test_user_2",
            last_name="test_user_2",
        )

        self.day_1.fork(creator=user_2)
        forked_day = Day.objects.filter(creator=user_2)
        self.assertEqual(len(forked_day), 1)
        forked_day = forked_day[0]

        self.assertEqual(self.day_1.creator, self.user_1)
        self.assertEqual(forked_day.creator, user_2)

        self.assertEqual(forked_day.name, self.day_1.name)
        self.assertEqual(forked_day.description, self.day_1.description)

        self.assertEqual(forked_day.dayvenue_set.count(), 2)
        for dv in self.day_1.dayvenue_set.all():
            forked_dv = forked_day.dayvenue_set.get(pos=dv.pos)
            self.assertEqual(dv.venue, forked_dv.venue)
            self.assertNotEqual(dv.day, forked_dv.day)


foo_user1 = {
    "username": "test1",
    "first_name": "One",
    "last_name": "Test",
    "email": "test1@example.com",
    "password": "test1",
}

foo_user2 = {
    "username": "test2",
    "first_name": "Two",
    "last_name": "Test",
    "email": "test2@example.com",
    "password": "test2",
}


class DayListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User.objects.create_user(
            username=foo_user1["username"],
            email=foo_user1["email"],
            password=foo_user1["password"],
            first_name=foo_user1["first_name"],
            last_name=foo_user1["last_name"],
        )
        Day.objects.create(creator=user1, name="test1 DayPlan")
        Day.objects.create(creator=user1, name="test1 DayPlan2")

    def test_get_queryset(self):
        response = self.client.get("/resources/days/test1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["day_list"]), 2)


class AllDaysViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User.objects.create_user(
            username=foo_user1["username"],
            email=foo_user1["email"],
            password=foo_user1["password"],
            first_name=foo_user1["first_name"],
            last_name=foo_user1["last_name"],
        )
        user2 = User.objects.create_user(
            username=foo_user2["username"],
            email=foo_user2["email"],
            password=foo_user2["password"],
            first_name=foo_user2["first_name"],
            last_name=foo_user2["last_name"],
        )
        Day.objects.create(creator=user1, name="test1 DayPlan1")
        Day.objects.create(creator=user1, name="test1 DayPlan2")
        Day.objects.create(creator=user2, name="test2 DayPlan1")

    def test_get_queryset(self):
        response = self.client.get("/resources/days/")
        self.assertEqual(len(response.context["all_days"]), 3)


class DetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User.objects.create_user(
            username=foo_user1["username"],
            email=foo_user1["email"],
            password=foo_user1["password"],
            first_name=foo_user1["first_name"],
            last_name=foo_user1["last_name"],
        )
        Day.objects.create(creator=user1, name="test1 DayPlan")
        Day.objects.create(creator=user1, name="test1 DayPlan2")

    def test_set_in_context(self):
        response = self.client.get("/resources/days/1/")
        self.assertEqual(response.context["detail"].name, "test1 DayPlan")


class EditViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User.objects.create_user(
            username=foo_user1["username"],
            email=foo_user1["email"],
            password=foo_user1["password"],
            first_name=foo_user1["first_name"],
            last_name=foo_user1["last_name"],
        )
        self.day1 = Day.objects.create(creator=user1, name="test1 Day")
        self.day2 = Day.objects.create(creator=user1, name="test2 Day")

    def test_get(self):
        self.assertEqual(len(self.day1.dayvenue_set.all()), 0)

        self.client.get("/resources/days/%i/edit" % self.day1.id)

        self.assertEqual(len(self.day1.dayvenue_set.all()), 0)

    def test_post_new_venue(self):
        self.assertEqual(len(self.day2.dayvenue_set.all()), 0)

        yelp_data = {"yelp_id": "test_id", "name": "foo", "image_url": "bar"}

        with patch.object(YelpRequest, "execute", return_value=yelp_data):
            self.client.post(
                "/resources/days/%i/edit" % self.day2.id, {"yelp_id": "test_id"}
            )
            self.assertEqual(len(self.day2.dayvenue_set.all()), 1)


class FavoriteDayTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            email="test_user@test.test",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.day = Day.objects.create(creator=self.user, name="test1 Day")

    def test_favorite_count(self):
        fav = FavoriteDay.objects.create(user=self.user, day=self.day)
        self.assertEqual(self.day.favoriteday_set.count(), 1)

        fav.delete()
        self.assertEqual(self.day.favoriteday_set.count(), 0)
