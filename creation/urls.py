from django.urls import path
from . import views

app_name = "creation"

urlpatterns = [
    path("", views.daylist),
    path("editday", views.editday),
    path("delete_day", views.deleteday),
]
