from django.shortcuts import render
import requests, json, os
from dayplanner.settings import YELP_API,SECRET_KEY
from .models import Venue

# Create your views here.
key ='CL1ez7IjEGAsK5LINl-ehN8lTuQSaOqP8NncZD0e8JRLcOmmACCc3u87rtD7l1Bwpc9uzwQF8Oj2K6lo7f9cHo2P6xhlCFSI6Thph0MaRgRDcM4XA6iww7AX8QROYXYx'
def index(request):
    return render(request, 'venues/_index.html', {
        'venues': Venue.objects.all()
    })

def detail(request):
    return render(request, 'venues/_detail.html')

def search_view(request):

    if request.method == 'GET':
        return render(request, 'venues/_search.html')
    elif request.method =='POST':
        user_input = request.POST['user_input']

        endpoint = 'https://api.yelp.com/v3/businesses/search'
        x = YELP_API
        y = SECRET_KEY
        Headers = {'Authorization': 'Bearer %s' % key}
        parameters = {'term':'coffee', 'limit':5, 'radius': 10000,'location': user_input}
        context = {}

        # make a request to the yelp API
        #resp = requests.request('GET',url=endpoint,params=parameters,headers=Headers)
        resp = requests.get(url= endpoint, headers=Headers,params=parameters)

        # convert the JSON string to a Dict
        bussiness_data = resp.json()
        context['data'] = bussiness_data['businesses']

        return render(request,"venues/_sample_yelp_output.html",context)










def getYelp_id():
    return None





def sampleYelpOutput(request, yelp_id):
    headers = {'Authorization': 'Bearer %s' % YELP_API}
    url = 'https://api.yelp.com/v3/businesses/%s' % yelp_id
    response = requests.get(url, headers = headers)
    business_date = response.json()
    businessStr = json.dumps(business_date, indent = 3)
    return render(request, 'venues/_sample_yelp_output.html', {
        'data': businessStr
    })
