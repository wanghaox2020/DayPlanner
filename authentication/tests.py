from django.test import TestCase, Client
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

login_url = "/authentication/login"


foo_user = {
    "username": "test1",
    "first_name": "One",
    "last_name": "Test",
    "email": "test1@example.com",
    "password": "test1",
}


def createFooUse():
    User = get_user_model()
    User.objects.create_user(
        username=foo_user["username"],
        email=foo_user["email"],
        password=foo_user["password"],
        first_name=foo_user["first_name"],
        last_name=foo_user["last_name"],
    )


class LoginTest(TestCase):
    def setUp(self):
        createFooUse()

    def test_user(self):
        fooUser = authenticate(
            username=foo_user["username"], password=foo_user["password"]
        )
        self.assertIsNotNone(fooUser)

    def test_user_authenticate_wrong_password(self):
        fooUser = authenticate(
            email=foo_user["email"],
            password=foo_user["password"] + foo_user["password"],
        )
        self.assertIsNone(fooUser)

    def test_user_authenticate_invalid_user(self):
        fooUser = authenticate(
            email=foo_user["first_name"], password=foo_user["password"]
        )
        self.assertIsNone(fooUser)

    def test_login_get_page(self):
        client = Client()
        response = client.get(login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_with_correct_credentials(self):
        client = Client()
        can_login = client.login(
            username=foo_user["username"], password=foo_user["password"]
        )
        self.assertTrue(can_login)

    def test_login_with_incorrect_credentials(self):
        client = Client()
        can_login = client.login(
            username=foo_user["username"],
            password=foo_user["password"] + foo_user["password"],
        )
        self.assertFalse(can_login)

    # def test_anonymoususer_access_user_profile(self):
    #     client = Client()
    #     response = client.get("/candidate_login/success/")
    #     self.assertEqual(response.status_code, 404)
