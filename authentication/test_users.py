def create_test_users():
    from django.contrib.auth import get_user_model
    from django.db import transaction

    User = get_user_model()

    usernames = ["prof", "ta", "test1", "test2", "test3", "test4", "test5"]

    for username in usernames:
        try:
            with transaction.atomic():
                existing_user = User.objects.filter(username=username).first()
                if existing_user:
                    continue

                User.objects.create_user(
                    email="%s@mailinator.com" % username,
                    username=username,
                    password="asdf",
                )
        except Exception as e:
            print("Encountered Error while creating test users:\n%s" % e)
            break
