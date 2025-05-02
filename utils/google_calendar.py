from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import List, Optional
import os
from datetime import datetime
from utils.schedule_processor import ScheduleElement

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'psychic-fin-253517-13362f8e8a96.json'

class GoogleCalendarManager:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('calendar', 'v3', credentials=credentials)

    def _create_event_body(self, lesson: ScheduleElement) -> dict:
        """Создает тело события для Google Calendar"""
        event = {
            'summary': f"{lesson.name} ({lesson.type})",
            'location': lesson.auditory.name if lesson.auditory and lesson.auditory.name else '',
            'description': f"Преподаватель: {lesson.teacher.name if lesson.teacher and lesson.teacher.name else 'Не указан'}",
            'start': {
                'dateTime': lesson.timing.start_date.isoformat(),
                'timeZone': 'Europe/Moscow',
            },
            'end': {
                'dateTime': lesson.timing.end_date.isoformat(),
                'timeZone': 'Europe/Moscow',
            },
            'reminders': {
                'useDefault': True
            }
        }
        return event

    async def share_calendar_with_user(self, calendar_id: str, user_email: str) -> bool:
        """Предоставляет доступ к календарю пользователю"""
        try:
            rule = {
                'role': 'reader',
                'scope': {
                    'type': 'user',
                    'value': user_email
                }
            }
            self.service.acl().insert(calendarId=calendar_id, body=rule).execute()
            return True
        except Exception as e:
            print(f"Ошибка при предоставлении доступа: {str(e)}")
            return False

    async def create_calendar_for_schedule(self, user_email: str, lessons: List[ScheduleElement]) -> Optional[str]:
        """Создает новый календарь для расписания и добавляет в него события"""
        try:
            # Создаем новый календарь
            calendar_body = {
                'summary': 'Расписание занятий',
                'timeZone': 'Europe/Moscow'
            }
            calendar = self.service.calendars().insert(body=calendar_body).execute()
            calendar_id = calendar['id']

            # Предоставляем доступ пользователю
            await self.share_calendar_with_user(calendar_id, user_email)

            # Добавляем события
            for lesson in lessons:
                event_body = self._create_event_body(lesson)
                self.service.events().insert(calendarId=calendar_id, body=event_body).execute()

            return calendar_id
        except Exception as e:
            print(f"Ошибка при создании календаря: {str(e)}")
            return None

    def get_calendar_link(self, calendar_id: str) -> str:
        """Возвращает ссылку на календарь"""
        return f"https://calendar.google.com/calendar/embed?src={calendar_id}"

    def get_calendar_add_link(self, calendar_id: str) -> str:
        """Возвращает ссылку для добавления календаря в свой Google Calendar"""
        return f"https://calendar.google.com/calendar/r?cid={calendar_id}" 