from pydantic import Field
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    mongo_conn: str = Field(default="mongodb://mongos1:27017/", alias="MONGODB_CONN")
    mongo_db: str = Field(default="activities", alias="MONGO_DB")
    mongo_collection: str = Field(default="user-activities", alias="MONGO_COLLECTION")
    # Services hosts
    api_host: str = "http://0.0.0.0"
    api_port: int = 8282


settings = TestSettings()
