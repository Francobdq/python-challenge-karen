from main import app
from httpx import AsyncClient

async def get_auth_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={"username": "user", "password": "password"})
        assert response.status_code == 200
        return response.json()["access_token"]

async def process_query(query):
    token = await get_auth_token()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        return await ac.post("/graphql/", json={"query": query}, headers={"Authorization": f"Bearer {token}"})
