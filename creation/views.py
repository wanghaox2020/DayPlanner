from django.shortcuts import render
from dayplanner.services import yelp_client

from resources.venues.models import Venue


def search(request):
    if request.method == "GET":
        return render(request, "creation/index.html")
    elif request.method == "POST":
        context = {}
        user_input_param1 = request.POST["user_input_term"]
        user_input_param2 = request.POST["user_input_location"]

        bussiness_data = yelp_client.search(user_input_param1, user_input_param2)

        context["search_results"] = bussiness_data["businesses"]

        # Model creation
        # for bussness in bussiness_data['businesses']:
        #     try:
        #         Venue.objects.create(yelp_id=bussness["id"])
        #     except:
        #         continue

        return render(request, "creation/index.html", context)
