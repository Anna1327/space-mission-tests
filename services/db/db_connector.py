import asyncpg
from settings import settings


class DBConnector:
    def __init__(self):
        self.conn = None

    async def __aenter__(self):
        db_url = settings.get("DATABASE_URL")

        if db_url.startswith("postgresql+asyncpg://"):
            db_url = db_url.replace("postgresql+asyncpg://", "postgresql://", 1)

        if "@db:" in db_url:
            db_url = db_url.replace("@db:", "@localhost:", 1)

        self.conn = await asyncpg.connect(db_url)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            await self.conn.close()

    async def select_from_table(self, table: str, where: str = '', params: tuple = ()):
        """Асинхронный SELECT. Возвращает список словарей [{поле: значение}]"""
        query = f"SELECT * FROM {table}"
        if where:
            query += f" WHERE {where}"

        rows = await self.conn.fetch(query, *params)
        return [dict(row) for row in rows]

    async def insert(self, table: str, data: dict):
        """Асинхронный INSERT. Возвращает ID созданной записи"""
        keys = ', '.join(data.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(data))])
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders}) RETURNING id"
        return await self.conn.fetchval(query, *values)

    async def delete(self, table: str, where: str, params: tuple = ()):
        """Асинхронное удаление записей"""
        query = f"DELETE FROM {table} WHERE {where}"
        status = await self.conn.execute(query, *params)
        return int(status.split()[-1]) if status else 0
