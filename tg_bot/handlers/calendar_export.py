from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.email_sender import EmailSender
from tg_bot.keyboards.calendar_kb import get_calendar_export_kb
from utils.schedule_processor import get_schedule_by_date, fetch_week_schedule, WeekScheduleElement
from utils.schedule_formatter import ScheduleFormatter
from utils.calendar_links import create_calendar_links_message
from utils.ics_generator import create_ics_calendar, cleanup_ics_file
from db_orm.crud import get_user_by_attrs
from utils.groups_jsoner import find_group_by_id
from tg_bot.lexicon.buttons import lexicon as btns_lexicon

router = Router()

class CalendarExport(StatesGroup):
    waiting_for_email = State()

load_dotenv()

email_sender = EmailSender(
    smtp_host=getenv('SMTP_HOST'),
    smtp_port=int(getenv('SMTP_PORT')),
    username=getenv('SMTP_USERNAME'),
    password=getenv('SMTP_PASSWORD')
)

@router.message(Command("export_today"))
@router.message(F.text == btns_lexicon['main_menu']['export_today'])
async def cmd_export_today(message: Message, state: FSMContext):
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
        return

    # Форматируем название группы
    title = f"Группа {find_group_by_id(faculty=user.faculty, group_num=user.group)['name']}"

    try:
        # Создаем ICS файл
        calendar_data = create_ics_calendar(day_schedule_response, title)
        
        # Сохраняем ICS файл временно
        filename = f"schedule_{datetime.now().strftime('%Y%m%d')}.ics"
        with open(filename, 'wb') as f:
            f.write(calendar_data)
        
        # Отправляем файл пользователю
        calendar_file = FSInputFile(filename)
        await message.answer_document(
            document=calendar_file,
            caption=(
                "Вот ваше расписание в формате ICS!\n"
                "Вы можете открыть этот файл в любом календарном приложении "
                "(Google Calendar, Apple Calendar, Outlook и др.)"
            )
        )

        # Очищаем временный файл
        cleanup_ics_file(filename)
    except Exception as e:
        await message.answer(
            "Произошла ошибка при создании календарного файла. "
            "Пожалуйста, попробуйте позже или обратитесь к администратору."
        )
        print(f"Error creating calendar file: {e}")
        return

@router.message(Command("export_week"))
@router.message(F.text == btns_lexicon['main_menu']['export_week'])
async def cmd_export_week_calendar(message: Message, state: FSMContext):
    # Получаем информацию о пользователе
    user = get_user_by_attrs(telegram_id=message.from_user.id)
    if not user or not user.is_active:
        await message.answer(
            text="У вас нет доступа к этой команде."
        )
        return

    # Получаем расписание на текущую неделю
    current_week_response = fetch_week_schedule(
        volume='group',
        volume_data={
            'faculty': user.faculty,
            'group': user.group,
        },
        request_date=datetime.now().date()
    )

    # Получаем расписание на следующую неделю
    next_week_date = datetime.now().date() + timedelta(days=7)
    next_week_response = fetch_week_schedule(
        volume='group',
        volume_data={
            'faculty': user.faculty,
            'group': user.group,
        },
        request_date=next_week_date
    )

    # Проверяем наличие расписания
    if (not current_week_response or not any(day.lessons for day in current_week_response.days)) and \
       (not next_week_response or not any(day.lessons for day in next_week_response.days)):
        await message.answer("На ближайшие две недели расписания нет.")
        return

    # Объединяем расписания двух недель
    if current_week_response and next_week_response:
        current_week_response.days.extend(next_week_response.days)
        # Обновляем даты начала и конца для объединенного расписания
        if current_week_response.timing and next_week_response.timing:
            current_week_response.timing.end_date = next_week_response.timing.end_date

    # Форматируем название группы
    title = f"Группа {find_group_by_id(faculty=user.faculty, group_num=user.group)['name']}"

    try:
        # Создаем ICS файл
        calendar_data = create_ics_calendar(current_week_response, title)
        
        # Сохраняем ICS файл временно
        filename = f"schedule_2weeks_{datetime.now().strftime('%Y%m%d')}.ics"
        with open(filename, 'wb') as f:
            f.write(calendar_data)
        
        # Отправляем файл пользователю
        calendar_file = FSInputFile(filename)
        await message.answer_document(
            document=calendar_file,
            caption=(
                "Вот ваше расписание на две недели в формате ICS!\n"
                "Вы можете открыть этот файл в любом календарном приложении "
                "(Google Calendar, Apple Calendar, Outlook и др.)"
            )
        )

        # Очищаем временный файл
        cleanup_ics_file(filename)
    except Exception as e:
        await message.answer(
            "Произошла ошибка при создании календарного файла. "
            "Пожалуйста, попробуйте позже или обратитесь к администратору."
        )
        print(f"Error creating calendar file: {e}")
        return

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

    # Получаем тип расписания из состояния
    state_data = await state.get_data()
    is_week_schedule = state_data.get("schedule_type") == "week"

    if is_week_schedule:
        schedule_response = fetch_week_schedule(
            volume='group',
            volume_data={
                'faculty': user.faculty,
                'group': user.group,
            },
            request_date=datetime.now().date()
        )
    else:
        schedule_response = get_schedule_by_date(
            volume='group',
            volume_data={
                'faculty': user.faculty,
                'group': user.group,
            },
            request_date=datetime.now().date()
        )

    if not schedule_response:
        await message.answer("Не удалось получить расписание.")
        await state.clear()
        return

    # Форматируем название группы
    title = f"Группа {find_group_by_id(faculty=user.faculty, group_num=user.group)['name']}"
    
    # Отправляем email
    success = await email_sender.send_schedule(
        to_email=email,
        schedule=schedule_response,
        title=title
    )

    if success:
        await message.answer("Расписание отправлено на ваш email.")
    else:
        await message.answer("Произошла ошибка при отправке расписания. Попробуйте позже.")

    await state.clear()

@router.callback_query(F.data == "cancel_export")
async def cancel_export(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Экспорт расписания отменен.")
    await state.clear() 