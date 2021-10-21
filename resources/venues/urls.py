from django.urls import path
from . import views

app_name = "resources.venues"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:venue_id>", views.detail),
    # path('for_yelp_id/<str:yelp_id>', views.sample_yelp_output(), name='sample_yelp_output'),
    path(
        "for_yelp_id/<str:yelp_id>",
        views.sample_yelp_single_output,
        name="sample_yelp_single_output",
    ),
    path("search", views.search_view),
]
