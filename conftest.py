import pytest
from api.v1.services.api_client import APIClient
from api.v1.src.data import AuthData, SystemsData, SensorsData
from services.ws.ws_client import WSClient
from settings import settings


@pytest.fixture(scope="function")
async def unauthentic_client():
    client = APIClient(base_url=settings.get("BASE_URL", "http://localhost:8000"))
    yield client
    await client.close()


@pytest.fixture(scope="function")
async def authentic_client():
    client = APIClient(base_url=settings.get("BASE_URL", "http://localhost:8000"))
    data = AuthData()
    register_payload = data.get_auth_payload
    register_resp = await client.post("/api/v1/auth/register", json=register_payload)
    assert register_resp.status_code in (200, 201)

    login_payload = data.make_login_payload(register_payload)
    login_resp = await client.post("/api/v1/auth/token", json=login_payload)
    assert login_resp.status_code == 200

    token_data = login_resp.json()
    jwt_token = token_data.get("access_token")
    client.token = jwt_token
    yield client
    await client.close()


@pytest.fixture()
async def created_system(authentic_client):
    data = SystemsData()
    systems_payload = data.create_system_payload
    response = await authentic_client.post("/api/v1/systems/", json=systems_payload)
    yield response.json()
    system_id = response.json()['id']
    response = await authentic_client.delete(f"/api/v1/systems/{system_id}")
    assert response.status_code == 200


@pytest.fixture()
async def created_systems(authentic_client, request):
    system_ids = []
    for i in range(request.param):
        data = SystemsData()
        systems_payload = data.create_system_payload
        response = await authentic_client.post("/api/v1/systems/", json=systems_payload)
        system_ids.append(response.json()["id"])
    yield system_ids
    for system_id in system_ids:
        response = await authentic_client.delete(f"/api/v1/systems/{system_id}")
        assert response.status_code == 200


@pytest.fixture()
async def created_sensor(authentic_client, created_system):
    data = SensorsData()
    sensor_payload = data.create_sensor_payload
    response = await authentic_client.post(f"/api/v1/systems/{created_system["id"]}/sensors/", json=sensor_payload)
    yield created_system, response.json()


@pytest.fixture(scope="function")
async def authentic_ws_client(authentic_client):
    token = authentic_client.token

    ws_client = WSClient(token=token)
    return ws_client
