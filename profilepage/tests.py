from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from profilepage.models import Profile

User = get_user_model()

profilepage_url = "/profilepage/"


class TestExplore(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test2@test.test",
            password="testpassword",
            first_name="test",
            last_name="test",
        )

        existing_profile = Profile.objects.filter(user=self.user).first()

        if not existing_profile:
            Profile.objects.create(user=self.user)

    def test_profilepage(self):
        response = self.client.get(profilepage_url + str(self.user.id))
        self.assertEqual(response.status_code, 301)
