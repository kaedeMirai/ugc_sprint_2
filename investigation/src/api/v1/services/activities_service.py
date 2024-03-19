from typing import Union, Annotated
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1.routers.auth_util import AuthUser
from api.v1.db.mongodb import get_mongodb_client
from api.v1.schemas.schemas import (
    Like,
    Review,
    Bookmark,
    FilmRating,
    ReviewWithSorting
)


class ActivitiesService:

    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client
        self.db = self.db_client.get_database(name="activities")
        self.collection = self.db.get_collection(name="user-activities")

    async def add_activity(self, activity_data: Union[Like, Review, Bookmark], is_auth: AuthUser) -> None:
        activity_data.user_id = is_auth.id
        await self.collection.insert_one(activity_data.model_dump())

    async def get_film_likes(self, film_id: str, offset: int, limit: int) -> list[dict]:
        cursor = self.collection.find({
            "entity_id": film_id,
            "activity_type": "like"
        }).skip(offset).limit(limit)

        film_likes = []

        async for doc in cursor:
            film_like = Like(**doc)
            film_likes.append(film_like.model_dump())

        return film_likes

    async def get_film_rating(self, film_id: str) -> FilmRating:
        cursor = self.collection.find({
            "entity_id": film_id,
            "activity_type": "like"
        })

        marks_sum = 0
        marks_amount = 0

        async for doc in cursor:
            marks_sum += doc["mark"]
            marks_amount += 1

        rating = round(marks_sum / marks_amount, 2)

        return FilmRating(film_id=film_id, rating=rating)

    async def get_film_reviews(self, review_with_sorting: ReviewWithSorting) -> list[dict]:
        query = {
            "film_id": review_with_sorting.film_id,
            "activity_type": 'review'
        }

        cursor = (
            self.collection
            .find(query)
            .sort(review_with_sorting.sort_keys, review_with_sorting.sort_order)
            .skip(review_with_sorting.offset)
            .limit(review_with_sorting.limit)
        )

        reviews = []
        async for doc in cursor:
            review = Review(**doc)
            reviews.append(review.model_dump())

        return reviews

    async def get_user_bookmarks(self, user_id: str, offset: int, limit: int) -> list[dict]:
        cursor = self.collection.find({
            "user_id": user_id,
            "activity_type": 'bookmark'
        }).skip(offset).limit(limit)

        bookmarks = []
        async for doc in cursor:
            bookmark = Bookmark(**doc)
            bookmarks.append(bookmark.model_dump())

        return bookmarks


def get_activities_service(
        db_client: Annotated[AsyncIOMotorClient, Depends(get_mongodb_client)]
) -> ActivitiesService:
    return ActivitiesService(db_client)
