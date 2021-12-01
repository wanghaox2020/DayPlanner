from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from dayplanner.services import yelp_client
from resources.days.models import Day, FavoriteDay, DayVenue
from resources.categories.models import Category
from resources.venues.models import FavoriteVenue

ERROR_FAV_NO_LOGIN = "To Save your Favourite day, Please Log in First"


def explore(requets):
    context = {}
    handle_message(requets, context)
    try:
        days = Day.objects.all().filter(is_active=True)
        day_list = []
        for day in days:
            if day.dayvenue_set.count() >= 1:
                if not requets.user.is_anonymous:
                    if day.favoriteday_set.filter(user=requets.user).count() == 1:
                        day_list.append({"day": day, "is_fav": True})
                    else:
                        day_list.append({"day": day, "is_fav": False})
                else:
                    day_list.append({"day": day, "is_fav": False})

        context["days"] = day_list
        context["cats"] = Category.objects.all()
    except Exception as e:
        return HttpResponse("Error Code: %s" % e)

    return render(requets, "explore/explore.html", context)


def explore_cats(requests, cat):
    context = {}
    handle_message(requests, context)

    try:
        cat_object = Category.objects.get(cat=cat)
        days = []
        for day in Day.objects.all():
            for cats in day.daycategory_set.all():
                if cats.cat == cat_object:
                    days.append(day)
        day_list = []
        for day in days:
            if day.dayvenue_set.count() >= 1:
                if not requests.user.is_anonymous:
                    if day.favoriteday_set.filter(user=requests.user).count() == 1:
                        day_list.append({"day": day, "is_fav": True})
                    else:
                        day_list.append({"day": day, "is_fav": False})
                else:
                    day_list.append({"day": day, "is_fav": False})

        context["days"] = day_list
        context["cats"] = Category.objects.all()
    except Exception as e:
        return HttpResponse("Error Code: %s" % e)

    return render(requests, "explore/explore.html", context)


def day_summary(requests, day_id):
    day = get_object_or_404(Day, pk=day_id)
    context = {}
    context["day"] = day
    context["active_categories"] = day.daycategory_set.all()
    DayVenues = day.dayvenue_set.all()
    fetch_list = []
    dayvenue_list = []

    handle_message(requests, context)

    for dv in DayVenues:
        if not requests.user.is_anonymous:
            if dv.venue.favoritevenue_set.filter(user=requests.user).count() == 1:
                dayvenue_list.append({"dayvenue": dv, "is_fav": True})
            else:
                dayvenue_list.append({"dayvenue": dv, "is_fav": False})
        else:
            dayvenue_list.append({"dayvenue": dv, "is_fav": False})
        fetch_list.append(dv.venue.yelp_id)
    context["dayvenue_list"] = dayvenue_list
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


def search_post_to_get(request):
    url = request.path
    get_url = url + "=" + request.POST["search_input"]
    return HttpResponseRedirect(get_url)


def search_handeler(request, search_key):
    context = {}
    handle_message(request, context)
    # if request.POST["search_input"] == "":
    #     return explore(request)
    try:
        # search_key = request.POST["search_input"]
        request.session["search_key"] = search_key
        days = Day.objects.all().filter(name__contains=search_key, is_active=True)
        day_list = []
        for day in days:
            if day.dayvenue_set.count() >= 1:
                if not request.user.is_anonymous:
                    if day.favoriteday_set.filter(user=request.user).count() == 1:
                        day_list.append({"day": day, "is_fav": True})
                    else:
                        day_list.append({"day": day, "is_fav": False})
                else:
                    day_list.append({"day": day, "is_fav": False})
        context["days"] = day_list
        context["cats"] = Category.objects.all()
    except Exception as e:
        return HttpResponse(e)
    return render(request, "explore/explore.html", context=context)


def favorite_day(request, day_id):
    last_url = request.GET.get("last")
    if request.user.is_anonymous:
        # Create a Error Message
        request.session["Error_Message"] = ERROR_FAV_NO_LOGIN
        return HttpResponseRedirect(last_url)

    # Create a FavoriteDay relation
    day = Day.objects.get(pk=day_id)
    FavoriteDay.objects.create(user=request.user, day=day)
    # Create a success Message
    msg = "Added %s to Favorite List" % day.name
    request.session["Success_Message"] = msg
    return HttpResponseRedirect(last_url)


def unfavorite_day(request, day_id):
    last_url = request.GET.get("last")
    if request.user.is_anonymous:
        request.session["error"] = ERROR_FAV_NO_LOGIN
        return HttpResponseRedirect(last_url)

    # Create a FavoriteDay relation
    day = Day.objects.get(pk=day_id)
    day.favoriteday_set.filter(user=request.user).delete()
    # Create a success Message
    msg = "Removed %s from Favorite List" % day.name
    request.session["Success_Message"] = msg

    return HttpResponseRedirect(last_url)


def favorite_venue(request, dayvenue_id):
    last_url = request.GET.get("last")
    if request.user.is_anonymous:
        # Create a Error Message
        request.session["Error_Message"] = ERROR_FAV_NO_LOGIN
        return HttpResponseRedirect(last_url)

    # Create a FavoriteDay relation
    dayvenue = DayVenue.objects.get(pk=dayvenue_id)
    venue = dayvenue.venue
    FavoriteVenue.objects.create(user=request.user, venue=venue)

    # create a success message
    msg = "Added venue from Favorite List"
    request.session["Success_Message"] = msg
    return HttpResponseRedirect(last_url)


def unfavorite_venue(request, dayvenue_id):
    last_url = request.GET.get("last")
    if request.user.is_anonymous:
        # Create a Error Message
        request.session["Error_Message"] = ERROR_FAV_NO_LOGIN
        return HttpResponseRedirect(last_url)
    # Remove a FavoriteDay relation
    dayvenue = DayVenue.objects.get(pk=dayvenue_id)
    venue = dayvenue.venue
    FavoriteVenue.objects.get(user=request.user, venue=venue).delete()
    # Create a success message
    msg = "Removed venue from Favorite List"
    request.session["Success_Message"] = msg
    return HttpResponseRedirect(last_url)


def handle_message(request, context):
    if "Error_Message" in request.session:
        context["error"] = request.session["Error_Message"]
        del request.session["Error_Message"]
    elif "Success_Message" in request.session:
        context["message"] = request.session["Success_Message"]
        del request.session["Success_Message"]
