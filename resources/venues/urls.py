from django.urls import path
from . import views

app_name = 'resources.venues'

urlpatterns = [
    path('', views.index, name='index'),
    path('for_yelp_id/<str:yelp_id>', views.sampleYelpOutput, name='sampleYelpOutput'),
]
