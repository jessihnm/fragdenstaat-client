import requests
from urllib.parse import urljoin


class APIRouter(object):
    base_url = "https://fragdenstaat.de/"

    def make_url(self, path: str):
        return urljoin(self.base_url, path)

    @property
    def token_url(self) -> str:
        return self.make_url("/account/token")


# According to the API docs (https://froide.readthedocs.io/en/latest/api/):
#
# GET requests do not need to be authenticated. POST, PUT and DELETE requests have to either carry a valid session
# cookie and a CSRF token or provide user name (you find your user name on your profile) and password via Basic
# Authentication.


class APIClient(object):
    routes = APIRouter()
    auth = None

    def __init__(self, username=None, password=None):
        self.http = requests.Session()
        if username and password:
            self.http.auth = self.auth = HTTPBasicAuth(username, password)

    def authenticate(self, username=None, password=None):
        if username and password:
            self.auth = HTTPBasicAuth(username, password)
        self.http.auth = self.auth

    def retrieve_requests(self):
        url = self.routes.make_url("/api/v1/request")
        response = self.http.get(url)
        return response.json()
