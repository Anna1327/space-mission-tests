import pytest
import allure
from api.v1.src.data import SensorsData, AuthData

data = SensorsData()
auth_data = AuthData()


# POSITIVE TESTS
@allure.feature("Sensors checks")
@allure.title("Get all sensors for system (GET /api/v1/systems/{system_id}/sensors/)")
@pytest.mark.asyncio
async def test_get_sensors_returns_200(authentic_client, created_sensor):
    system, sensor = created_sensor
    response = await authentic_client.get(f"/api/v1/systems/{system['id']}/sensors/")
    data = response.json()
    assert response.status_code == 200
    assert data[0]["name"] == sensor["name"]


@allure.feature("Sensors checks")
@allure.title("Create new sensor for system (POST /api/v1/systems/{system_id}/sensors/)")
@pytest.mark.asyncio
async def test_create_sensors_returns_201(authentic_client, created_system):
    response_get_sensors = await authentic_client.get(f"/api/v1/systems/{created_system['id']}/sensors/")
    assert response_get_sensors.status_code == 200
    get_sensors = response_get_sensors.json()
    assert not get_sensors

    sensors_payload = data.create_sensor_payload
    response = await authentic_client.post(f"/api/v1/systems/{created_system['id']}/sensors/", json=sensors_payload)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["name"] == sensors_payload["name"]

    response_get_sensors = await authentic_client.get(f"/api/v1/systems/{created_system['id']}/sensors/")
    assert response_get_sensors.status_code == 200
    get_sensors = response_get_sensors.json()
    assert get_sensors[0]["name"] == sensors_payload["name"]


@allure.feature("Sensors checks")
@allure.title("Update sensor by id (PATCH /api/v1/systems/{system_id}/sensors/{sensor_id}/value)")
@pytest.mark.asyncio
@pytest.mark.parametrize('value', [-100.0, -50.0, -10.0, 0.0, 10.0, 50.0, 100.0])
async def test_patch_sensors_returns_200(authentic_client, created_sensor, value):
    system, sensor = created_sensor
    payload = data.update_sensor_payload(value)

    response = await authentic_client.patch(f"/api/v1/systems/{system['id']}/sensors/{sensor['id']}/value", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["sensor_id"] == sensor["id"]
    assert response_data["value"] == payload["value"]

    expected_status = data.get_sensor_status(value, sensor["min_normal"], sensor["max_normal"])
    assert response_data["status"] == expected_status
