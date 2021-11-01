from django.urls import path
from . import views
from .views import DayvenueListView

app_name = "creation"

urlpatterns = [
    path("", views.daylist),
    path("edit/<int:pk>", DayvenueListView.as_view(), name="editpage"),
    path("delete_day", views.deleteday),
]
