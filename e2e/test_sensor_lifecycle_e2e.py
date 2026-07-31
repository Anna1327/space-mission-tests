import json
import random

import pytest
import allure
import asyncio
from api.v1.src.constants import SENSORS


@allure.feature("End-to-End Testing")
@allure.title("Жизненный цикл датчика с WebSocket-уведомлениями и логированием инцидентов в БД")
@pytest.mark.asyncio
async def test_sensor_boundary_value_and_auto_recovery_e2e(
    authentic_client,
    authentic_ws_client,
    db_connector
):
    sensor_template = random.choice(SENSORS)
    allure.dynamic.description(f"E2E тест на базе датчика: {sensor_template['name']}")

    min_n = sensor_template["min_normal"]
    max_n = sensor_template["max_normal"]

    normal_value = float(min_n + (max_n - min_n) / 2)
    abnormal_value = float(max_n + 50)

    with allure.step("Создание космической системы через API"):
        system_payload = {"name": "Propulsion Core Alpha", "system_type": "engine"}
        system_response = await authentic_client.post("/api/v1/systems/", json=system_payload)
        assert system_response.status_code == 201
        system_id = system_response.json()["id"]

    with allure.step(f"Инициализация датчика '{sensor_template['name']}' со стартовым значением"):
        sensor_payload = {
            "name": sensor_template["name"],
            "unit": sensor_template["unit"],
            "min_normal": float(min_n),
            "max_normal": float(max_n),
            "value": normal_value
        }

        sensor_response = await authentic_client.post(
            f"/api/v1/systems/{system_id}/sensors/",
            json=sensor_payload
        )
        assert sensor_response.status_code == 201
        sensor_id = sensor_response.json()["id"]

    async with authentic_ws_client.connect(f"{system_id}") as ws:
        await asyncio.sleep(0.2)

        with allure.step(f"Отправка критического значения ({abnormal_value}) для датчика, проверка изменения статуса"):
            value_payload = {"value": abnormal_value}
            patch_response = await authentic_client.patch(
                f"/api/v1/systems/{system_id}/sensors/{sensor_id}/value",
                json=value_payload
            )
            assert patch_response.status_code == 200
            assert patch_response.json()["status"] == "abnormal"

        with allure.step("Перехват уведомления об аварии 'system_warning' через WebSocket"):
            try:
                raw_ws_msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
                ws_message = json.loads(raw_ws_msg)

                assert ws_message["system_id"] == system_id
                assert ws_message["event"] == "system_warning"
                assert ws_message["new_status"] == "warning"
            except asyncio.TimeoutError:
                pytest.fail("WebSocket не прислал уведомление о критическом выходе датчика за границы!")

        await asyncio.sleep(0.3)

        with allure.step(f"Возвращение показателя датчика в норму ({normal_value}), проверка изменения статуса"):
            recovery_payload = {"value": normal_value}
            recovery_response = await authentic_client.patch(
                f"/api/v1/systems/{system_id}/sensors/{sensor_id}/value",
                json=recovery_payload
            )
            assert recovery_response.status_code == 200
            assert recovery_response.json()["status"] == "normal"

        with allure.step("Перехват уведомления о восстановлении 'system_recover' через WebSocket"):
            try:
                raw_ws_recover_msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
                ws_recover_message = json.loads(raw_ws_recover_msg)

                assert ws_recover_message["system_id"] == system_id
                assert ws_recover_message["event"] == "system_recover"
                assert ws_recover_message["new_status"] == "active"
            except asyncio.TimeoutError:
                pytest.fail("WebSocket не прислал уведомление об автоматическом восстановлении!")

        with allure.step("Валидация логов инцидентов в PostgreSQL через DBConnector"):
            db_events = await db_connector.select_from_table(
                table="events",
                where="system_id = $1",
                params=(system_id,)
            )
            assert len(db_events) >= 2, "База данных не зафиксировала полную историю инцидентов!"

            event_types = [row["event_type"] for row in db_events]
            assert "system_warning" in event_types, "В таблице events отсутствует запись о критическом сбое!"
            assert "system_recover" in event_types, "В таблице events отсутствует запись о восстановлении!"
