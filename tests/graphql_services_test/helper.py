from main import app
from httpx import AsyncClient

async def process_query(query):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        return await ac.post("/graphql/", json={"query": query})
