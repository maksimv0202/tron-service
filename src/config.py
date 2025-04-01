import os
import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = pathlib.Path(os.getcwd()).parent / '.env'


class Settings(BaseSettings):
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding='utf-8')


settings = Settings()
