from django.urls import path

from resources.days.views import DayListView
from resources.days.views import DayDetailView

app_name = 'resources.days'

urlpatterns = [
    path('<str:username>',DayListView.as_view(),name='list_of_days'),

    path('<int:pk>', DayDetailView.as_view(),name='detail_of_day'),
    # This one will not work


    path('<str:username>/<int:pk>', DayDetailView.as_view())
    # This one will work


    # ex. http://localhost:8000/resources/days/admin -> will show day_list admin has
    # ex. http://localhost:8000/resources/days/admin/2 -> will show the day detail of this day

    # However, The detail_of_day should not be under /days/admin/2, but /days/2.
    # I dont know where went wrong with my views.
]