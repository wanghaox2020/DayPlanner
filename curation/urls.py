from django.urls import path
from . import views

app_name = "curation"

urlpatterns = [
    path("", views.favorite_day_dayvenue),
]
