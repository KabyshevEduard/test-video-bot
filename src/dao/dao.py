import asyncpg
from src.settings import settings


async def execute_sql(query):
    url = settings.PG_PATH[:10] + settings.PG_PATH[18:]
    conn = await asyncpg.connect(url)
    values = await conn.fetch(query)
    await conn.close()
    return values