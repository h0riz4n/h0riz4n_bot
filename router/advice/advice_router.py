import asyncio
import logging
from typing import Any

from aiogram import Router, types
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest, TelegramForbiddenError, TelegramServerError, \
    TelegramNetworkError
from aiogram.filters import ExceptionTypeFilter

advice_router = Router(name="advice_router")


@advice_router.error(ExceptionTypeFilter(TelegramRetryAfter))
async def handle_telegram_retry_after(event: types.ErrorEvent) -> Any:
    """
    Соблюдение "скоростного режима" в телеграм.
    """
    logging.error(f"TelegramRetryAfter exception is raised. Retry After {event.exception.retry_after}")
    await asyncio.sleep(event.exception.retry_after)


@advice_router.error(ExceptionTypeFilter(TelegramBadRequest))
async def handle_telegram_bad_request(event: types.ErrorEvent) -> Any:
    """
    Исключение возникает, когда запрос имеет неверный формат.
    """
    logging.error(event.exception.message)


@advice_router.error(ExceptionTypeFilter(TelegramForbiddenError))
async def handle_telegram_forbidden_error(event: types.ErrorEvent) -> Any:
    """
    Исключение возникает, когда у бота недостаточно привелегий, чтобы выполнить определённую функцию
    """
    logging.error(event.exception.message)


@advice_router.error(ExceptionTypeFilter(TelegramServerError))
async def handle_telegram_server_error(event: types.ErrorEvent) -> Any:
    """
    Исключение возникает, когда сервера Телеграм возвращают 5хх ошибку
    """
    logging.error(event.exception.message)


@advice_router.error(ExceptionTypeFilter(TelegramNetworkError))
async def handle_telegram_retry_after(event: types.ErrorEvent) -> Any:
    """
    Исключение возникает, когда появляется проблема с соединением
    """

    logging.error(event.exception.message)