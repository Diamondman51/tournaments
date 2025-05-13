import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_tournament():
    async with AsyncClient(base_url="http://localhost:8000/") as session:
        response = await session.post("/tournaments/", json={
            "name": "Running Uzbekistan 2025",
            "max_players": 100
        })

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Running Uzbekistan 2025"
    assert data["max_players"] == 100
