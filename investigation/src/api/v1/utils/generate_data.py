import uuid
import asyncio
from random import randint
from typing import Union

from motor.motor_asyncio import AsyncIOMotorClient

from api.v1.utils.util import timeit
from api.v1.schemas.schemas import (
    Like,
    Review,
    Bookmark
)

USER_IDS = [str(uuid.uuid4()) for _ in range(5000)]
FILM_IDS = [str(uuid.uuid4()) for _ in range(5000)]


def generate_likes_data(amount: int = 2000) -> list[Like]:
    likes_data = []

    for _ in range(amount):
        user_id = USER_IDS[randint(0, 4999)]
        film_id = FILM_IDS[randint(0, 24)]

        like = Like(
            user_id=user_id,
            entity_id=film_id,
            activity_type='like',
            mark=randint(0, 10)
        )

        likes_data.append(like)

    return likes_data


def generate_reviews_data(amount: int = 2000) -> list[Review]:
    reviews_data = []

    for _ in range(amount):
        user_id = USER_IDS[randint(0, 4999)]
        film_id = FILM_IDS[randint(0, 24)]

        review = Review(
            user_id=user_id,
            film_id=film_id,
            activity_type='review',
            text="Lorem ipsum dolores sir amet"
        )

        reviews_data.append(review)

    return reviews_data


def generate_bookmarks_data(amount: int = 2000) -> list[Bookmark]:
    bookmarks_data = []
    user_id = USER_IDS[randint(0, 4999)]

    for _ in range(amount):
        film_id = FILM_IDS[randint(0, 4999)]

        bookmark = Bookmark(
            user_id=user_id,
            film_id=film_id,
            activity_type='bookmark'
        )

        bookmarks_data.append(bookmark)

    return bookmarks_data


@timeit
async def write_data(
        data: list[Union[Like, Review, Bookmark]],
        client: AsyncIOMotorClient
) -> None:
    db = client.get_database("activities")
    collection = db.get_collection("user-activities")

    for doc in data:
        await collection.insert_one(doc.model_dump())


async def generate_data():
    client = AsyncIOMotorClient("mongodb://mongos1:27017")

    likes_data = generate_likes_data()
    reviews_data = generate_reviews_data()
    bookmarks_data = generate_bookmarks_data()

    try:
        print(f'Generating likes ...')
        await write_data(likes_data, client)
        print(f'Generating reviews ...')
        await write_data(reviews_data, client)
        print(f'Generating bookmarks ...')
        await write_data(bookmarks_data, client)
    except Exception as e:
        print(e)
    finally:
        client.close()


if __name__ == '__main__':
    asyncio.run(generate_data())
