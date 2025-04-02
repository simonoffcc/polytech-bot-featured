from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db_orm.crud import get_user_by_attrs
from tg_bot.handlers.menu import cmd_menu
from tg_bot.keyboards.service import get_list_kb
from tg_bot.keyboards.service import get_cancel_action_kb

from tg_bot.lexicon.messages import lexicon as msgs_lexicon
from tg_bot.lexicon.buttons import lexicon as btns_lexicon
from tg_bot.states.find_teacher import InputTeacherName
from utils.groups_jsoner import find_teacher_by_name
from utils.schedule_formatter import ScheduleFormatter
from utils.schedule_processor import get_schedule_by_date

router = Router()


@router.message(Command("find_teacher"))
@router.message(F.text == btns_lexicon['main_menu']['find_teacher'])
async def cmd_find_teacher(message: Message, state: FSMContext):
    user = get_user_by_attrs(telegram_id=message.from_user.id)

    if not user or not user.is_active:
        await message.answer(
            text=msgs_lexicon['service']['command_not_allowed']
        )
        return


    await message.answer(
        text=msgs_lexicon['find_teacher']['first_message'],
        reply_markup=get_cancel_action_kb()
    )

    await state.set_state(InputTeacherName.waiting_for_msg)

@router.message(InputTeacherName.waiting_for_msg)
async def find_teacher_by_user_input(message: Message, state: FSMContext):
    input_teacher_name = message.text.strip()

    if input_teacher_name == btns_lexicon['service']['cancel_action']:
        await message.answer(
            text=msgs_lexicon['service']['action_canceled'],
            reply_markup=None
        )
        await cmd_menu(message, state)

    else:
        founded_teachers = find_teacher_by_name(input_teacher_name)

        if founded_teachers:
            if len(founded_teachers) == 1:
                await state.clear()

                teacher = founded_teachers[0]
                teacher_schedule_response = get_schedule_by_date(
                    volume='teacher',
                    volume_data={
                        'teacher_id': teacher['id']
                    },
                    request_date=datetime.now().date()
                )

                if teacher_schedule_response: # ruz отдал OK 200
                    current_dt = datetime.now()
                    result = {'status': None, 'lesson': None}
                    for lesson in teacher_schedule_response.lessons:
                        if current_dt < lesson.timing.start_date:
                            result['status'] = 'upcoming'
                            result['lesson'] = lesson
                            break
                        elif lesson.timing.start_date <= current_dt < lesson.timing.end_date:
                            result['status'] = 'running'
                            result['lesson'] = lesson
                            break

                    await message.answer(
                        text=ScheduleFormatter.format_find_teacher_block(teacher, result['status'], result['lesson']),
                        reply_markup=None
                    )

                else:
                    await message.answer(
                        text=msgs_lexicon['service']['ruz_error']
                    )


            elif len(founded_teachers) < 20:
                await message.answer(
                    text=msgs_lexicon['find_teacher']['many_teachers'],
                    reply_markup=get_list_kb(founded_teachers, 'name')
                )

            else:
                await message.answer(
                    text=msgs_lexicon['find_teacher']['many_teachers']
                )


        else:
            await message.answer(
                text=msgs_lexicon['find_teacher']['teacher_not_found']
            )
