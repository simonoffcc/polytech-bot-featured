from datetime import datetime
from icalendar import Calendar, Event, vText
from typing import List, Dict
from uuid import uuid4

def create_calendar_event(lesson: Dict) -> Event:
    """Create a calendar event from a lesson dictionary"""
    event = Event()
    
    # Generate unique identifier for the event
    event['uid'] = str(uuid4())
    
    # Set basic event properties
    event.add('summary', f"{lesson['subject']} ({lesson['type']})")
    event.add('description', f"Преподаватель: {lesson['teacher']}\nАудитория: {lesson['classroom']}")
    
    # Convert string dates to datetime objects
    start_time = datetime.strptime(f"{lesson['date']} {lesson['start_time']}", "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(f"{lesson['date']} {lesson['end_time']}", "%Y-%m-%d %H:%M")
    
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    
    # Add location
    event.add('location', vText(lesson['classroom']))
    
    # Add status and other required properties
    event.add('status', 'CONFIRMED')
    event.add('sequence', 0)
    event.add('created', datetime.now())
    event.add('dtstamp', datetime.now())
    
    return event

def create_calendar(lessons: List[Dict]) -> str:
    """Create a calendar with multiple events"""
    cal = Calendar()
    
    # Set calendar metadata
    cal.add('prodid', '-//Polytech Schedule Bot//RU')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'REQUEST')  # Important for Google Calendar
    
    # Add events to calendar
    for lesson in lessons:
        event = create_calendar_event(lesson)
        cal.add_component(event)
    
    return cal.to_ical().decode('utf-8') 