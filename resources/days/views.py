from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Day, DayVenue
from resources.venues.models import Venue


class DayDetailView(DetailView):
    model = Day
    template_name = "days/_day_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DayDetailView, self).get_context_data(*args, **kwargs)
        detail = get_object_or_404(Day, id=self.kwargs["pk"])
        context["detail"] = detail
        return context


class DayListView(ListView):
    model = Day
    template_name = "days/_list_of_days.html"
    context_object_name = "day_list"

    def get_queryset(self):
        queryset = super(DayListView, self).get_queryset()
        return queryset.filter(creator__username=self.kwargs["username"])


class AllDaysView(ListView):
    model = Day
    template_name = "days/_all_days.html"
    context_object_name = "all_days"



def edit(request, day_id):
    day = Day.objects.get(pk=day_id)

    if request.method == "POST":
        yelp_id  = request.POST["yelp_id"]
        venue = Venue.objects.get_or_create(yelp_id=yelp_id)
        DayVenue.objects.create(day=day, venue=venue)
    
    return render(request, "days/_edit.html", {'day': day})