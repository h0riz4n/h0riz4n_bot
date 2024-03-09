from datetime import datetime
from typing import Any

import pytz
from aiogram import types, html
from sqlalchemy.ext.asyncio import AsyncSession

from db import *
from constant import *
from keyboard import *


class CommandService:

    def __init__(self):
        pass

    @staticmethod
    async def cmd_start(
            message: types.Message,
            session: AsyncSession
    ) -> Any:
        time = datetime.now()
        time.replace(tzinfo=pytz.timezone("Europe/Moscow"))

        await session.merge(User(id=message.from_user.id, username=message.from_user.username, creation_date_time=time))
        await message.reply(
            text=f"Привет, <b>{html.quote(message.from_user.full_name)}</b>"
        )

    @staticmethod
    async def cmd_menu(
            message: types.Message
    ) -> Any:
        await message.answer(
            text=response_message.CMD_MENU_MSG,
            reply_markup=inline.food_type_board()
        )
