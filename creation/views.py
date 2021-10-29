from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from dayplanner.services import yelp_client
from django.contrib.auth.models import User
from resources.days.models import Day, DayVenue
from resources.venues.models import Venue


def editday(request):
    context = {}
    day_id = request.GET.get("day_id")

    try:
        day = Day.objects.get(id=day_id)
        context["day"] = day

    except Exception:
        return HttpResponse("--The day is not existed")

    if request.method == "GET":
        if request.GET.get("yelp_id"):
            addVenue(request, day)

        return render(request, "creation/editday.html", context)
    elif request.method == "POST":
        if request.GET.get("search"):
            return search(request, context)


def addVenue(request, day):
    yelp_id = request.GET.get("yelp_id")
    venue, created = Venue.objects.get_or_create(yelp_id=yelp_id)
    DayVenue.objects.create(day=day, venue=venue, pos=day.dayvenue_set.count() + 1)
    return HttpResponseRedirect(request.path_info)


def search(request, context):
    # handle Search action in creation/editday?<day_id>
    user_input_param1 = request.POST["user_input_term"]
    user_input_param2 = request.POST["user_input_location"]

    bussiness_data = yelp_client.search(user_input_param1, user_input_param2)
    context["search_results"] = bussiness_data["businesses"]

    return render(request, "creation/editday.html", context)


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

    userName = "admin"
    userObject = User.objects.get(username="admin")
    context = {
        "userDayList": userObject.day_set.all().filter(is_active=True),
        "username": userName,
    }
    return render(request, "creation/day_list.html", context)
