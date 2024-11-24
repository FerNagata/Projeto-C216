import asyncpg
import os

async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/") 
    return await asyncpg.connect(DATABASE_URL)

async def get_all_accomodation():
    conn = await get_database()
    try:
        query = "SELECT * FROM accommodation"
        rows = await conn.fetch(query)
        accommodations = [dict(row) for row in rows]
        return accommodations
    finally:
        await conn.close()