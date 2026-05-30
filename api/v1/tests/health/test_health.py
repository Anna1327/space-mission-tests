import pytest
import allure


@allure.feature("Health checks")
@pytest.mark.asyncio
async def test_health_returns_200(unauthentic_client):
    response = await unauthentic_client.get("/health")
    assert response.status_code == 200


@allure.feature("Health checks")
@pytest.mark.asyncio
async def test_health_contains_all_components(unauthentic_client):
    response = await unauthentic_client.get("/health")
    data = response.json()
    assert data["status"] == "healthy"


@allure.feature("Health checks")
@pytest.mark.asyncio
async def test_negative_method_not_allowed(unauthentic_client):
    response = await unauthentic_client.post("/health")
    assert response.status_code == 405
