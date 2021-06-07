"""
fragdenstaat_client.api - HTTP request module that implements a basic RESTful API client (does not handle pagination automatically)
"""import requests
from urllib.parse import urljoin


# According to the API docs (https://froide.readthedocs.io/en/latest/api/):
#
# GET requests do not need to be authenticated. POST, PUT and DELETE requests have to either carry a valid session
# cookie and a CSRF token or provide user name (you find your user name on your profile) and password via Basic
# Authentication.


class APIClient(object):
    """Makes HTTP requests to the fragdenstaat API (https://froide.readthedocs.io/en/latest/api/)
    """
    base_url = "https://fragdenstaat.de/"

    def __init__(self):
        """class constructor method, instantiates a requests.Session() that uses "connection pooling" to handle a large number of TCP connections
        """
        # full documentation here https://docs.python-requests.org/en/latest/api/#request-sessions
        self.http = requests.Session()

    def make_url(self, path: str):
        """takes a Request-URI path and concatenates it to the base URL
        """
        # request-URI is the correct name for "path" https://datatracker.ietf.org/doc/html/rfc2616#section-5.1.2 
        return urljoin(self.base_url, path)

    def retrieve_requests(self, offset):
        """downloads a list of requests from fragdenstaat
        """
        url = self.make_url(f"/api/v1/request/?format=json&offset={offset}")
        # makes the GET http request
        response = self.http.get(url)
        # returns the json response
        return response.json()
