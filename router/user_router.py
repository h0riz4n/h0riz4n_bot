from typing import Any

from aiogram import Router, types, F, Bot, html
from aiogram.filters import CommandStart, CommandObject, StateFilter, Command
from aiogram.fsm.context import FSMContext
from asyncpg import Pool
from sqlalchemy.ext.asyncio import AsyncSession

from service import *
from filter import *
from util import *

router = Router(name="user_router")
router.message.filter(F.chat.type == "private")


@router.message(F.photo)
async def msg(
        message: types.Message
) -> Any:
    print(message.photo[-1].file_id)


@router.callback_query(FoodTypeCallback.filter())
async def callback_food_type(
        callback: types.CallbackQuery,
        callback_data: FoodTypeCallback,
        session: AsyncSession
) -> Any:
    await UserService.callback_food_type(callback, callback_data, session)


@router.callback_query(PageCallback.filter())
async def callback_page(
        callback: types.CallbackQuery,
        callback_data: PageCallback,
        session: AsyncSession
) -> Any:
    await UserService.callback_page(callback, callback_data, session)


@router.callback_query(IngredientCallback.filter())
async def callback_ingredient(
        callback: types.CallbackQuery,
        callback_data: IngredientCallback,
        session: AsyncSession
) -> Any:
    await UserService.callback_ingredient(callback, callback_data, session)


@router.callback_query(CartCallback.filter(F.action == Action.remove))
async def callback_cart_remove(
        callback: types.CallbackQuery,
        callback_data: CartCallback,
        session: AsyncSession
) -> Any:
    await UserService.callback_cart_remove(callback, callback_data, session)


@router.callback_query(CartCallback.filter(F.action == Action.add))
async def callback_cart_add(
        callback: types.CallbackQuery,
        callback_data: CartCallback,
        session: AsyncSession
) -> Any:
    await UserService.callback_cart_add(callback, callback_data, session)


@router.callback_query(F.data == 'get_cart')
async def callback_get_cart(
        callback: types.CallbackQuery,
        session: AsyncSession
) -> Any:
    await UserService.callback_get_cart(callback, session)
