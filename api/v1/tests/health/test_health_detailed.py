import pytest
import allure


@allure.feature("Health checks")
@pytest.mark.asyncio
async def test_health_detailed_returns_200(unauthentic_client):
    response = await unauthentic_client.get("/health/detailed")
    assert response.status_code == 200


@allure.feature("Health checks")
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