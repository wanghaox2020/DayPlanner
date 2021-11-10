from django.urls import path
from . import views

app_name = "creation"

urlpatterns = [
    path("", views.daylist),
    path("<int:day_id>/detail", views.viewMap),
    path("<int:day_id>/edit", views.editPage),
    path("<int:day_id>/edit/searchpage", views.searchpage),
    path("<int:day_id>/edit/delete_dayvenue/<int:dayvenue_id>", views.delete_dayvenue),
    path("delete_day", views.deleteday),
]
