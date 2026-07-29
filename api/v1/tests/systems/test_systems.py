import pytest
import allure
from api.v1.src.data import SystemsData, AuthData

data = SystemsData()
auth_data = AuthData()


# POSITIVE TESTS
@allure.feature("Systems checks")
@allure.title("Get all system's list (GET /api/v1/systems/)")
@pytest.mark.asyncio
async def test_get_systems_returns_200(authentic_client):
    response = await authentic_client.get("/api/v1/systems/")
    assert response.status_code == 200


@allure.feature("Systems checks")
@allure.title("Create new system (POST /api/v1/systems/)")
@pytest.mark.asyncio
async def test_post_systems_returns_200(authentic_client):
    systems_payload = data.create_system_payload
    response = await authentic_client.post("/api/v1/systems/", json=systems_payload)
    assert response.status_code == 201

    created_id = response.json()["id"]
    delete_resp = await authentic_client.delete(f"/api/v1/systems/{created_id}")
    assert delete_resp.status_code == 200


@allure.feature("Systems checks")
@allure.title("Get system's list with pagination (GET /api/v1/systems/?skip=2&limit=5)")
@pytest.mark.parametrize("created_systems", [10], indirect=True)
@pytest.mark.asyncio
async def test_get_systems_with_pagination(authentic_client, created_systems):
    response = await authentic_client.get("/api/v1/systems/?skip=2&limit=5")
    assert response.status_code == 200

    response_data = response.json()
    assert len(response_data) == 5

    response = await authentic_client.get("/api/v1/systems/")
    all_systems = response.json()
    assert response_data[0]["id"] == all_systems[2]["id"]


@allure.feature("Systems checks")
@allure.title("Get system's list with sorting (GET /api/v1/systems/?sort_by=name&order=desc)")
@pytest.mark.parametrize("created_systems", [10], indirect=True)
@pytest.mark.asyncio
async def test_get_systems_with_sorting(authentic_client, created_systems):
    response = await authentic_client.get("/api/v1/systems/?sort_by=name&order=desc")
    assert response.status_code == 200

    response_data = response.json()
    received_names = [system["name"] for system in response_data]
    expected_names = sorted(received_names, reverse=True)
    assert received_names == expected_names


@allure.feature("Systems checks")
@allure.title("Get system's list with status filter (GET /api/v1/systems/?status_filter={status})")
@pytest.mark.asyncio
@pytest.mark.parametrize('status', ['active', 'warning', 'failed'])
async def test_get_systems_with_status_filter(authentic_client, status):
    response = await authentic_client.get(f"/api/v1/systems/?status_filter={status}")
    system_data = response.json()
    assert response.status_code == 200
    assert all(system["status"] == status for system in system_data)


@allure.feature("Systems checks")
@allure.title("Get system by id positive (GET /api/v1/systems/{system_id})")
@pytest.mark.asyncio
async def test_get_system_by_id_returns_200(authentic_client, created_system):
    response = await authentic_client.get(f"/api/v1/systems/{created_system['id']}")
    assert response.status_code == 200


@allure.feature("Systems trigger checks")
@allure.title("Add trigger event to system (POST /api/v1/systems/{system_id}/trigger/{event_type})")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "event_type, expected_status",
    [
        ("failure", "failed"),
        ("warning", "warning"),
        ("recover", "active"),
    ]
)
async def test_add_trigger_event_to_system(authentic_client, created_system, event_type, expected_status):
    response = await authentic_client.post(f"/api/v1/systems/{created_system['id']}/trigger/{event_type}")
    response_data = response.json()
    assert response_data["status"] == 'triggered'
    get_system = await authentic_client.get(f"/api/v1/systems/{created_system['id']}")
    system_data = get_system.json()
    assert system_data["status"] == expected_status


# NEGATIVE TESTS
@allure.feature("Systems checks")
@allure.title("Get all system's list negative (GET /api/v1/systems/)")
@pytest.mark.asyncio
async def test_get_systems_without_token(unauthentic_client):
    response = await unauthentic_client.get("/api/v1/systems/")
    assert response.status_code == 401


@allure.feature("Systems checks")
@allure.title("Get all system's list negative (GET /api/v1/systems/)")
@pytest.mark.asyncio
async def test_get_systems_with_fake_token(unauthentic_client):
    unauthentic_client.token = "this_is_a_fake_and_broken_jwt_token"
    response = await unauthentic_client.get("/api/v1/systems/")
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Invalid or expired token"


@allure.feature("Systems checks")
@allure.title("Get system by id negative (GET /api/v1/systems/{system_id})")
@pytest.mark.asyncio
async def test_get_system_by_id_returns_404(authentic_client):
    system_id = 999999
    response = await authentic_client.get(f"/api/v1/systems/{system_id}")
    assert response.status_code == 404


@allure.feature("Systems trigger checks")
@allure.title("Add trigger event to system negative (POST /api/v1/systems/{system_id}/trigger/{event_type})")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "event_type",
    ["explosion"]
)
async def test_add_trigger_event_negative(authentic_client, created_system, event_type):
    response = await authentic_client.post(f"/api/v1/systems/{created_system['id']}/trigger/{event_type}")
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == 'Invalid event_type. Must be one of: failure, warning, recover'
