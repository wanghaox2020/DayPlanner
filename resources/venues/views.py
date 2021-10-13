from django.shortcuts import render
import requests, json, os
from dayplanner.settings import YELP_API
from .models import Venue

# Create your views here.

def index(request):
    return render(request, 'venues/_index.html', {
        'venues': Venue.objects.all()
    })

def detail(request):
    return render(request, 'venues/_detail.html')

def sampleYelpOutput(request, yelp_id):
    headers = {'Authorization': 'Bearer %s' % YELP_API}
    url = 'https://api.yelp.com/v3/businesses/%s' % yelp_id
    response = requests.get(url, headers = headers)
    business_date = response.json()
    businessStr = json.dumps(business_date, indent = 3)
    return render(request, 'venues/_sample_yelp_output.html', {
        'data': businessStr
    })
