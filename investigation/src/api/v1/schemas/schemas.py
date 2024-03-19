from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field


class BaseActivity(BaseModel):
    user_id: str
    activity_type: Literal["like", "review", "bookmark"]
    created_date: datetime = Field(default=datetime.now())


class Like(BaseActivity):
    entity_id: str
    mark: int = Field(ge=0, le=10)


class Review(BaseActivity):
    film_id: str
    text: str = Field(max_length=1000)


class Bookmark(BaseActivity):
    film_id: str


class FilmRating(BaseModel):
    film_id: str
    rating: float


class PaginationMixin(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=1000, ge=1, le=100000)


class FilmParams(PaginationMixin):
    film_id: str


class UserParams(PaginationMixin):
    pass


class ReviewWithSorting(PaginationMixin):
    film_id: str
    sort_keys: str = Field(default="film_id"),
    sort_order: int = Field(ge=-1, le=1)


class AuthUser(BaseModel):
    id: str
    username: str
    roles: list
