from enum import Enum

from aiogram.filters.callback_data import CallbackData


class FoodTypeCallback(CallbackData, prefix='food_type'):
    food_type: int


class IngredientCallback(CallbackData, prefix='ingredient'):
    food_id: int


class PageCallback(CallbackData, prefix='page'):
    is_next: bool
    page: int
    food_type: int


class Action(str, Enum):
    add = 'add'
    remove = 'remove'


class CartCallback(CallbackData, prefix='menu'):
    action: Action
    page: int
    food_type: int
    food_id: int
