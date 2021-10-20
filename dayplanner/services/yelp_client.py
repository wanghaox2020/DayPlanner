import requests, json
from dayplanner.settings import YELP_API

Search_endpoint = 'https://api.yelp.com/v3/businesses/search'
Detail_endpoint = 'https://api.yelp.com/v3/businesses/%s'
search_cache = {}
Detail_cache = {}


# input: yelp id
# output will be a python dict
def fetch_by_id(yelp_id):
    if yelp_id in Detail_cache:
        print("Cache Hit!")
        return Detail_cache[yelp_id]

    print("Cache Miss!")

    req = YelpRequest(
        endpoint=Detail_endpoint % yelp_id,
    )

    response = req.execute()

    Detail_cache[yelp_id] = response

    return response



# input: List of yelp ids
# output: List of python dict
def fetch_many(yelp_ids):
    pass

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
        endpoint= Search_endpoint ,
        params= parameters,
    )

    # search Result is a python dict in the form of YELP JSON
    # Refer to https://www.yelp.com/developers/documentation/v3/business_search
    searchResult = req.execute()
    search_cache[term_location] = searchResult

    return searchResult


class YelpRequest:
    def __init__(self,endpoint,params={}):
        self.endpoint = endpoint
        self.params = params
        self.headers = {'Authorization': 'Bearer %s' % YELP_API}

    def execute(self):
        return requests.get(url=self.endpoint,
                     headers=self.headers,
                     params=self.params).json()

