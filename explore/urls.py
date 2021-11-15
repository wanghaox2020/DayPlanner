from django.urls import path
from . import views
app_name = "explore"


urlpatterns = [
    path("", views.explore),
    path("<int:day_id>", views.day_summary)
]