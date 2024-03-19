import time
from typing import Union

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from fastapi.logger import logger

from api.v1.routers.auth_util import get_current_user
from api.v1.services.activities_service import (
    ActivitiesService,
    get_activities_service
)
from api.v1.schemas.schemas import (
    Like,
    Review,
    Bookmark,
    AuthUser,
    FilmParams,
    UserParams,
    ReviewWithSorting
)

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post(
    "/add_activity",
    summary="Add user activity",
    description="Add user activity (Like, Review, Favorite)",
    response_model=dict
)
async def add_activity(
        activity_data: Union[Like, Review, Bookmark],
        service: ActivitiesService = Depends(get_activities_service),
        is_auth: AuthUser = Depends(get_current_user)
):
    start_time = time.time()
    try:
        logger.info("Add activity %s", activity_data.activity_type, extra={"user_id": is_auth.id})
        await service.add_activity(activity_data, is_auth)
        return {"detail": "Activity was added"}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info("Execution time for add_activity: %s seconds", elapsed_time)


@router.get(
    "/get_film_likes",
    summary="Get film likes",
    description="Get film likes",
    response_model=dict
)
async def get_film_likes(
        params: FilmParams = Depends(),
        service: ActivitiesService = Depends(get_activities_service)
):
    try:
        logger.info("Get film likes for film id: %s", params.film_id)
        film_likes = await service.get_film_likes(params.film_id, params.offset, params.limit)
        return {"detail": film_likes}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    "/get_film_rating",
    summary="Get film rating",
    description="Get film rating",
    response_model=dict
)
async def get_film_rating(
        film_id: str,
        service: ActivitiesService = Depends(get_activities_service)
):
    try:
        logger.info("Get film rating for film id: %s", film_id)
        rating = await service.get_film_rating(film_id)
        return {"detail": rating}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    "/get_film_reviews",
    summary="Get film reviews",
    description="Get film reviews",
    response_model=dict,
)
async def get_film_reviews(
        review_with_sorting: ReviewWithSorting = Depends(),
        service: ActivitiesService = Depends(get_activities_service)
):
    try:
        logger.info("Get film reviews for film id: %s", review_with_sorting.film_id)
        film_reviews = await service.get_film_reviews(review_with_sorting)
        return {"detail": film_reviews}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    "/get_user_bookmarks",
    summary="Get user bookmarks",
    description="Get user bookmarks",
    response_model=dict
)
async def get_user_bookmarks(
        params: UserParams = Depends(),
        service: ActivitiesService = Depends(get_activities_service),
        is_auth: AuthUser = Depends(get_current_user)
):
    start_time = time.time()
    try:
        logger.info("Get user: %s bookmarks", is_auth.username, extra={"user_id": is_auth.id})
        user_bookmarks = await service.get_user_bookmarks(is_auth.id, params.offset, params.limit)
        return {"detail": user_bookmarks}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info("Execution time for get_user_bookmarks: %s seconds", elapsed_time)


@router.get("/sentry-debug")
async def trigger_error():
    """
    endpoint to check sentry
    """
    division_by_zero = 1 / 0
