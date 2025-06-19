from datetime import datetime
import os
from icalendar import Calendar, Event
from utils.schedule_processor import DayScheduleElement, ScheduleElement, WeekScheduleElement

def create_ics_calendar(schedule: DayScheduleElement | WeekScheduleElement, title: str) -> bytes:
    """
    Creates an ICS calendar file from schedule data.
    
    Args:
        schedule: Schedule data for a day or week
        title: Title for the calendar (e.g. group name)
        
    Returns:
        bytes: The ICS file content as bytes
    """
    cal = Calendar()
    cal.add('prodid', '-//Polytech Schedule Bot//RU')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', f'Расписание - {title}')
    cal.add('x-wr-timezone', 'Europe/Moscow')

    if isinstance(schedule, WeekScheduleElement):
        if schedule.days:
            for day in schedule.days:
                if day.lessons:
                    for lesson in day.lessons:
                        event = _create_calendar_event(lesson)
                        cal.add_component(event)
    else:  # DayScheduleElement
        if schedule and schedule.lessons:
            for lesson in schedule.lessons:
                event = _create_calendar_event(lesson)
                cal.add_component(event)
    
    return cal.to_ical()

def _create_calendar_event(lesson: ScheduleElement) -> Event:
    """
    Creates a calendar event from a lesson.
    
    Args:
        lesson: The lesson data
        
    Returns:
        Event: Calendar event
    """
    event = Event()
    
    # Basic event info
    event.add('summary', f'{lesson.name} ({lesson.type})')
    event.add('dtstart', lesson.timing.start_date)
    event.add('dtend', lesson.timing.end_date)
    
    # Location
    location = lesson.auditory.name if lesson.auditory.name else 'Место не указано'
    event.add('location', location)
    
    # Description
    description = []
    if lesson.teacher.name:
        description.append(f'Преподаватель: {lesson.teacher.name}')
    if lesson.links:
        description.append('\nСсылки:')
        for link in lesson.links:
            description.append(f'- {link.title}: {link.url}')
    
    event.add('description', '\n'.join(description))
    
    # Add unique identifier
    event_id = f'{lesson.timing.start_date.strftime("%Y%m%d")}_{lesson.name}_{lesson.type}'
    event.add('uid', event_id)
    
    return event

def cleanup_ics_file(filename: str) -> None:
    """
    Removes a temporary ICS file.
    
    Args:
        filename: Name of the file to remove
    """
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        print(f"Error cleaning up ICS file: {e}") 