from datetime import datetime
from typing import Callable, Awaitable, Dict, Any

import pytz
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from constant import *
from config import *


class TimeMiddleware(BaseMiddleware):
    """
      Middleware-класс для проверки рабочего времени
    """

    def __init__(self):
        super().__init__()
        self.__start_time = datetime.strptime(config.start_time, '%H:%M:%S').time()
        self.__end_time = datetime.strptime(config.end_time, '%H:%M:%S').time()

        if self.__start_time > self.__end_time:
            raise ValueError('Время начала рабочего дня должно быть раньше, чем конец рабочего дня')

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:

        time = datetime.now(pytz.timezone('Europe/Moscow'))

        if event.from_user.id in config.admins or self.__start_time <= time.time() < self.__end_time:
            return await handler(event, data)
        else:
            await event.bot.send_sticker(
                chat_id=event.from_user.id,
                sticker=sticker.SLEEP_STICKER
            )
            await event.answer(
                text=response_message.WORK_TIME_MSG
            )
            return
