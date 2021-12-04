from django.db import models
from django.contrib.auth.models import User

# from django.db.models.signals import post_save

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    is_private = models.BooleanField(default=False)


# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# post_save.connect(create_user_profile, sender=User)
