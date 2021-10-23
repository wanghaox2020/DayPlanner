import json

from django.shortcuts import render, get_object_or_404
from .models import Venue

# Create your views here.
def index(request):
    return render(request, 'venues/_index.html', {
        'venues': Venue.objects.all()
    })

def detail(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    context = {
        'venue': venue,
        'raw_yelp_data': venue.raw_yelp_data()
    }
    return render(request, 'venues/_detail.html', context)

def for_yelp_id(request, yelp_id):
     venue, is_created = Venue.objects.get_or_create(yelp_id=yelp_id)
     data = venue.raw_yelp_data()
     context = {
         'dict': data,
         'json': json.dumps(data, indent=2)
     }
     return render(request, 'venues/for_yelp_id.html', context)