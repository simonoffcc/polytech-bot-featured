import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List
import os
from email_validator import validate_email, EmailNotValidError
import ssl
from utils.schedule_processor import ScheduleElement
from utils.calendar_links import create_google_calendar_link
from datetime import datetime
from email.utils import formatdate
from icalendar import Calendar, Event, vText

class EmailSender:
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.ssl_context = ssl.create_default_context()

    @staticmethod
    def validate_email_address(email: str) -> bool:
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

    @staticmethod
    def create_ics_file(lesson: ScheduleElement) -> bytes:
        """Create an ICS file for a lesson"""
        cal = Calendar()
        cal.add('prodid', '-//Polytech Schedule Bot//RU')
        cal.add('version', '2.0')
        cal.add('method', 'REQUEST')  # This makes it an invitation

        event = Event()
        event.add('summary', f"{lesson.name} ({lesson.type})")
        event.add('dtstart', lesson.timing.start_date)
        event.add('dtend', lesson.timing.end_date)
        event.add('dtstamp', datetime.now())
        
        # Add location if available
        if lesson.auditory and lesson.auditory.name:
            event.add('location', vText(lesson.auditory.name))
        
        # Add description with teacher info
        description = f"Преподаватель: {lesson.teacher.name if lesson.teacher and lesson.teacher.name else 'Не указан'}"
        event.add('description', description)
        
        # Add organizer if teacher is available
        if lesson.teacher and lesson.teacher.name:
            event.add('organizer', f"CN={lesson.teacher.name}")
        
        # Add other required fields
        event.add('status', 'CONFIRMED')
        event.add('transp', 'OPAQUE')
        
        cal.add_component(event)
        return cal.to_ical()

    @staticmethod
    def format_lesson_email(lesson: ScheduleElement) -> tuple[str, str, str]:
        """Format email subject and bodies (plain text and HTML) for a lesson"""
        # Format subject
        subject = f"Приглашение: {lesson.name} ({lesson.type})"
        
        # Format plain text body
        plain_text = (
            f"{lesson.name} ({lesson.type})\n"
            f"\n"
            f"Когда: {lesson.timing.start_date.strftime('%A, %d %B %Y')}\n"
            f"Время: {lesson.timing.start_date.strftime('%H:%M')} - {lesson.timing.end_date.strftime('%H:%M')}\n"
            f"Место: {lesson.auditory.name if lesson.auditory and lesson.auditory.name else 'Не указано'}\n"
            f"Преподаватель: {lesson.teacher.name if lesson.teacher and lesson.teacher.name else 'Не указан'}\n\n"
            f"* Календарное приглашение находится во вложении"
        )

        # Format HTML body
        html_body = f"""
        <html>
        <body>
        <div style="font-family: Arial, sans-serif;">
            <h2>{lesson.name} ({lesson.type})</h2>
            <p>
                <strong>Когда:</strong> {lesson.timing.start_date.strftime('%A, %d %B %Y')}<br>
                <strong>Время:</strong> {lesson.timing.start_date.strftime('%H:%M')} - {lesson.timing.end_date.strftime('%H:%M')}<br>
                <strong>Место:</strong> {lesson.auditory.name if lesson.auditory and lesson.auditory.name else 'Не указано'}<br>
                <strong>Преподаватель:</strong> {lesson.teacher.name if lesson.teacher and lesson.teacher.name else 'Не указан'}
            </p>
            <p><em>* Календарное приглашение находится во вложении</em></p>
        </div>
        </body>
        </html>
        """
        
        return subject, plain_text, html_body

    async def send_lesson_email(
        self,
        to_email: str,
        lesson: ScheduleElement
    ) -> bool:
        """Send email with ICS attachment for a lesson"""
        if not self.validate_email_address(to_email):
            return False

        subject, plain_text, html_body = self.format_lesson_email(lesson)

        # Create multipart message
        message = MIMEMultipart('mixed')
        message["From"] = self.username
        message["To"] = to_email
        message["Subject"] = subject
        message["Date"] = formatdate(localtime=True)

        # Create alternative part for text and HTML
        alt_part = MIMEMultipart('alternative')
        alt_part.attach(MIMEText(plain_text, 'plain', 'utf-8'))
        alt_part.attach(MIMEText(html_body, 'html', 'utf-8'))
        message.attach(alt_part)

        # Create and attach ICS file
        ics_content = self.create_ics_file(lesson)
        ics_part = MIMEBase('text', 'calendar', method='REQUEST')
        ics_part.set_payload(ics_content)
        encoders.encode_base64(ics_part)
        ics_part.add_header('Content-Type', 'text/calendar; charset="UTF-8"; method=REQUEST')
        ics_part.add_header('Content-Disposition', 'attachment', filename='invite.ics')
        message.attach(ics_part)

        try:
            # Send email with STARTTLS
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.username,
                password=self.password,
                start_tls=True,
                tls_context=self.ssl_context
            )
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    async def send_schedule(
        self,
        to_email: str,
        lessons: List[ScheduleElement]
    ) -> bool:
        """Send separate email for each lesson in schedule"""
        if not lessons:
            return True

        success = True
        for lesson in lessons:
            if not await self.send_lesson_email(to_email, lesson):
                success = False
                
        return success 