def create_test_users():
    from django.contrib.auth import get_user_model

    User = get_user_model()

    User.objects.get_or_create(
        email="prof@mailinator.com", username="prof", password="asdf"
    )
    User.objects.get_or_create(
        email="ta@mailinator.com", username="ta", password="asdf"
    )
    User.objects.get_or_create(
        email="test1@mailinator.com", username="test1", password="asdf"
    )
    User.objects.get_or_create(
        email="test2@mailinator.com", username="test2", password="asdf"
    )
    User.objects.get_or_create(
        email="test3@mailinator.com", username="test3", password="asdf"
    )
    User.objects.get_or_create(
        email="test4@mailinator.com", username="test4", password="asdf"
    )
    User.objects.get_or_create(
        email="test5@mailinator.com", username="test5", password="asdf"
    )
