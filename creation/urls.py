from django.urls import path
from . import views

app_name = "creation"

urlpatterns = [
    path("", views.daylist),
    path("edit/<int:day_id>", views.viewMap),
    path("delete_day", views.deleteday),
]
