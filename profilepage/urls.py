from django.urls import path
from .views import ProfileView
from . import views


urlpatterns = [
    path("<int:pk>/", ProfileView.as_view(), name="show_profile_page"),
    # ex. lhttp://localhost:8000/profilepage/1/
    # pk is the primary key in User Model
    path("private", views.make_profile_private),
    path("public", views.make_profile_public),
]
