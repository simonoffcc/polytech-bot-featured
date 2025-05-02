from utils.google_calendar import GoogleCalendarManager
from utils.schedule_processor import ScheduleElement
from typing import List

async def handle_schedule_export(message: types.Message, lessons: List[ScheduleElement], user_email: str):
    """Обработчик экспорта расписания в Google Calendar"""
    await message.reply("Создаю календарь с расписанием...")
    
    calendar_manager = GoogleCalendarManager()
    calendar_id = await calendar_manager.create_calendar_for_schedule(user_email, lessons)
    
    if calendar_id:
        view_link = calendar_manager.get_calendar_link(calendar_id)
        add_link = calendar_manager.get_calendar_add_link(calendar_id)
        
        response_text = (
            "✅ Календарь с расписанием создан!\n\n"
            "📅 Чтобы добавить расписание в свой Google Calendar:\n"
            "1. Перейдите по ссылке ниже\n"
            "2. Нажмите '+ Google Календарь' в нижней части страницы\n\n"
            f"🔗 [Открыть календарь]({view_link})\n"
            f"➕ [Добавить в свой календарь]({add_link})"
        )
        
        await message.reply(
            response_text,
            parse_mode=types.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    else:
        await message.reply(
            "❌ Произошла ошибка при создании календаря. Пожалуйста, попробуйте позже."
        ) 