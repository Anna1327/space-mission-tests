import pytest
import allure


@allure.feature("Database Integration")
@allure.title("Проверка создания системы в PostgreSQL через DBConnector")
@pytest.mark.asyncio
async def test_system_creation_in_db(authentic_client, db_connector):
    payload = {
        "name": "Life Support Alpha",
        "system_type": "life_support"
    }

    response = await authentic_client.post("/api/v1/systems/", json=payload)
    assert response.status_code == 201
    system_id = response.json()["id"]

    db_systems = await db_connector.select_from_table(
        table="systems",
        where="id = $1",
        params=(system_id,)
    )

    assert len(db_systems) > 0, f"Система с ID {system_id} не найдена в БД!"
    system_record = db_systems[0]

    assert system_record["name"] == "Life Support Alpha"
    assert system_record["system_type"] == "life_support"
    assert system_record["status"] == "active"

