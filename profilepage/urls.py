from django.urls import path
from .views import ProfileView

urlpatterns = [
    path('<int:pk>/',ProfileView.as_view(),name='show_profile_page')
]