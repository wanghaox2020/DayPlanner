from django.shortcuts import render


def index(request):
    return render(request, "dayplanner/index.html")


def about(request):
    return render(request, "dayplanner/about.html")
