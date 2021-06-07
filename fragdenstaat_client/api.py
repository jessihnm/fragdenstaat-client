import requests
from urllib.parse import urljoin


# According to the API docs (https://froide.readthedocs.io/en/latest/api/):
#
# GET requests do not need to be authenticated. POST, PUT and DELETE requests have to either carry a valid session
# cookie and a CSRF token or provide user name (you find your user name on your profile) and password via Basic
# Authentication.


class APIClient(object):
    base_url = "https://fragdenstaat.de/"

    def __init__(self):
        self.http = requests.Session()

    def make_url(self, path: str):
        return urljoin(self.base_url, path)

    def retrieve_requests(self, offset):
        url = self.make_url(f"/api/v1/request/?format=json&offset={offset}")
        response = self.http.get(url)
        return response.json()
