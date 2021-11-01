from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from dayplanner.services import yelp_client
from django.contrib.auth.models import User
from resources.days.models import Day, DayVenue
from resources.venues.models import Venue

def viewMap(request, day_id):
    day = get_object_or_404(Day, pk=day_id)
    context = {}
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
    return render(request, "creation/mappage.html",context)

def deleteday(request):
    day_id = request.GET.get("day_id")
    if not day_id:
        return HttpResponse("--- Deletion request cannot be processed")
    try:
        day = Day.objects.get(id=day_id, is_active=True)
        day.is_active = False
        day.save()
    except Exception as e:
        print("-- deletion error %s") % (e)

    return HttpResponseRedirect("/creation")


def daylist(request):
    # userName is in string
    # Example: login as Admin the userName == "admin"
    if request.method == "POST":
        # create a new day here
        dayname = request.POST["day_name"]
        Day.objects.create(creator=request.user, name=dayname)

    userObject = request.user
    context = {
        "userDayList": userObject.day_set.all().filter(is_active=True),
        "username": userObject.username,
    }
    return render(request, "creation/_day_list.html", context)  


 