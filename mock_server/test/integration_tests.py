import pytest
import pytest_asyncio
from httpx import AsyncClient, Client
from mock_server.app.main import app
import time


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(base_url="http://localhost:5000") as client:
        yield client

@pytest_asyncio.fixture
def sync_client():
    with Client(base_url="http://localhost:5000") as client:
        yield client


# Root endpoint
@pytest.mark.asyncio
async def test_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.text == "\"ok\""

# Status endpoint
@pytest.mark.asyncio
async def test_status(async_client):
    response = await async_client.get("/status")
    assert response.status_code == 200
    assert response.json().get("status") == "healthy"
    assert "version" in response.json()

# Users endpoints
@pytest.mark.asyncio
async def test_get_users(async_client):
    response = await async_client.get("/users")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_add_user(async_client):
    new_user = {"id": 6, "name": "Test User", "email": "test@example.com"}
    response = await async_client.post("/users", json=new_user)
    assert response.status_code == 201

    response = await async_client.get("/users/6")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"

@pytest.mark.asyncio
async def test_delete_user(async_client):
    time.sleep(1)
    response = await async_client.delete("/users/6")
    assert response.status_code == 201

    response = await async_client.get("/users/6")
    assert response.status_code == 404

# Companies endpoints
@pytest.mark.asyncio
async def test_get_companies(async_client):
    response = await async_client.get("/companies")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_add_company(async_client):
    new_company = {"id": 6, "name": "Test Company"}
    response = await async_client.post("/companies", json=new_company)
    assert response.status_code == 201

    response = await async_client.get("/companies/6")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Company"

@pytest.mark.asyncio
async def test_delete_company(async_client):
    time.sleep(1)
    response = await async_client.delete("/companies/6")
    assert response.status_code == 201

    response = await async_client.get("/companies/6")
    assert response.status_code == 404
