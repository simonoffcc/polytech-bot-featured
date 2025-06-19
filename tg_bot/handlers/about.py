from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from db_orm.crud import get_user_by_attrs
from tg_bot.keyboards.main_menu import get_main_menu_kb

from tg_bot.lexicon.messages import lexicon as msgs_lexicon
from tg_bot.lexicon.buttons import lexicon as btns_lexicon

router = Router()


@router.message(Command("about"))
@router.message(F.text == btns_lexicon['main_menu']['about'])
async def cmd_about(message: Message):
    user = get_user_by_attrs(telegram_id=message.from_user.id)

    if not user or not user.is_active:
        await message.answer(
            text=msgs_lexicon['service']['command_not_allowed'],
        )
        return

    await message.answer(
        text=msgs_lexicon['about']['info'],
        reply_markup=get_main_menu_kb()
    )

