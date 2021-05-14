from urllib.parse import urljoin


class APIRouter(object):
    base_url = "https://fragdenstaat.de/"

    def make_url(self, path: str):
        return urljoin(self.base_url, path)

    @property
    def token_url(self) -> str:
        return self.make_url("/account/token")

