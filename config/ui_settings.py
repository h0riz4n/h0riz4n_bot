from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def set_ui_settings(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота 👋"),
        BotCommand(command="menu", description="Меню 📝"),
        BotCommand(command="cart", description="Корзина 🛒")
    ]
    await bot.set_my_description("")
    await bot.set_my_short_description("")
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
