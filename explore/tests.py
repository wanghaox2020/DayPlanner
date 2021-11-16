from django.test import TestCase, Client
from resources.days.models import Day

# Create your tests here.

class TestExplore(TestCase):
    def setUp(self):
        self.client = Client()
        self.explore_url = "/explore/"

    def test_explore_index(self):
        response = self.client.get(self.explore_url)
        self.assertEqual(response.status_code, 200)




