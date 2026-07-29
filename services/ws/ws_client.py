from websockets.asyncio.client import connect
from settings import settings


class WSClient:
    def __init__(self, token=None):
        self.ws_base_url = settings.get("WS_URL")
        self._token = token

    def connect(self, path: str):
        url = f"{self.ws_base_url}{path}"

        return connect(url)
