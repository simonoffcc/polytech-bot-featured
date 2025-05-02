from os import getenv
from dotenv import load_dotenv
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.calendar_formatter import create_calendar
from utils.email_sender import EmailSender
from tg_bot.keyboards.calendar_kb import get_calendar_export_kb
from utils.schedule_processor import get_schedule_by_date
from utils.schedule_formatter import ScheduleFormatter
from utils.calendar_links import create_calendar_links_message
from db_orm.crud import get_user_by_attrs
from utils.groups_jsoner import find_group_by_id

router = Router()

class CalendarExport(StatesGroup):
    waiting_for_email = State()

load_dotenv()

email_sender = EmailSender(
    smtp_host= getenv('SMTP_HOST'),
    smtp_port=int(getenv('SMTP_PORT')),
    username=getenv('SMTP_USERNAME'),
    password=getenv('SMTP_PASSWORD')
)

@router.message(Command("export_calendar"))
async def cmd_export_calendar(message: Message, state: FSMContext):
    await message.answer(
        "Для экспорта расписания в Google Calendar, пожалуйста, "
        "введите адрес вашей почты:",
        reply_markup=get_calendar_export_kb()
    )
    await state.set_state(CalendarExport.waiting_for_email)

@router.message(CalendarExport.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    
    if not email_sender.validate_email_address(email):
        await message.answer(
            "Пожалуйста, введите корректный email адрес.\n"
            "Например: example@gmail.com"
        )
        return

    # Получаем информацию о пользователе
    user = get_user_by_attrs(telegram_id=message.from_user.id)
    if not user or not user.is_active:
        await message.answer(
            text="У вас нет доступа к этой команде."
        )
        return

    # Получаем расписание на сегодня
    day_schedule_response = get_schedule_by_date(
        volume='group',
        volume_data={
            'faculty': user.faculty,
            'group': user.group,
        },
        request_date=datetime.now().date()
    )

    if not day_schedule_response or not day_schedule_response.lessons:
        await message.answer("На сегодня расписания нет.")
        await state.clear()
        return

    # Форматируем название группы
    title = f"Группа {find_group_by_id(faculty=user.faculty, group_num=user.group)['name']}"
    
    # Отправляем email для каждой пары
    success = await email_sender.send_schedule(
        to_email=email,
        lessons=day_schedule_response.lessons
    )
    
    if success:
        await message.answer(
            f"На вашу почту {email} отправлены приглашения для каждой пары! "
            "Проверьте почту и добавьте интересующие вас занятия в календарь.\n\n"
            "Также вы можете добавить занятия прямо отсюда:"
        )
        
        # Создаем и отправляем сообщение со ссылками на добавление в календарь
        calendar_links = create_calendar_links_message(day_schedule_response.lessons)
        await message.answer(
            calendar_links,
            disable_web_page_preview=True,  # Отключаем превью ссылок
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "Произошла ошибка при отправке расписания. "
            "Пожалуйста, попробуйте позже или обратитесь к администратору."
        )
    
    await state.clear()

@router.callback_query(F.data == "cancel_export")
async def cancel_export(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Экспорт расписания отменен.")
    await state.clear() 