
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Day
  
class DayListView(ListView):
    model = Day
    template_name = 'days/list_of_days.html'
    context_object_name = 'day_list'
    def get_queryset(self):
        queryset = super(DayListView, self).get_queryset()
        return queryset.filter(user__username=self.kwargs['username'])

# Problems with this one!!
class DayDetailView(DetailView):
    model = Day
    template_name = 'days/day_detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super(DayDetailView, self).get_context_data( *args, **kwargs)
        details = get_object_or_404(Day, id=self.kwargs['pk'])
        context['details'] = details
        return context
