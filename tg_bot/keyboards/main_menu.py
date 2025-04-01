from os import getenv

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tg_bot.lexicon.buttons import lexicon as btns_lexicon
from tg_bot.lexicon.messages import lexicon as msgs_lexicon


def get_main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=btns_lexicon['main_menu']['schedule'])
    )
    builder.row(
        KeyboardButton(text=btns_lexicon['main_menu']['find_teacher']),
    )
    builder.row(
        KeyboardButton(
            text=btns_lexicon['main_menu']['settings'],
            web_app=WebAppInfo(
                url="https://ya.ru"
                # url=f"{getenv('WEBAPP_URL')}/settings?uid={tid}&token={settings_token}"
            )
        )
    )

    return builder.as_markup(resize_keyboard=True)
