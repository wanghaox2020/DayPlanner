from django.urls import path
from . import views

app_name = "explore"


urlpatterns = [
    path("", views.explore),
    path("<int:day_id>", views.day_summary),
    path("<int:day_id>/fork", views.fork),
    path("search", views.search_handeler),
    path("search/<str:tag>", views.explore_cats),
]
