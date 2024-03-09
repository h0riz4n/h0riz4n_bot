from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.keyboard import InlineKeyboardMarkup

from db import *
from keyboard.inline import inline_keyboard as inline


class Util:

    def __init__(self):
        pass

    @staticmethod
    async def get_user_board(
            user_id: int,
            food: Food,
            page: int,
            session: AsyncSession
    ) -> InlineKeyboardMarkup:
        cart_query = await session.execute(select(Cart.quantity)
                                           .where(Cart.user_id == user_id)
                                           .where(Cart.food_id == food.id)
                                           )
        quantity: int = cart_query.scalar_one_or_none()

        if isinstance(quantity, int):
            return inline.cart_menu(page, food.id, food.food_type, quantity)
        else:
            return inline.menu(page, food.id, food.food_type)

