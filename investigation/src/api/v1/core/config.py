from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_conn: str = Field(alias="MONGO_CONN")
    sentry_dsn: str = Field(alias="SENTRY_DSN")


settings = Settings()
