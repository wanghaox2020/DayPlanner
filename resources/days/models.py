from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Day(models.Model):
    # primary key is auto generated by django
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=False)
