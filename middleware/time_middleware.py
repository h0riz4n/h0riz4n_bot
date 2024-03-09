from datetime import datetime
from typing import Callable, Awaitable, Dict, Any

import pytz
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from constant import *


class TimeMiddleware(BaseMiddleware):
    """
      Middleware-класс для проверки рабочего времени
    """

    def __init__(
            self,
            start_time: str,
            end_time: str
    ):
        """
        :param start_time: Начало рабочего дня
        :param end_time: Конец рабочего дня
        """
        super().__init__()
        self.__start_time = start_time
        self.__end_time = end_time

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        time = datetime.now()
        time.replace(tzinfo=pytz.timezone("Europe/Moscow"))

        start_time = datetime.combine(time.date(), datetime.strptime(self.__start_time, '%H:%M:%S').time())
        end_time = datetime.combine(time.date(), datetime.strptime(self.__end_time, '%H:%M:%S').time())

        if start_time < time < end_time:
            return await handler(event, data)
        else:
            if event.message:
                await event.message.answer_sticker(
                    sticker=sticker.SLEEP_STICKER
                )
                await event.message.answer(
                    text=response_message.WORK_TIME_MSG
                )
            elif event.callback_query:
                await event.callback_query.answer(
                    text=response_message.WORK_TIME_MSG,
                    show_alert=True
                )
            return
