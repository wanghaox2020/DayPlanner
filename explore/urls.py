from django.urls import path
from . import views

app_name = "explore"


urlpatterns = [
    path("", views.explore),
    path("<int:day_id>", views.day_summary),
    path("<int:day_id>/fork", views.fork),
    path("search", views.search_handeler),
    path("search/<str:cat>", views.explore_cats),
    path("favorite_day/<int:day_id>", views.favorite_day),
    path("unfavorite_day/<int:day_id>", views.unfavorite_day),
    path("favorite_venue/<int:dayvenue_id>", views.favorite_venue),
    path("unfavorite_venue/<int:dayvenue_id>", views.unfavorite_venue),
]
