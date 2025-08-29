from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    IP_API_LIBERALI: str
    AUTH_API_LIBERALI: str
    PATH_DATABASE: str
