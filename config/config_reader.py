from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str
    limit: int
    admins: list
    db_host: str
    db_user: str
    db_password: str
    db_port: int
    db_name: str
    redis_password: str
    redis_host: str
    redis_port: int
    redis_throttling_db: int
    redis_main_db: int
    model_config = SettingsConfigDict(env_file='./venv/bot_config', env_file_encoding='utf-8')


config = Settings()
