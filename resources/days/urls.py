from django.urls import path
from resources.days.views import DayDetailView
from resources.days.views import  AllDaysView, DayListView

app_name = 'resources.days'

urlpatterns = [
    path('<int:pk>', DayDetailView.as_view(), name='day_detail'),
    path('<int:pk>/', DayDetailView.as_view(), name='day_detail'),
    path('', AllDaysView.as_view(),name='all_days'),
    path('<str:username>/',DayListView.as_view(),name='list_of_days'),

    # ex. http://localhost:8000/resources/days/admin/ -> will show day_list admin has
    # ex. http://localhost:8000/resources/days/1 -> will show the day detail of the day with primary key "1", in our Day model
]