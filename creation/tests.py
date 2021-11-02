from django.test import TestCase

# Create your tests here.
creation_url = "/creation/"


class CreationTest(TestCase):
    def test_creation_page_url_nouser(self):
        response = self.client.get(creation_url)
        self.assertEqual(response.status_code, 302)
