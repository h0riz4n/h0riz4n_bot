import asyncio
import logging
import sys
from typing import Any

from aiogram import Dispatcher, Bot, F
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from middleware import *
from router import *
from config import *
from config.load_all import *
from db import *


async def startup(
        async_engine: AsyncEngine,
        async_session: async_sessionmaker[AsyncSession],
        bot: Bot,
) -> Any:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            await session.merge(FoodType(id=1, name='Бургеры'))
            await session.merge(FoodType(id=2, name='Хот-доги'))
            await session.merge(FoodType(id=3, name='Фритюр'))
            await session.merge(FoodType(id=4, name='Соусы'))

    await set_ui_settings(bot)
    await bot.delete_webhook(drop_pending_updates=False)


async def main():
    bot = Bot(config.token, default=bot_default)
    dp = Dispatcher()

    dp.include_routers(command_router, user_router, advice_router)

    dp["async_engine"] = engine
    dp["async_session"] = session_maker
    dp.startup.register(startup)

    dp.update.middleware.register(DbSessionMiddleware(session_pool=session_maker))
    dp.callback_query.middleware.register(CallbackAnswerMiddleware())

    dp.message.outer_middleware.register(TimeMiddleware())
    dp.callback_query.outer_middleware.register(TimeMiddleware())

    # dp.message.outer_middleware.register(ThrottlingMiddleware(limit=config.limit))
    # dp.callback_query.outer_middleware.register(ThrottlingMiddleware(limit=config.limit))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
