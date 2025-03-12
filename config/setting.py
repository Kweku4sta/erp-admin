from typing import Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    version: str = "1.0"
    releaseId: str = "1.1"
    API_PREFIX: str = "/api/v1"
    APP_NAME: str = "Remcash Admin Portal"
    API_TITLE: str = "Remcash Admin Portal API Documentation"
    APP_DESCRIPTION: str = "This is the API documentation for the Remcash Admin Portal"
    DATABASE_URL: str = "sqlite:///./test.db"
    TESTING: bool = False
    X_SUBSCRIPTION_KEY: str=  "tester"
    AUTH_SERVICE_API_USER: str = "tester"
    AUTH_SERVICE_API_KEY: str = "tester"
    REDIS_HOST: str = "192.168.124.168"
    REDIS_PORT: Union[int, str] = 6370
    REDIS_DB: Union[int, str] = 0
    REDIS_PASSWORD: str = ""
    POSTRES_DATABASE_URL: str = "postgresql://postgres:database@localhost/erp-portal"
    S3_REGION : str = "S3_REGION"
    AWS_ACCESS_KEY: str 
    AWS_SECRET_KEY: str 
    S3_ENDPOINT_URL: str = "http://192.168.126.207:9000"
    S3_BUCKET_NAME: str = "adminportal"
    PRESIGNED_URL_EXPIRATION: int = 60
    KAFKA_USERNAME: str = "admin"
    KAFKA_PASSWORD: str = "admin"
    KAFKA_BOOTSTRAP_SERVERS : str ="localhost:9092,localhost:9093,localhost:9094"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE: int = 60
    DEFAULT_ADMIN_PASSWORD: str = "Changem!1"
    DEFAULT_USER_PASSWORD: str = "Changem!1"


    class Config:
        env_file = ".env"


settings = Settings()