from datetime import datetime
from urllib.parse import quote
from typing import List
from utils.schedule_processor import ScheduleElement

def create_google_calendar_link(lesson: ScheduleElement) -> str:
    """Create a Google Calendar event link for a lesson"""
    
    # Format dates for URL
    start_time = lesson.timing.start_date.strftime("%Y%m%dT%H%M%S")
    end_time = lesson.timing.end_date.strftime("%Y%m%dT%H%M%S")
    
    # Create event details
    event_name = f"{lesson.name} ({lesson.type})"
    location = lesson.auditory.name if lesson.auditory and lesson.auditory.name else "Место не указано"
    description = f"Преподаватель: {lesson.teacher.name if lesson.teacher and lesson.teacher.name else 'Не указан'}"
    
    # Create the URL
    base_url = "https://calendar.google.com/calendar/render"
    params = {
        "action": "TEMPLATE",
        "text": event_name,
        "dates": f"{start_time}/{end_time}",
        "details": description,
        "location": location,
    }
    
    # Build the URL
    url_parts = [f"{key}={quote(str(value))}" for key, value in params.items()]
    return f"{base_url}?{'&'.join(url_parts)}"

def create_calendar_links_message(lessons: List[ScheduleElement]) -> str:
    """Create a message with Google Calendar links for all lessons"""
    if not lessons:
        return "На этот день занятий нет"
    
    message_parts = ["<b>Ссылки для добавления занятий в календарь:</b>\n"]
    
    # Add individual links
    for lesson in lessons:
        time_str = f"{lesson.timing.start_date.strftime('%H:%M')}–{lesson.timing.end_date.strftime('%H:%M')}"
        event_name = f"{lesson.name} ({lesson.type})"
        calendar_link = create_google_calendar_link(lesson)
        
        message_parts.append(
            f"🕐 {time_str} - {event_name}\n"
            f"➕ <a href='{calendar_link}'>Добавить в календарь</a>\n"
        )
    
    return "\n".join(message_parts) 