from django.db.models import Model
from django.shortcuts import render
from dayplanner.services import yelp_client
import requests, json, os
from dayplanner.settings import YELP_API
from .models import Venue

# Create your views here.
Sampe_ID =  "WavvLdfdP6g8aZTtbBQHTw"

def index(request):
    return render(request, 'venues/_index.html', {
        'venues': Venue.objects.all()
    })

def detail(request, yelp_id):
    business_detail = yelp_client.fetch_by_id(yelp_id)

    return render(request, 'venues/_detail.html', business_detail)

def search_view(request):

    if request.method == 'GET':
        return render(request, 'venues/_search.html')
    elif request.method =='POST':
        context = {}
        user_input = request.POST['user_input']
        bussiness_data = yelp_client.search(user_input)


        context['data'] = bussiness_data['businesses']

        # Model creation
        # for bussness in bussiness_data['businesses']:
        #     try:
        #         Venue.objects.create(yelp_id=bussness["id"])
        #     except:
        #         continue


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
