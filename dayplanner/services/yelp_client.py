import requests, json
from dayplanner.settings import YELP_API

key ='CL1ez7IjEGAsK5LINl-ehN8lTuQSaOqP8NncZD0e8JRLcOmmACCc3u87rtD7l1Bwpc9uzwQF8Oj2K6lo7f9cHo2P6xhlCFSI6Thph0MaRgRDcM4XA6iww7AX8QROYXYx'
Search_endpoint = 'https://api.yelp.com/v3/businesses/search'
Detail_endpoint = 'https://api.yelp.com/v3/businesses/{id}'
search_cache = {}
Detail_cache = {}


# input: yelp id
# output will be a python dict
def fetch_by_id(yelp_id):
    pass
# input: List of yelp ids
# output: List of python dict
def fetch_many(yelp_ids):
    pass

# example paramerters
# parameters = {'term':'coffee', 'limit':5, 'radius': 10000,'location': location}
def search(location):

    if location in search_cache:
        print("Cache Hit")
        return search_cache[location]

    print("Cache Missed")
    req = YelpRequest(
        endpoint= Search_endpoint ,
        params= {'term':'coffee', 'limit':5, 'radius': 10000,'location': location},
    )
    # search Result is a python dict in the form of YELP JSON
    # Refer to https://www.yelp.com/developers/documentation/v3/business_search
    searchResult = req.execute()

    search_cache[location] = searchResult

    return searchResult


class YelpRequest:
    def __init__(self,endpoint,params):
        self.endpoint = endpoint
        self.params = params
        self.headers = {'Authorization': 'Bearer %s' % YELP_API}
    def execute(self):
        return requests.get(url=self.endpoint,
                     headers=self.headers,
                     params=self.params).json()

