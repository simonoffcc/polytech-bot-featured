from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_calendar_export_kb() -> InlineKeyboardMarkup:
    """Return keyboard for calendar export"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data="cancel_export"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 