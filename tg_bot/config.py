from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from .handlers import (start, menu, about, schedule, calendar_export, puffins, unknown_msg)
from puffins import service as puffins_service

load_dotenv()

bot = Bot(token=getenv('BOT_API_KEY'), default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher()

# SMTP_HOST = "smtp.mail.ru"
# SMTP_PORT = 587
# SMTP_USERNAME = "your-email@vk.com"
# SMTP_PASSWORD = "your-password"

dp.include_routers(
    start.router,
    menu.router,
    about.router,
    schedule.router,
    calendar_export.router,
    puffins.router,
    puffins_service.router,
    unknown_msg.router,
)
