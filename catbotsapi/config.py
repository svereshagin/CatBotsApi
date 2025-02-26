from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR: Path = Path(__file__).parents[1]
ENV_FILE_PATH: Path = BASE_DIR.joinpath(".env")


class Settings(BaseSettings):
    """
    Settings class
    :var
    DB_DATABASE_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    TOKEN: str
    LOGIN: str
    PASSWORD: str
    """

    model_config = SettingsConfigDict(extra="ignore", env_file=ENV_FILE_PATH)
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def __str__(self):
        return self.DATABASE_URL


settings = Settings()
