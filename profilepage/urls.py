from django.urls import path
from .views import ProfileView

urlpatterns = [
    path("<int:pk>/", ProfileView.as_view(), name="show_profile_page")
    # ex. lhttp://localhost:8000/profilepage/1/
    # pk is the primary key in User Model
]
