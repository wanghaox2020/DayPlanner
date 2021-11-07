from django.urls import path
from . import views

app_name = "creation"

urlpatterns = [
    path("", views.daylist),
    path("<int:day_id>/detail", views.viewMap),
    path("edit/<int:day_id>", views.editPage),
    path("edit/<int:day_id>/searchpage", views.searchpage),
    path("delete_day", views.deleteday),
]
