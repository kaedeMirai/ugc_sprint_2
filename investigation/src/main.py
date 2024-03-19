from contextlib import asynccontextmanager

import uvicorn
import logging
import logstash
import sentry_sdk
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.responses import ORJSONResponse

from api.v1.core.config import settings
from api.v1.routers.router import router
from api.v1.db.mongodb import close_mongodb_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # from investigation.src.api.v1.utils import generate_data
    # await generate_data.generate_data()
    yield
    close_mongodb_client()


def build_app():
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    logger.setLevel(logging.INFO)
    # handler for LogStash
    logger.addHandler(logstash.LogstashHandler('logstash', 5044, version=0))
    # handler for stdout
    logger.addHandler(logging.StreamHandler())

    logger.info("Starting App")

    fast_api_app = FastAPI(
        title='UGC Sprint 2',
        description='Tracking activities api',
        version='1.0.0',
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
        lifespan=lifespan
    )

    fast_api_app.include_router(router, prefix='/api/v1')
    return fast_api_app


app = build_app()

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host="0.0.0.0",
        port=8282,
        reload=True
    )
