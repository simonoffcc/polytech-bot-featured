from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from handlers import start, menu, schedule, find_teacher, puffins
from puffins.service import router as puffins_service

load_dotenv()

bot = Bot(token=getenv('BOT_API_KEY'), default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher()

dp.include_routers(
    start.router,
    menu.router,
    schedule.router,
    find_teacher.router,
    puffins.router,
    puffins_service,
)
