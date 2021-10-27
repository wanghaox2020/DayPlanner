from django.test import TestCase
from django.contrib.auth import get_user_model

login_url = "/authentication/login"


foo_user = {
    "username": "test1",
    "first_name": "One",
    "last_name": "Test",
    "email": "test1@example.com",
    "password": "test1",
}


def createFooUser():
    User = get_user_model()
    User.objects.create_user(
        username=foo_user["username"],
        email=foo_user["email"],
        password=foo_user["password"],
        first_name=foo_user["first_name"],
        last_name=foo_user["last_name"],
    )


class SignUpTest(TestCase):
    def setUp(self):
        self.username = "test1"
        self.email = "test1@example.com"
        self.password = "test1"

    def test_signup_page_url(self):
        response = self.client.get("/authentication/signup")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authentication/signup.html")

    def test_wrong_signup(self):
        response = self.client.post(
            "/authentication/signup",
            data={
                "email": self.email,
                "username": self.username,
                "password1": self.password,
                "password2": "not_woring",
            },
        )
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_signup(self):
        response = self.client.post(
            "/authentication/signup",
            data={
                "email": self.email,
                "username": self.username,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEqual(response.status_code, 302)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)


class LoginTest(TestCase):
    def setUp(self):
        createFooUser()
        self.username = "test1"
        self.email = "test1@example.com"
        self.password = "test1"

    def test_login(self):
        response = self.client.post(
            "/authentication/login",
            data={
                "username": self.username,
                "password": self.password,
            },
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_wrong_login(self):
        response = self.client.post(
            "/authentication/login",
            data={
                "username": self.username,
                "password": self.password + self.password,
            },
            follow=True,
        )
        self.assertIsNone(response.context)


class LogoutTest(TestCase):
    def setUp(self):
        createFooUser()
        self.username = "test1"
        self.email = "test1@example.com"
        self.password = "test1"

    def test_logout(self):
        self.client.login(username="test1", password="test1")
        response = self.client.get("/authentication/login")
        self.client.logout()
        self.assertEquals(response.status_code, 200)
        response = self.client.get("/authentication/logout")
        self.assertEquals(response.status_code, 302)
