from os import getenv

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tg_bot.lexicon.buttons import lexicon as btns_lexicon


def get_main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=btns_lexicon['main_menu']['schedule']),
        KeyboardButton(text=btns_lexicon['main_menu']['week_schedule'])
    )
    builder.row(
        KeyboardButton(text=btns_lexicon['main_menu']['export_calendar']),
        KeyboardButton(text=btns_lexicon['main_menu']['export_week'])
    )
    builder.row(
        KeyboardButton(text=btns_lexicon['main_menu']['puffins'])
    )
    builder.row(
        KeyboardButton(
            text=btns_lexicon['main_menu']['settings'],
            web_app=WebAppInfo(
                url=f"{getenv('WEBAPP_URL', 'https://simonoffcc.github.io/polytech-bot-featured')}"
            )
        )
    )
    builder.row(
        KeyboardButton(text=btns_lexicon['main_menu']['about'])
    )

    return builder.as_markup(resize_keyboard=True)
