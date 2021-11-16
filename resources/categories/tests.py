# Create your tests here.
from unittest.mock import patch
from django.test import TestCase
from .models import Day
from django.contrib.auth.models import User
from .models import Category, DayCategory
from django.test import Client


foo_user1 = {
    "username": "test1",
    "first_name": "One",
    "last_name": "Test",
    "email": "test1@example.com",
    "password": "test1",
}


class CategoryModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User.objects.create_user(
            username=foo_user1["username"],
            email=foo_user1["email"],
            password=foo_user1["password"],
            first_name=foo_user1["first_name"],
            last_name=foo_user1["last_name"],
        )
        day1 = Day.objects.create(creator=user1, name="test1 DayPlan1")

    def add_new_category(self):
        cat1 = Category.objects.create(cat="sushi")
        self.assertTrue(len(Category.objects.get_queryset()) == 1)


class DayCategoryModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User.objects.create_user(
            username=foo_user1["username"],
            email=foo_user1["email"],
            password=foo_user1["password"],
            first_name=foo_user1["first_name"],
            last_name=foo_user1["last_name"],
        )
        day1 = Day.objects.create(creator=user1, name="test1 DayPlan1")
        cat1 = Category.objects.create(cat="sushi")

    def add_daycategory(self):
        DayCategory.objects.create(day=self.day1, cat=self.cat1)
        self.assertTrue(
            len(DayCategory.objects.filter(day=self.day1, cat=self.cat1)) == 1
        )
