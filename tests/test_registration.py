import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(base_url='http://localhost:8000/') as session:
        response = await session.post('tournaments/24/register', json={
            "name": "John Doe",
            "email": "john25@gmail.com"
        })

    assert response.status_code == 201
    data = response.json()
    assert data['name'] == "John Doe"
    assert data['email'] == "john25@gmail.com"
