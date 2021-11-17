from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from dayplanner.services import yelp_client
from resources.days.models import Day


def explore(requets):
    context = {}
    try:
        days = Day.objects.all().filter(is_active=True)
        context["days"] = [day for day in days if day.dayvenue_set.count() >= 1]
    except Exception as e:
        return HttpResponse("Error Code: %s" % e)

    return render(requets, "explore/explore.html", context)


def day_summary(requests, day_id):
    day = get_object_or_404(Day, pk=day_id)
    context = {}
    context["day"] = day
    context["active_categories"] = day.daycategory_set.all()
    DayVenues = day.dayvenue_set.all()
    fetch_list = []
    for dv in DayVenues:
        fetch_list.append(dv.venue.yelp_id)

    responses = yelp_client.fetch_many(fetch_list)
    coordinates = []
    # [{"latitude":<lat_val>,"longitude":<long_val>,"name":<name>}]
    for resp in responses:
        data = resp["coordinates"]
        data["name"] = resp["name"]
        coordinates.append(data)
    context["coordinates"] = coordinates

    return render(requests, "explore/day_summary.html", context)


def fork(request, day_id):
    day = get_object_or_404(Day, pk=day_id)

    new_day = day.fork(request.user)
    return HttpResponseRedirect("/creation/%i/edit" % new_day.id)
