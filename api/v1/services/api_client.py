import httpx


class APIClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url.rstrip('/')
        self._token = token
        self._client = httpx.AsyncClient(timeout=30.0)

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    async def get(self, path, **kwargs):
        return await self._client.get(f"{self.base_url}{path}", headers=self._headers(), **kwargs)

    async def post(self, path, **kwargs):
        return await self._client.post(f"{self.base_url}{path}", headers=self._headers(), **kwargs)

    async def put(self, path, **kwargs):
        return await self._client.put(f"{self.base_url}{path}", headers=self._headers(), **kwargs)

    async def delete(self, path, **kwargs):
        return await self._client.delete(f"{self.base_url}{path}", headers=self._headers(), **kwargs)

    async def close(self):
        await self._client.aclose()
