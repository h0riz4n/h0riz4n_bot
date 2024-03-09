from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .config_reader import config

# Соединение с PostgreSQL Database
engine = create_async_engine(
    url="postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_USER=config.db_user,
        DB_PASSWORD=config.db_password,
        DB_HOST=config.db_host,
        DB_PORT=config.db_port,
        DB_NAME=config.db_name
    ), echo=True)
session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Соединение с Redis Database
redis = RedisStorage.from_url('redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'.format(
    REDIS_PASSWORD=config.redis_password,
    REDIS_HOST=config.redis_host,
    REDIS_PORT=config.redis_port,
    REDIS_DB=config.redis_main_db
))

# Bot settings
bot_default = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
    link_preview_is_disabled=True
)
