import uuid
from http import HTTPStatus
from datetime import datetime
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from tests.settings import settings
from api.v1.schemas.schemas import (
    Like,
    Review,
    Bookmark
)


async def test_add_activity(api_client: AsyncClient, mongodb_client: AsyncIOMotorClient):
    user_id = str(uuid.uuid4())
    film_id = str(uuid.uuid4())

    activity = {
        "user_id": user_id,
        "film_id": film_id,
        "activity_type": "bookmark"
    }

    response = await api_client.post("/api/v1/activities/add_activity", json=activity)

    db = mongodb_client.get_database(settings.mongo_db)
    collection = db.get_collection(settings.mongo_collection)
    bookmark = await collection.find_one_and_delete({
        "user_id": user_id,
        "film_id": film_id,
        "activity_type": "bookmark"
    })

    assert response.status_code == HTTPStatus.OK
    assert Bookmark(**bookmark)


async def test_get_film_likes(api_client: AsyncClient, mongodb_client: AsyncIOMotorClient):
    user_id = str(uuid.uuid4())
    film_id = str(uuid.uuid4())

    activity = {
        "user_id": user_id,
        "entity_id": film_id,
        "mark": 10,
        "activity_type": "like",
        "created_date": datetime.now()
    }

    db = mongodb_client.get_database(settings.mongo_db)
    collection = db.get_collection(settings.mongo_collection)
    await collection.insert_one(activity)

    response = await api_client.get(f"/api/v1/activities/get_film_likes?film_id={film_id}&offset=0&limit=100")
    await collection.find_one_and_delete(activity)

    assert response.status_code == HTTPStatus.OK
    assert Like(**response.json()["detail"][0])


async def test_get_film_rating(api_client: AsyncClient, mongodb_client: AsyncIOMotorClient):
    user_id = str(uuid.uuid4())
    film_id = str(uuid.uuid4())

    activity = {
        "user_id": user_id,
        "entity_id": film_id,
        "mark": 10,
        "activity_type": "like",
        "created_date": datetime.now()
    }

    db = mongodb_client.get_database(settings.mongo_db)
    collection = db.get_collection(settings.mongo_collection)
    await collection.insert_one(activity)

    response = await api_client.get(f"/api/v1/activities/get_film_rating?film_id={film_id}")
    await collection.find_one_and_delete(activity)

    assert response.status_code == HTTPStatus.OK
    assert dict(response.json()).get("detail").get("rating") == 10


async def test_get_film_reviews(api_client: AsyncClient, mongodb_client: AsyncIOMotorClient):
    user_id = str(uuid.uuid4())
    film_id = str(uuid.uuid4())

    activity = {
        "user_id": user_id,
        "film_id": film_id,
        "text": "test",
        "activity_type": "review",
        "created_date": datetime.now()
    }

    db = mongodb_client.get_database(settings.mongo_db)
    collection = db.get_collection(settings.mongo_collection)
    await collection.insert_one(activity)

    response = await api_client.get(
        f"/api/v1/activities/get_film_reviews?film_id={film_id}"
        f"&offset=0&limit=100&sort_keys=user_id&sort_order=1"
    )
    await collection.find_one_and_delete(activity)

    assert response.status_code == HTTPStatus.OK
    assert Review(**response.json()["detail"][0])


async def test_get_user_bookmarks(api_client: AsyncClient, mongodb_client: AsyncIOMotorClient):
    user_id = str(uuid.uuid4())
    film_id = str(uuid.uuid4())

    activity = {
        "user_id": user_id,
        "film_id": film_id,
        "activity_type": "bookmark",
        "created_date": datetime.now()
    }

    db = mongodb_client.get_database(settings.mongo_db)
    collection = db.get_collection(settings.mongo_collection)
    await collection.insert_one(activity)

    response = await api_client.get(f"/api/v1/activities/get_user_bookmarks?user_id={user_id}&offset=0&limit=100")
    await collection.find_one_and_delete(activity)

    assert response.status_code == HTTPStatus.OK
    assert Bookmark(**response.json()["detail"][0])
