from aiogram import Router
from aiogram.types import Message

from tg_bot.keyboards.main_menu import get_main_menu_kb

from tg_bot.lexicon.messages import lexicon as msgs_lexicon

router = Router()

@router.message()
async def unknown_message_handler(message: Message):
    await message.answer(
        text=msgs_lexicon['service']['command_not_allowed'],
        reply_markup=get_main_menu_kb()
    )