from django.urls import path
from . import views

app_name = "creation"

urlpatterns = [
    path("", views.daylist),
    path("editday/<int:day_id>", views.editday),
    path("delete_day", views.deleteday),
    path("editday/<int:day_id>/viewmap", views.viewMap),
]
