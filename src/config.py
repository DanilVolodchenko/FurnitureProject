import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    HOST: str
    PORT: int
    SECRET_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ROOT_PATH: Path = Path(__file__).parent.parent
    MEDIA_FILE_NAME = 'media'
    PATH_MEDIA_FILE = os.path.join(ROOT_PATH, MEDIA_FILE_NAME)
    EXPIRE_TOKEN: int = 60 * 60 * 48

    model_config = SettingsConfigDict(env_file=f'{ROOT_PATH}/.env')


settings = Settings()
