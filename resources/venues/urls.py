from django.urls import path
from . import views

app_name = 'resources.venues'

urlpatterns = [
    path('', views.index),
    path('<int:venue_id>', views.detail),
]
