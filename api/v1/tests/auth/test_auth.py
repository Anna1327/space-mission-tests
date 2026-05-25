import pytest
import allure
from api.v1.src.data import AuthData

data = AuthData()


@allure.feature("Authentication")
class TestAuth:
    @allure.story("Register and login")
    @pytest.mark.asyncio
    async def test_register_and_login(self, unauthentic_client):
        register_payload = data.get_auth_payload
        register_resp = await unauthentic_client.post("/api/v1/auth/register", json=register_payload)
        assert register_resp.status_code in (200, 201), f"Registration failed: {register_resp.text}"

        login_payload = data.make_login_payload(register_payload)
        login_resp = await unauthentic_client.post("/api/v1/auth/token", json=login_payload)
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"

        token_data = login_resp.json()
        assert "access_token" in token_data, "Response does not contain access_token"
        assert token_data["access_token"], "access_token is empty"

    @allure.story("Register duplicate client")
    @pytest.mark.asyncio
    async def test_register_duplicate_client(self, unauthentic_client):
        register_payload = data.get_auth_payload
        await unauthentic_client.post("/api/v1/auth/register", json=register_payload)

        resp = await unauthentic_client.post("/api/v1/auth/register", json=register_payload)
        assert resp.status_code == 409, f"Expected 409 Conflict, got {resp.status_code}"

    @allure.story("Login with invalid credentials")
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, unauthentic_client):
        login_payload = data.get_login_wrong_payload
        resp = await unauthentic_client.post("/api/v1/auth/token", json=login_payload)
        assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}"
