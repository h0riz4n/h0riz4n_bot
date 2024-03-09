from .command_router import router as command_router
from .user_router import router as user_router
from .advice.advice_router import advice_router

__all__ = [
    'command_router',
    'user_router',
    'advice_router'
]
