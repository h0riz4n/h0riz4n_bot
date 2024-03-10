from typing import Any

from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter, Command
from sqlalchemy.ext.asyncio import AsyncSession

from service import *

router = Router(name="command_router")
router.message.filter(F.chat.type == "private")
router.message.filter(StateFilter(None))


@router.message(CommandStart())
async def cmd_start(
        message: types.Message,
        session: AsyncSession
) -> Any:
    await CommandService.cmd_start(message, session)


@router.message(Command('menu'))
async def cmd_admin(
        message: types.Message
) -> Any:
    await CommandService.cmd_menu(message)


@router.message(Command('cart'))
async def cmd_cart(
        message: types.Message,
        session: AsyncSession
) -> Any:
    await CommandService.cmd_cart(message, session)
