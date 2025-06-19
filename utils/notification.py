import os
from aiogram import Bot
from dotenv import load_dotenv
from emoji import emojize
from tg_bot.lexicon.messages import lexicon as msgs_lexicon
from os import getenv

from db_orm.crud import get_all_active_users
from db_orm.database import Session

async def notification(bot: Bot, message_text: str = 'Бот запущен!'):
    with Session() as session:
        users = get_all_active_users(session)

    for user in users:
        if user.telegram_id == int(getenv('ADMIN_ID')):
            await bot.send_message(chat_id=user.telegram_id, text=message_text)
