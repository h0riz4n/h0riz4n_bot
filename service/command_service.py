from datetime import datetime
from typing import Any

import pytz
from aiogram import types, html
from sqlalchemy import select
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
        time = datetime.now(pytz.timezone('Europe/Moscow'))
        start_time = datetime.combine(time.date(), time.time())

        await session.merge(User(id=message.from_user.id, username=message.from_user.username, creation_date_time=start_time))
        await message.answer_sticker(
            sticker=sticker.HELLO_STICKER
        )
        await message.answer(
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

    @staticmethod
    async def cmd_cart(
            message: types.Message,
            session: AsyncSession
    ) -> Any:
        cart_query = await session.execute(
            select(Cart.quantity, Food.price, Food.name)
            .join_from(Cart, Food)
            .where(Cart.user_id == message.from_user.id)
        )
        carts = cart_query.all()

        if isinstance(carts, list) and carts:
            main_price = 0
            main_text = "<b>Ваша корзина 🛒</b>\n\n"
            for row in carts:
                main_price += row[0] * row[1]
                main_text += f"🍽 <b>{row[2]}</b>\n<b>{row[0]} шт.</b> x <b>{row[1]}₽</b> = <b>{row[0] * row[1]}₽</b>\n\n"
            main_text += f"Итого: <b>{main_price} ₽</b>"
            await message.answer(
                text=main_text
            )
        else:
            await message.answer(
                text="Ваша корзина пуста 🛒\nВыберите категорию, чтобы что-то выбрать 📝",
                reply_markup=inline.food_type_board()
            )
