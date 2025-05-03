from typing import List
from urllib.parse import quote
from utils.schedule_processor import ScheduleElement

def create_calendar_links_message(lessons: List[ScheduleElement], max_links_per_message: int = 10) -> List[str]:
    """
    Creates messages with Google Calendar links for each lesson.
    
    Args:
        lessons: List of lessons to create links for
        max_links_per_message: Maximum number of links per message to avoid Telegram limits
        
    Returns:
        List[str]: List of formatted messages with calendar links
    """
    if not lessons:
        return ["Нет занятий для добавления в календарь."]
    
    links = []
    for lesson in lessons:
        # Format event details
        title = f"{lesson.name} ({lesson.type})"
        location = lesson.auditory.name if lesson.auditory.name else 'Место не указано'
        
        description = []
        if lesson.teacher.name:
            description.append(f'Преподаватель: {lesson.teacher.name}')
        if lesson.links:
            description.append('\nСсылки:')
            for link in lesson.links:
                description.append(f'- {link.title}: {link.url}')
        
        # Create Google Calendar link
        start_time = lesson.timing.start_date.strftime('%Y%m%dT%H%M%S')
        end_time = lesson.timing.end_date.strftime('%Y%m%dT%H%M%S')
        
        url = (
            "https://calendar.google.com/calendar/render?"
            f"action=TEMPLATE&text={quote(title)}&"
            f"dates={start_time}/{end_time}&"
            f"location={quote(location)}&"
            f"details={quote('\n'.join(description))}"
        )
        
        # Format the link with date for better organization
        date_str = lesson.timing.start_date.strftime('%d.%m.%y')
        links.append((date_str, f"• <a href='{url}'>{title}</a> ({date_str})"))
    
    # Sort links by date
    links.sort(key=lambda x: x[0])
    links = [link[1] for link in links]
    
    # Split links into chunks
    messages = []
    for i in range(0, len(links), max_links_per_message):
        chunk = links[i:i + max_links_per_message]
        if i == 0:
            messages.append("Добавить в Google Calendar:\n\n" + "\n".join(chunk))
        else:
            messages.append("Продолжение списка занятий:\n\n" + "\n".join(chunk))
    
    return messages 