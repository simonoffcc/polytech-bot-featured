from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from db_orm.crud import get_user_by_attrs
from db_orm.database import Session
from tg_bot.keyboards.main_menu import get_main_menu_kb

from tg_bot.lexicon.messages import lexicon as msgs_lexicon
from tg_bot.lexicon.buttons import lexicon as btns_lexicon

router = Router()

@router.message(Command("menu"))
@router.message(F.text == btns_lexicon['service']['back_to_menu'])
async def cmd_menu(message: Message):
    with Session() as session:
        user = get_user_by_attrs(session, telegram_id=message.from_user.id)

    if user and user.is_active:
        await message.answer(
            text=msgs_lexicon['main_menu']['menu'],
            reply_markup=get_main_menu_kb()
        )
    else:
        await message.answer(
            text=msgs_lexicon['service']['command_not_allowed'],
        )