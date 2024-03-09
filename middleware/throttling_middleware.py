from typing import Any, Dict, Callable, Awaitable

from config import *
from constant import *
from aiogram import BaseMiddleware

from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware-класс, который занимается урегулированием количества сообщений
    в минуту
    """

    def __init__(self, limit: int):
        """
        :param limit: лимит на количество сообщений в минуту
        """
        self.__storage = RedisStorage.from_url('redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'.format(
            REDIS_PASSWORD=config.redis_password,
            REDIS_HOST=config.redis_host,
            REDIS_PORT=config.redis_port,
            REDIS_DB=config.redis_throttling_db
        ))
        self.__limit = limit

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        check_user = await self.__storage.redis.get(str(event.from_user.id))

        if check_user:
            user_limit = int(check_user.decode())
            if user_limit == 1:
                await self.__storage.redis.set(name=str(event.from_user.id), value=0, ex=60)
                return await event.answer("Превышен лимит запросов в минуту")
            elif user_limit > 1:
                expire = await self.__storage.redis.ttl(name=str(event.from_user.id))
                if isinstance(expire, int) and expire > 0:
                    await self.__storage.redis.set(name=str(event.from_user.id), value=user_limit - 1, ex=expire)
                return await handler(event, data)
            return

        await self.__storage.redis.set(name=str(event.from_user.id), value=self.__limit, ex=60)
        return await handler(event, data)
