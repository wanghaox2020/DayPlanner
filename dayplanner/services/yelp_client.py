import requests, json
from dayplanner.settings import YELP_API

key ='CL1ez7IjEGAsK5LINl-ehN8lTuQSaOqP8NncZD0e8JRLcOmmACCc3u87rtD7l1Bwpc9uzwQF8Oj2K6lo7f9cHo2P6xhlCFSI6Thph0MaRgRDcM4XA6iww7AX8QROYXYx'
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
    responses = []
    # A single connection can reuse the same TCP connection between requests
    with requests.Session() as conn:
        for yelp_id in yelp_ids:
            if yelp_id in Detail_cache:
                responses.append(Detail_cache[yelp_id])
            else:
                req = YelpRequest(
                    endpoint=Detail_endpoint % yelp_id,
                    conn=conn
                )
                response = req.execute()
                Detail_cache[yelp_id] = response
                responses.append(response)
    
    return responses



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

