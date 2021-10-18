from django.urls import path
from . import views
from .views import ProfileView

urlpatterns = [
    path('signup',views.register_view),
    path('login',views.login_view),
    path('index',views.index_view),
    path('logout',views.logout),
    path('<int:pk>/',ProfileView.as_view(),)
]