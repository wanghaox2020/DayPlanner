from django.urls import path
from . import views

app_name = 'resources.venues'

urlpatterns = [
    path('', views.index),
    path('<int:venue_id>', views.detail),
    path('for_yelp_id/<str:yelp_id>', views.for_yelp_id),
]
