import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from tests.settings import settings


@pytest_asyncio.fixture(scope="session")
async def api_client() -> AsyncClient:
    client = AsyncClient(
        base_url=f"{settings.api_host}:{settings.api_port}",
    )
    yield client


@pytest_asyncio.fixture(scope="session")
async def mongodb_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(settings.mongo_conn)
    yield client
    client.close()
