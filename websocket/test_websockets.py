import asyncio
import pytest
import allure
from services.ws.ws_listener import WSListener


@allure.feature("Systems WebSockets")
@allure.title("Проверка уведомлений об аварии системы в реальном времени через WS")
@pytest.mark.asyncio
async def test_system_failure_websocket_notification(authentic_client, authentic_ws_client, created_system):
    system_id = created_system["id"]

    await asyncio.sleep(0.5)

    async with authentic_ws_client.connect(f"{system_id}") as ws_connection:
        listener = WSListener(ws_connection)

        filter_params = {
            "system_id": system_id,
            "new_status": "failure"
        }

        async def trigger_failure():
            response = await authentic_client.post(f"/api/v1/systems/{system_id}/trigger/failure")
            assert response.status_code == 200

        def validator(data):
            assert data["event"] == "system_failure"
            assert data["system_name"] == created_system["name"]

        await trigger_failure()
        await listener.wait_for_event(
            filter_params=filter_params,
            callback=lambda data: validator(data),
            timeout_sec=5
        )
