from typing import Any

from aiogram import types
from aiogram.types import InputMediaPhoto
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import *
from constant import *
from util import *
from keyboard import *


class UserService:

    def __init__(self):
        pass

    @staticmethod
    async def callback_food_type(
            callback: types.CallbackQuery,
            callback_data: FoodTypeCallback,
            session: AsyncSession
    ) -> Any:
        food_query = await session.execute(
            select(Food)
            .where(Food.food_type == callback_data.food_type)
            .where(Food.is_active == True)
            .offset(offset=0)
            .limit(limit=1)
            .order_by(Food.id)
        )
        food: Food = food_query.scalar_one_or_none()

        if isinstance(food, Food):
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=food.preview,
                caption=response_message.FOOD_TITLE.format(
                    name=food.name,
                    price=food.price
                ),
                reply_markup=await Util.get_user_board(callback.from_user.id, food, 0, session)
            )
        else:
            await callback.answer(
                text='В данной категории нет позиций ❌',
                show_alert=True
            )

    @staticmethod
    async def callback_page(
            callback: types.CallbackQuery,
            callback_data: PageCallback,
            session: AsyncSession
    ) -> Any:
        if callback_data.is_next:
            page = callback_data.page + 1
        else:
            page = callback_data.page - 1
            if page < 0:
                await callback.answer(
                    text="Вы находитесь в начале",
                    show_alert=False
                )
                return

        food_query = await session.execute(
            select(Food)
            .where(Food.food_type == callback_data.food_type)
            .where(Food.is_active == True)
            .offset(offset=page)
            .limit(limit=1)
            .order_by(Food.id)
        )
        food: Food = food_query.scalar_one_or_none()

        if isinstance(food, Food):
            await callback.message.edit_media(
                media=InputMediaPhoto(
                    media=food.preview,
                    caption=response_message.FOOD_TITLE.format(
                        name=food.name,
                        price=food.price
                    ),
                ),
                reply_markup=await Util.get_user_board(callback.from_user.id, food, page, session)
            )
        else:
            await callback.answer(
                text="Позиций больше нет",
                show_alert=False
            )

    @staticmethod
    async def callback_ingredient(
            callback: types.CallbackQuery,
            callback_data: IngredientCallback,
            session: AsyncSession
    ) -> Any:
        ingredient_query = await session.execute(
            select(Food.ingredients)
            .where(Food.id == callback_data.food_id)
        )
        ingredients: str = ingredient_query.scalar_one_or_none()

        if isinstance(ingredients, str):
            await callback.answer(
                text="🔖 " + ingredients,
                show_alert=True
            )
        else:
            await callback.answer(
                text='Ингредиенты не найдены'
            )

    @staticmethod
    async def callback_cart_remove(
            callback: types.CallbackQuery,
            callback_data: CartCallback,
            session: AsyncSession
    ) -> Any:
        cart_query = await session.execute(
            select(Cart)
            .where(Cart.user_id == callback.from_user.id)
            .where(Cart.food_id == callback_data.food_id)
        )

        cart: Cart = cart_query.scalar_one_or_none()
        keyboard = inline.menu(callback_data.page, callback_data.food_id, callback_data.food_type)

        if isinstance(cart, Cart):
            if cart.quantity == 1:
                await session.delete(cart)
            else:
                cart.quantity = cart.quantity - 1
                await session.merge(cart)
                keyboard = inline.cart_menu(callback_data.page, callback_data.food_id, callback_data.food_type, cart.quantity)

        await callback.message.edit_reply_markup(
            reply_markup=keyboard
        )

    @staticmethod
    async def callback_cart_add(
            callback: types.CallbackQuery,
            callback_data: CartCallback,
            session: AsyncSession
    ) -> Any:
        cart_query = await session.execute(
            select(Cart)
            .where(Cart.user_id == callback.from_user.id)
            .where(Cart.food_id == callback_data.food_id)
        )
        cart: Cart = cart_query.scalar_one_or_none()

        if isinstance(cart, Cart):
            cart.quantity = cart.quantity + 1
        else:
            cart = Cart(user_id=callback.from_user.id, food_id=callback_data.food_id, quantity=1)

        await session.merge(cart)
        await callback.message.edit_reply_markup(
            reply_markup=inline.cart_menu(callback_data.page, callback_data.food_id, callback_data.food_type,
                                          cart.quantity)
        )

    @staticmethod
    async def callback_get_cart(
            callback: types.CallbackQuery,
            session: AsyncSession
    ) -> Any:
        cart_query = await session.execute(
            select(Cart.quantity, Food.price)
            .join_from(Cart, Food)
            .where(Cart.user_id == callback.from_user.id)
        )
        carts = cart_query.all()

        if isinstance(carts, list):
            main_price = 0
            for row in carts:
                main_price += row[0] * row[1]

            await callback.answer(text=f"Общая сумма: {main_price} ₽")

