from typing import Any

from aiogram import Router, types, F, Bot, html
from aiogram.filters import CommandStart, CommandObject, StateFilter, Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from service import *
from filter import *

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