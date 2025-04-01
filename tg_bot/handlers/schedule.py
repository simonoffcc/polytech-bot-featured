from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db_orm.crud import get_user_by_attrs
from tg_bot.keyboards.main_menu import get_main_menu_kb

from tg_bot.lexicon.messages import lexicon as msgs_lexicon
from tg_bot.lexicon.buttons import lexicon as btns_lexicon
from utils.groups_jsoner import find_group_by_name, find_group_by_id
from utils.schedule_formatter import ScheduleFormatter
from utils.schedule_processor import get_schedule_by_date

router = Router()


@router.message(Command("schedule"))
@router.message(F.text == btns_lexicon['main_menu']['schedule'])
async def cmd_new_work(message: Message, state: FSMContext):
    user = get_user_by_attrs(telegram_id=message.from_user.id)

    if user and user.is_active:

        day_schedule_response = get_schedule_by_date(
            volume='group',
            volume_data={
                'faculty': user.faculty,
                'group': user.group,
            },
            request_date=datetime.now().date()
        )

        title = f"Группа {find_group_by_id(faculty=user.faculty, group_num=user.group)['name']}"
        formatted_day_schedule = ScheduleFormatter.format_day_schedule(day_schedule_response, title)

        await message.answer(
            text=btns_lexicon['main_menu']['schedule'],
            # todo: Reply Keyboard для расписания
            reply_markup=None
        )

        # todo: Inline Keyboard для сообщения с расписанием
        await message.answer(
            text=formatted_day_schedule,
        )

    else:
        await message.answer(
            text=msgs_lexicon['service']['command_not_allowed']
        )
