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


def createFooUse():
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

    def test_signup_page_view_name(self):
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
        createFooUse()
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
        self.assertTrue(response.context["user"].is_active)

    def test_wrong_login(self):
        response = self.client.post(
            "/authentication/login",
            data={
                "username": self.username,
                "password": self.password + self.password,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    # def test_user(self):
    #     fooUser = authenticate(
    #         username=foo_user["username"], password=foo_user["password"]
    #     )
    #     self.assertIsNotNone(fooUser)

    # def test_user_authenticate_wrong_password(self):
    #     fooUser = authenticate(
    #         email=foo_user["email"],
    #         password=foo_user["password"] + foo_user["password"],
    #     )
    #     self.assertIsNone(fooUser)

    # def test_user_authenticate_invalid_user(self):
    #     fooUser = authenticate(
    #         email=foo_user["first_name"], password=foo_user["password"]
    #     )
    #     self.assertIsNone(fooUser)

    # def test_login_get_page(self):
    #     client = Client()
    #     response = client.get(login_url)
    #     self.assertEqual(response.status_code, 200)

    # def test_login_with_correct_credentials(self):
    #     client = Client()
    #     can_login = client.login(
    #         username=foo_user["username"], password=foo_user["password"]
    #     )
    #     self.assertTrue(can_login)

    # def test_login_with_incorrect_credentials(self):
    #     client = Client()
    #     can_login = client.login(
    #         username=foo_user["username"],
    #         password=foo_user["password"] + foo_user["password"],
    #     )
    #     self.assertFalse(can_login)
