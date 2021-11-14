from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from resources.days.models import Day


def explore(requets):
    context = {}
    with transaction.atomic():
        try:
            days = Day.objects.all()
            context["days"] = days
        except Exception as e:
            return HttpResponse("Error Code: %s" % e)

    return render(requets,"explore/explore.html",context)