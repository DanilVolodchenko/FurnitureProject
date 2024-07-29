from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str
    PORT: int
    SECRET_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ROOT_PATH: Path = Path(__file__).parent.parent

    model_config = SettingsConfigDict(env_file=f'{ROOT_PATH}/.env')


settings = Settings()
