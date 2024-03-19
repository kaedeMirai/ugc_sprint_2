from motor.motor_asyncio import AsyncIOMotorClient
from api.v1.core.config import settings

client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongo_conn)


def get_mongodb_client():
    return client


def close_mongodb_client():
    client.close()
