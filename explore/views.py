from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from dayplanner.services import yelp_client
from resources.days.models import Day
from resources.categories.models import Category


def explore(requets):
    context = {}
    try:
        days = Day.objects.all().filter(is_active=True)
        context["days"] = [day for day in days if day.dayvenue_set.count() >= 1]
        context["cats"] = [cat for cat in Category.objects.all()]
        print(context["cats"])
    except Exception as e:
        return HttpResponse("Error Code: %s" % e)

    return render(requets, "explore/explore.html", context)


def explore_tags(requests, tag):
    context = {}
    try:
        Tag = Category.objects.get(cat=tag)
        days = []
        for day in Day.objects.all():
            for tags in day.daycategory_set.all():
                if tags.cat == Tag:
                    days.append(day)

        context["days"] = [day for day in days if day.dayvenue_set.count() >= 1]
        context["cats"] = [cat for cat in Category.objects.all()]
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
        context["days"] = Day.objects.all().filter(name__contains=search_key,is_active=True)
    except Exception as e:
        return HttpResponse(e)
    return render(request, "explore/explore.html",context=context)
