from typing import List
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email_validator import validate_email, EmailNotValidError
from utils.schedule_processor import ScheduleElement, DayScheduleElement, WeekScheduleElement
from utils.ics_generator import create_ics_calendar

class EmailSender:
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    @staticmethod
    def validate_email_address(email: str) -> bool:
        """
        Validates an email address.
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if email is valid, False otherwise
        """
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

    async def send_schedule(self, to_email: str, schedule: DayScheduleElement | WeekScheduleElement | List[ScheduleElement], title: str = "Расписание") -> bool:
        """
        Sends schedule as calendar invites to the specified email.
        
        Args:
            to_email: Recipient email address
            schedule: Schedule data (day, week, or list of lessons)
            title: Title for the calendar
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Create message container
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = 'Расписание занятий'

            # Add body
            body = "Во вложении находится ваше расписание в формате ICS.\n\n"
            body += "Вы можете открыть этот файл в любом календарном приложении "
            body += "(Google Calendar, Apple Calendar, Outlook и др.)."
            msg.attach(MIMEText(body, 'plain'))

            # Create and attach ICS file
            if isinstance(schedule, (DayScheduleElement, WeekScheduleElement)):
                calendar_data = create_ics_calendar(schedule, title)
            else:  # List[ScheduleElement]
                # Create a temporary DayScheduleElement to wrap the lessons
                day_schedule = DayScheduleElement(
                    timing=schedule[0].timing if schedule else None,
                    lessons=schedule
                )
                calendar_data = create_ics_calendar(day_schedule, title)

            ics_attachment = MIMEApplication(calendar_data, _subtype='ics')
            ics_attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename='schedule.ics'
            )
            msg.attach(ics_attachment)

            # Send email
            await aiosmtplib.send(
                message=msg.as_string(),
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.username,
                password=self.password,
                use_tls=True
            )
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False 