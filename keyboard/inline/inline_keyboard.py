from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from util import *


def food_type_board() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Бургеры 🍔",
            callback_data=FoodTypeCallback(food_type=1).pack()
        )
    ).row(
        InlineKeyboardButton(
            text="Хот-доги 🌭",
            callback_data=FoodTypeCallback(food_type=2).pack()
        )
    ).row(
        InlineKeyboardButton(
            text="Фритюр 🍟",
            callback_data=FoodTypeCallback(food_type=3).pack()
        )
    ).row(
        InlineKeyboardButton(
            text="Соусы 🥫",
            callback_data=FoodTypeCallback(food_type=4).pack()
        )
    )
    return builder.as_markup()


def menu(
        page: int,
        food_id: int,
        food_type: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Состав 🔖",
            callback_data=IngredientCallback(food_id=food_id).pack()
        )
    ).row(
        InlineKeyboardButton(
            text="Добавить в корзину 🛒",
            callback_data=CartCallback(action=Action.add, page=page, food_type=food_type, food_id=food_id).pack()
        )
    ).row(
        InlineKeyboardButton(
            text="« Назад",
            callback_data=PageCallback(is_next=False, page=page, food_type=food_type).pack()
        ),
        InlineKeyboardButton(
            text="Далее »",
            callback_data=PageCallback(is_next=True, page=page, food_type=food_type).pack()
        )
    )
    return builder.as_markup()


def cart_menu(
        page: int,
        food_id: int,
        food_type: int,
        quantity: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Состав 🔖",
            callback_data=IngredientCallback(food_id=food_id).pack()
        )
    ).row(
        InlineKeyboardButton(
            text="-",
            callback_data=CartCallback(action=Action.remove, page=page, food_type=food_type, food_id=food_id).pack()
        ),
        InlineKeyboardButton(
            text=f"{quantity} 🛒",
            callback_data='get_cart'
        ),
        InlineKeyboardButton(
            text="+",
            callback_data=CartCallback(action=Action.add, page=page, food_type=food_type, food_id=food_id).pack()
        )
    ).row(
        InlineKeyboardButton(
            text="« Назад",
            callback_data=PageCallback(is_next=False, page=page, food_type=food_type).pack()
        ),
        InlineKeyboardButton(
            text="Далее »",
            callback_data=PageCallback(is_next=True, page=page, food_type=food_type).pack()
        )
    )
    return builder.as_markup()
