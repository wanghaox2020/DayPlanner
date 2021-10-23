from django.core.cache import caches
from dayplanner.settings import YELP_API
import requests, json

search_endpoint = 'https://api.yelp.com/v3/businesses/search'
detail_endpoint = 'https://api.yelp.com/v3/businesses/%s'

search_cache = caches['yelp_search']
business_cache = caches['yelp_businesses']


# input: yelp id
# output will be a python dict
def fetch_by_id(yelp_id):
    if yelp_id in business_cache:
        print("Cache Hit!")
        return business_cache[yelp_id]

    print("Cache Miss!")

    req = YelpRequest(
        endpoint=detail_endpoint % yelp_id,
    )

    response = req.execute()

    business_cache[yelp_id] = response

    return response



# input: List of yelp ids
# output: List of python dict
def fetch_many(yelp_ids):
    responses = []
    # A single conn can reuse the same TCP connection between requests
    with requests.Session() as conn:
        for yelp_id in yelp_ids:
            if yelp_id in business_cache:
                responses.append(business_cache[yelp_id])
            else:
                req = YelpRequest(
                    endpoint=detail_endpoint % yelp_id,
                    conn=conn
                )
                response = req.execute()
                business_cache[yelp_id] = response
                responses.append(response)

    return responses



# example paramerters
# parameters = {'term':'coffee', 'limit':5, 'radius': 10000,'location': location}

def search(term, location):


    term_location = term + location

    if term_location in search_cache:
        print("Cache Hit")
        return search_cache[term_location]

    print("Cache Missed")
    parameters = {'term': term, 'limit':5, 'radius': 10000}
    if "Latitude:" in location and "Longitude:" in location:
        args = location.split(' ')
        lat = args[1]
        long = args[3]
        parameters['latitude'] = lat
        parameters['longitude'] = long
    else:
        parameters['location'] = location

    req = YelpRequest(
        endpoint= search_endpoint ,
        params= parameters,
    )

    # search Result is a python dict in the form of YELP JSON
    # Refer to https://www.yelp.com/developers/documentation/v3/business_search
    searchResult = req.execute()
    search_cache[term_location] = searchResult

    return searchResult

# If initialized with a conn object, YelpRequest will use it
# to make HTTP requests.
class YelpRequest:
    # conn is a requests Session object
    def __init__(self,endpoint,params={},conn=None):
        self.endpoint = endpoint
        self.params = params
        self.conn = conn
        self.headers = {'Authorization': 'Bearer %s' % YELP_API}

    def execute(self):
        conn = self.conn or requests
        return conn.get(url=self.endpoint,
                     headers=self.headers,
                     params=self.params).json()

