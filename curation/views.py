from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from resources.days.models import FavoriteDay
from resources.venues.models import FavoriteVenue

# # Create your views here.


def index(request):
    return render(request, "curation/curation_page.html")


@login_required(login_url="/authentication/login")
def favorite_day_dayvenue(request):
    user = request.user
    context = {}
    context["favorite_day"] = FavoriteDay.objects.filter(user=user)
    context["favorite_venue"] = FavoriteVenue.objects.filter(user=user)
    context["user"] = user
    return render(request, "curation/curation_page.html", context)
