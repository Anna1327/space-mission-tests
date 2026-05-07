import pytest
from api.v1.services.api_client import APIClient
from settings import settings


@pytest.fixture(scope="function")
async def unauthentic_client():
    client = APIClient(base_url=settings.get("BASE_URL", "http://localhost:8000"))
    yield client
    await client.close()
