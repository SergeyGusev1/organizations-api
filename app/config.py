from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@db:5432/orgdb"
    API_KEY: str = "supersecretapikey"

    model_config = {"env_file": ".env"}


settings = Settings()
