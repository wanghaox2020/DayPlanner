from django.contrib import admin
from .models import Venue
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Venue

