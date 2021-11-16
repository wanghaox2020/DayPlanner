from django.contrib.auth.models import User


def create_test_users():
    User.objects.get_or_create(
        email="prof@mailinator.com", username="prof", password="asdf"
    )
    User.objects.get_or_create(
        email="ta@mailinator.com", username="ta", password="asdf"
    )
    User.objects.get_or_create(
        email="testuser1@mailinator.com", username="testuser1", password="asdf"
    )
    User.objects.get_or_create(
        email="testuser2@mailinator.com", username="testuser2", password="asdf"
    )
    User.objects.get_or_create(
        email="testuser3@mailinator.com", username="testuser3", password="asdf"
    )
    User.objects.get_or_create(
        email="testuser4@mailinator.com", username="testuser4", password="asdf"
    )
    User.objects.get_or_create(
        email="testuser5@mailinator.com", username="testuser5", password="asdf"
    )
