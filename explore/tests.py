from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from resources.days.models import Day

# Create your tests here.

class TestExplore(TestCase):
    def setUp(self):
        self.client = Client()
        self.explore_url = "/explore/"
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

    def test_explore_index(self):
        response = self.client.get(self.explore_url)
        self.assertEqual(response.status_code, 200)

    def test_explore_day_fail(self):
        response = self.client.get(self.explore_url+"0")
        self.assertEqual(response.status_code, 404)

    def test_explore_day_success(self):
        response = self.client.get(self.explore_url+str(self.test_day.id))
        self.assertEqual(response.status_code, 200)





