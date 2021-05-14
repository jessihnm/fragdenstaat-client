import os
import requests
from pathlib
from typing import Optional
from urllib.parse import urljoin
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


# API docs: https://froide.readthedocs.io/en/latest/api/


class Configuration(object):
    defaults = dict(
        # https://fragdenstaat.de/account/applications/
        FRAG_DEN_STAAT_CLIENT_ID="",
        FRAG_DEN_STAAT_CLIENT_SECRET=""
    )

    def get_client_id(self):
        return self.get_config("FRAG_DEN_STAAT_CLIENT_ID")

    def get_client_secret(self):
        return self.get_config("FRAG_DEN_STAAT_CLIENT_SECRET")

    def get_config(self, key: str) -> Optional[str]:
        return os.getenv(key) or self.defaults.get(key, "")


class APIRouter(object):
    base_url = "https://fragdenstaat.de/"

    def make_url(self, path: str):
        return urljoin(self.base_url, path)

    @property
    def token_url(self) -> str:
        return self.make_url("/account/token")


class Authenticator(object):
    routes = APIRouter()

    def __init__(self, config: Configuration):
        self.client = BackendApplicationClient(client_id=config.get_client_id())
        self.oauth = OAuth2Session(client=self.client)
        self.config = config

    def authenticate(self):
        token = self.oauth.fetch_token(
            token_url=self.routes.token_url, 
            client_id=self.config.get_client_id(),
            client_secret=self.config.get_client_secret()
        )
        return token


class APIClient(object):
    routes = APIRouter()
    token = None

    def __init__(self, auth: Authenticator):
        self.auth = auth
        self.http = requests.Session()

    def authenticate(self):
        if not self.token:
            self.token = self.auth.authenticate()

        self.http.headers["Authentication"] = f"Bearer {self.token}"

    def retrieve_requests(self):
        url = self.routes.make_url("/api/v1/request")
        response = self.http.get(url)
        return response.json()
