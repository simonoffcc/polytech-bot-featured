from os import getenv

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tg_bot.lexicon.buttons import lexicon as btns_lexicon
from tg_bot.lexicon.messages import lexicon as msgs_lexicon


def get_cancel_action_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=btns_lexicon['service']['cancel_action'])
    )

    return builder.as_markup(resize_keyboard=True)

def get_list_kb(data: list, key: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for el in data:
        builder.row(
            KeyboardButton(text=el[key])
        )

    return builder.as_markup(resize_keyboard=True)