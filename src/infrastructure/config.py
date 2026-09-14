import os

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

# Determine environment (defaults to 'dev')
APP_ENV = os.getenv("APP_ENV", "dev")
ENV_FILE = ".env.test" if APP_ENV == "test" else ".env.dev"

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Clean Architecture"
    APP_ENV: str = APP_ENV
    DEBUG: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Dynamically generates the SQLAlchemy database connection URL."""
        return str(
            MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE if APP_ENV in ("dev", "test") else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()