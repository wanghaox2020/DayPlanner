from django.urls import path
from user import views

urlpatterns = [
    path('signup',views.register_view),
    path('login',views.login_view),
    path('index',views.index_view),
    path('logout',views.logout),
]