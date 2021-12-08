def create_test_users():
    from django.contrib.auth import get_user_model
    from django.db import transaction
    from profilepage.models import Profile

    User = get_user_model()

    usernames = ["prof", "ta", "test1", "test2", "test3", "test4", "test5"]
    for username in usernames:
        try:
            with transaction.atomic():
                existing_user = User.objects.filter(username=username).first()
                if existing_user:
                    continue

                user = User.objects.create_user(
                    email="%s@mailinator.com" % username,
                    username=username,
                    password="asdf",
                )
                Profile.objects.create(user=user)
        except Exception as e:
            print("Encountered Error while creating test users:\n%s" % e)
            break
