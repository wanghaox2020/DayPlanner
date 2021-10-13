from django.shortcuts import render

# Create your views here.

# def index(request):
#     return render(request, 'venues/index.html')

def detail(request):
    return render(request, 'venues/_detail.html')