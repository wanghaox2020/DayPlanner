from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from resources.days.models import Day

# Create your tests here.
creation_url = "/creation/"


class CreationTest(TestCase):
    def setUp(self):
        self.client = Client()

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

    def test_creation_page_url_nouser(self):
        response = self.client.get(creation_url)
        self.assertEqual(response.status_code, 302)

    def test_creation_page_empty_days(self):
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(creation_url)
        self.assertTrue(response.context["userDayList"].count() == 0)

    def test_creation_page_present_days(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")

        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(creation_url)
        self.assertTrue(response.context["userDayList"].count() > 0)
