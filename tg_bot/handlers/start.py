import os
import subprocess
from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from pyexpat.errors import messages
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from emoji import emojize

from db_orm.crud import get_user_by_attrs, create_user, update_user_data
from db_orm.models import User
from tg_bot.handlers.menu import cmd_menu
from tg_bot.keyboards.service import get_list_kb
from tg_bot.states.register_user import InputUserStudyGroup
from utils.groups_jsoner import find_group_by_name, find_faculties_by_name
from tg_bot.keyboards.main_menu import get_main_menu_kb
from tg_bot.states.user_states import Registration
from tg_bot.lexicon.messages import lexicon as msgs_lexicon
from db_orm.database import Session

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    with Session() as session:
        user = get_user_by_attrs(session, telegram_id=message.from_user.id)
    if user:
        if not user.is_active:
            with Session() as session:
                update_user_data(session, telegram_id=message.from_user.id, is_active=True)
        await message.answer(
            text=emojize(msgs_lexicon['start']['already_registered'].format(first_name=message.from_user.first_name)),
            reply_markup=get_main_menu_kb()
        )
    else:
        await state.set_state(Registration.waiting_for_faculty)
        await message.answer(text=msgs_lexicon['start']['new_user'])


@router.message(Registration.waiting_for_faculty)
async def process_faculty(message: Message, state: FSMContext):
    faculty = find_faculties_by_name(faculty_name=message.text)
    if faculty:
        await state.update_data(faculty=faculty['id'])
        await state.set_state(Registration.waiting_for_group)
        await message.answer(text=msgs_lexicon['start']['faculty_found'])
    else:
        await message.answer(text=msgs_lexicon['start']['faculty_not_found'])


@router.message(Registration.waiting_for_group)
async def process_group(message: Message, state: FSMContext):
    user_data = await state.get_data()
    group = find_group_by_name(faculty_id=user_data['faculty'], group_name=message.text)

    if group:
        await state.update_data(group=group['id'])
        user_data = await state.get_data()

        with Session() as session:
            create_user(
                session,
                telegram_id=message.from_user.id,
                faculty=user_data['faculty'],
                group=user_data['group']
            )

        await message.answer(
            text=emojize(msgs_lexicon['start']['success_registration']),
            reply_markup=get_main_menu_kb()
        )
        await state.clear()
    else:
        await message.answer(
            text=msgs_lexicon['start']['group_not_found']
        )
