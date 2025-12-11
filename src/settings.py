from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    BOT_TOKEN: str
    PG_PATH: str
    LLM_TOKEN: str
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/.env')


settings = Settings()
