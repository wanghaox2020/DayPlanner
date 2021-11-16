from django.apps import AppConfig
from .test_users import create_test_users


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"

    def ready(self):
        create_test_users()
