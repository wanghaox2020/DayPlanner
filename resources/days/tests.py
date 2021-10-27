from django.test import TestCase
from .models import Day, User
from django.test import Client


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
