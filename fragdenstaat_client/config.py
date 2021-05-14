import os
from typing import Optional


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

