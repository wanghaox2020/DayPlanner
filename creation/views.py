from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from dayplanner.services import yelp_client
from resources.days.models import Day, DayVenue
from resources.categories.models import Category, DayCategory
from resources.venues.models import Venue


def viewMap(request, day_id):
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
    return render(request, "creation/mappage.html", context)


def editPage(request, day_id):
    day = get_object_or_404(Day, pk=day_id)
    context = {}
    context["day"] = day
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

    if request.method == "GET":
        return render(request, "creation/editpage.html", context)

    elif request.method == "POST":
        day_name = request.POST["day_name"]
        day_description = request.POST["day_description"]
        try:
            currDay = Day.objects.get(id=day_id)
            currDay.name = day_name
            currDay.description = day_description
            currDay.save()
        except Exception as e:
            return HttpResponse("Error Code: %s" % e)
    return HttpResponseRedirect("/creation/%s/detail" % day.id)


def day_venue_up(request, day_id, dv_id):
    day = get_object_or_404(Day, pk=day_id)
    day_venues = day.dayvenue_set.all()
    try:
        day.day_venue_up(day_venues, dv_id)
    except Exception as e:
        return HttpResponse("Error Code: %s" % e)
    return HttpResponseRedirect("/creation/%s/edit" % day.id)


def day_venue_down(request, day_id, dv_id):
    day = get_object_or_404(Day, pk=day_id)
    day_venues = day.dayvenue_set.all()
    try:
        day.day_venue_down(day_venues, dv_id)
    except Exception as e:
        return HttpResponse("Error Code: %s" % e)
    return HttpResponseRedirect("/creation/%s/edit" % day.id)


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


def delete_dayvenue(request, day_id, dayvenue_id):
    day = get_object_or_404(Day, pk=day_id)
    try:
        day.delete_dayvenue(pk=dayvenue_id)
    except Exception as e:
        print("-- deletion error %s") % (e)

    return HttpResponseRedirect("/creation/%i/edit" % day_id)


def searchpage(request, day_id):
    # Initializing the context dict
    context = {}
    # Given day_id try to access the day object
    day = get_object_or_404(Day, pk=day_id)
    context["day"] = day

    if request.method == "GET":
        # Case the the user send a GET URL with a query String Yelp_id:<id>
        # For example: /creation/editday/1?yelp_id=x86
        # Is User want to added x86 into day 1
        if request.GET.get("yelp_id"):
            # The function addVenue Defined at line 32
            # Add Venue into current selected day and refresh the page
            return addVenue(request, day)

        return render(request, "creation/search_page.html", context)
    elif request.method == "POST":
        if request.GET.get("search"):
            return search(request, context)


def addVenue(request, day):
    yelp_id = request.GET.get("yelp_id")
    venue, created = Venue.objects.get_or_create(yelp_id=yelp_id)
    DayVenue.objects.create(day=day, venue=venue, pos=day.dayvenue_set.count() + 1)
    rootpath = request.path.split("/searchpage")[0]
    return HttpResponseRedirect(rootpath)


def search(request, context):
    # handle Search action in creation/editday?<day_id>
    user_input_param1 = request.POST["user_input_term"]
    user_input_param2 = request.POST["user_input_location"]

    business_data = yelp_client.search(user_input_param1, user_input_param2)
    if "businesses" not in business_data:
        context["error"] = "Your input is invalid"
        return render(request, "creation/search_page.html", context)

    context["search_results"] = business_data["businesses"]
    coordinates = []
    # [{"latitude":<lat_val>,"longitude":<long_val>,"name":<name>}]
    for business in business_data["businesses"]:
        data = business["coordinates"]
        data["name"] = business["name"]
        coordinates.append(data)
    context["coordinates"] = coordinates
    return render(request, "creation/search_page.html", context)


@login_required(login_url="/authentication/login")
def daylist(request):
    # userName is in string
    # Example: login as Admin the userName == "admin"
    if request.method == "POST":
        # create a new day here
        dayname = request.POST["day_name"]
        day = Day.objects.create(creator=request.user, name=dayname)
        return HttpResponseRedirect("/creation/%s/detail" % day.id)

    userObject = request.user
    context = {
        "userDayList": userObject.day_set.all().filter(is_active=True),
        "username": userObject.username,
    }
    return render(request, "creation/_day_list.html", context)


def edit_categories_page(request, day_id):
    day = get_object_or_404(Day, pk=day_id)
    cat_list = [daycat.cat for daycat in day.daycategory_set.all()]
    context = {
        "active_categories": day.daycategory_set.all(),
        "inactive_categories": Category.objects.all().exclude(cat__in=cat_list),
        "day": day,
    }
    return render(request, "creation/edit_category_page.html", context)


def add_daycategory(request, day_id, daycat_id):
    day = get_object_or_404(Day, pk=day_id)
    cat = get_object_or_404(Category, pk=daycat_id)
    try:
        DayCategory.objects.create(day=day, cat=cat)
    except Exception as e:
        print("-- Add error %s") % (e)
    return HttpResponseRedirect("/creation/%i/edit/categories" % day_id)


def remove_daycategory(request, day_id, daycat_id):
    day = get_object_or_404(Day, pk=day_id)
    daycat = get_object_or_404(DayCategory, pk=daycat_id)
    cat = get_object_or_404(Category, cat=daycat.cat)
    curr = DayCategory.objects.filter(day=day, cat=cat, pk=daycat_id)
    if len(curr) == 1:
        try:
            DayCategory.objects.get(pk=daycat_id).delete()
        except Exception as e:
            print("-- deletion error %s") % (e)
    return HttpResponseRedirect("/creation/%i/edit/categories" % day_id)
