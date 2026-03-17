from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    aws_region: str = "us-east-1"
    db_url: str = "postgresql://dbos:password@postgres:5432/dbos"

    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"))


settings = Settings()
