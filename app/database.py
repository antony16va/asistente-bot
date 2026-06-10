import asyncpg
from app.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

pool = None

async def init_pool():
    global pool
    pool = await asyncpg.create_pool(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        min_size=2,
        max_size=10
    )

async def close_pool():
    global pool
    await pool.close()

async def get_pool():
    return pool
