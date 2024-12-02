from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
    DB2_HOST: str
    DB2_DB: str
    DB2_PORT: int
    DB2_USER: str
    DB2_PASS: str
