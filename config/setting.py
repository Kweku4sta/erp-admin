from typing import Union

from pydantic_settings import BaseSettings


"""
This class is used to store the application settings.
Feel free to add more settings as needed. and make sure to add them to the .env file
You can also add more configurations to the class Config
You can change the class name to whatever you want, but make sure to change it in the core/setup.py file

"""

class Settings(BaseSettings):
    version: str = "1.0"
    releaseId: str = "1.1"
    API_PREFIX: str = "/api/v1"
    APP_NAME: str = "FastAPI Base Application"
    API_TITLE: str = "Quantum Group API Documentation"
    APP_DESCRIPTION: str = "This is a base application for FastAPI"
    DATABASE_URL: str = "sqlite:///./test.db"
    TESTING: bool = False
    X_SUBSCRIPTION_KEY: str=  "tester"
    AUTH_SERVICE_API_USER: str = "tester"
    AUTH_SERVICE_API_KEY: str = "tester"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: Union[int, str] = 6379
    REDIS_DB: Union[int, str] = 0
    REDIS_PASSWORD: str = ""
    POSTRES_DATABASE_URL: str = "postgresql://postgres:database@localhost/erp-portal"
    S3_REGION : str = "S3_REGION"
    AWS_ACCESS_KEY: str = "AWS_ACCESS_KEY"
    AWS_SECRET_KEY: str = "AWS_SECRET_KEY"

    class Config:
        env_file = ".env"


settings = Settings()