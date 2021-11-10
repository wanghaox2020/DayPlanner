from django.urls import path
from . import views

app_name = "creation"

urlpatterns = [
    path("", views.daylist),
    path("<int:day_id>/detail", views.viewMap),
    path("<int:day_id>/edit", views.editPage),
    path("<int:day_id>/edit/searchpage", views.searchpage),
    path("delete_day", views.deleteday),
]
