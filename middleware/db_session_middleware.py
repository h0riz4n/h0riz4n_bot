from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class DbSessionMiddleware(BaseMiddleware):
    """
      Middleware-класс для работы с ассинхронной сессией базы данных
    """

    def __init__(
            self,
            session_pool: async_sessionmaker[AsyncSession]
    ):
        """
        :param session_pool: Сессия пула в базу данных
        """
        super().__init__()
        self.__session_pool = session_pool

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        async with self.__session_pool() as session:
            async with session.begin():
                data["session"] = session
                return await handler(event, data)
