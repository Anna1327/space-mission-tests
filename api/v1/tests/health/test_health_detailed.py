import pytest
import allure
import time


@allure.feature("Health detailed checks")
@pytest.mark.asyncio
async def test_health_detailed_returns_200(unauthentic_client):
    response = await unauthentic_client.get("/health/detailed")
    assert response.status_code == 200


@allure.feature("Health detailed checks")
@pytest.mark.asyncio
async def test_health_detailed_contains_all_components(unauthentic_client):
    response = await unauthentic_client.get("/health/detailed")
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data["checks"]
    assert "redis" in data["checks"]
    assert "websocket" in data["checks"]
    assert data["checks"]["database"] == "connected"
    assert data["checks"]["redis"] == "connected"
    assert "active_connections" in data["checks"]["websocket"]


@allure.feature("Health checks")
@pytest.mark.asyncio
async def test_health_detailed_content_type_json(unauthentic_client):
    response = await unauthentic_client.get("/health/detailed")
    assert response.headers["content-type"] == "application/json"


@allure.feature("Health checks")
@pytest.mark.asyncio
async def test_negative_method_not_allowed(unauthentic_client):
    response = await unauthentic_client.post("/health/detailed")
    assert response.status_code == 405
