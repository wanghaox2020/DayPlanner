from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class userInfo(AbstractUser):
    phonenumber = models.CharField(max_length=11,default="")

