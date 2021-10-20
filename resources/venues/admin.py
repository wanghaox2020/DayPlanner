from django.contrib import admin
from .models import Venue
# Register your models here.

class VenueManage(admin.ModelAdmin):
    list_display = ['yelp_id']

admin.site.register(Venue,VenueManage)
