from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from dayplanner.services import yelp_client
from resources.days.models import Day, FavoriteDay
from resources.categories.models import Category


def explore(requets):
    context = {}
    try:
        days = Day.objects.all().filter(is_active=True)
        List = []
        for day in days:
            if day.dayvenue_set.count() >= 1:
                if not requets.user.is_anonymous:
                    if day.favoriteday_set.filter(user=requets.user).count() == 1:
                        List.append({"day": day, "is_fav": True})
                    else:
                        List.append({"day": day, "is_fav": False})
                else:
                    List.append({"day": day, "is_fav": False})

        context["days"] = List
        context["cats"] = Category.objects.all()
    except Exception as e:
        return HttpResponse("Error Code: %s" % e)

    return render(requets, "explore/explore.html", context)


def explore_cats(requests, cat):
    context = {}
    try:
        cat_object = Category.objects.get(cat=cat)
        days = []
        for day in Day.objects.all():
            for cats in day.daycategory_set.all():
                if cats.cat == cat_object:
                    days.append(day)
        List = []
        for day in days:
            if day.dayvenue_set.count() >= 1:
                if not requests.user.is_anonymous:
                    if day.favoriteday_set.filter(user=requests.user).count() == 1:
                        List.append({"day": day, "is_fav": True})
                    else:
                        List.append({"day": day, "is_fav": False})
                else:
                    List.append({"day": day, "is_fav": False})

        context["days"] = List
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


def search_handeler(request):
    context = {}
    search_key = request.POST["search_input"]
    if search_key == "":
        return explore(request)
    try:
        context["days"] = Day.objects.all().filter(
            name__contains=search_key, is_active=True
        )
        context["cats"] = Category.objects.all()
    except Exception as e:
        return HttpResponse(e)
    return render(request, "explore/explore.html", context=context)


@login_required(login_url='/example url you want redirect/')
def favorite(request, day_id):
    if request.user.is_anonymous:
        return send_login_errormessage(request)

    last_url = request.GET.get("last")
    # Create a FavoriteDay relation
    day = Day.objects.get(pk=day_id)
    FavoriteDay.objects.create(user=request.user, day=day)

    return HttpResponseRedirect(last_url)


def unfavorite(request, day_id):
    if request.user.is_anonymous:
        return send_login_errormessage(request)

    last_url = request.GET.get("last")
    # Create a FavoriteDay relation
    day = Day.objects.get(pk=day_id)
    day.favoriteday_set.filter(user=request.user).delete()

    return HttpResponseRedirect(last_url)


def send_login_errormessage(request):
    context = {}
    try:
        days = Day.objects.all().filter(is_active=True)
        List = []
        for day in days:
            if day.dayvenue_set.count() >= 1:
                List.append({"day": day, "is_fav": False})

        context["days"] = List
        context["cats"] = Category.objects.all()
        context["error"] = "Please Login to Save Your Favorite Day"
    except Exception as e:
        return HttpResponse("Error Code: %s" % e)

    return render(request, "explore/explore.html", context)
