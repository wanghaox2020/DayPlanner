
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Day

class DayDetailView(DetailView):
    model = Day
    template_name = 'days/_day_detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super(DayDetailView, self).get_context_data( *args, **kwargs)
        detail = get_object_or_404(Day, id=self.kwargs['pk'])
        context['detail'] = detail
        return context

class DayListView(ListView):
    model = Day
    template_name = 'days/_list_of_days.html'
    context_object_name = 'day_list'
    def get_queryset(self):
        queryset = super(DayListView, self).get_queryset()
        return queryset.filter(creator__username=self.kwargs['username'])

class AllDaysView(ListView):
    model = Day
    template_name = 'days/_all_days.html'
    context_object_name = 'all_days'
    def get_queryset(self):
        queryset = super(AllDaysView, self).get_queryset()
        return queryset

