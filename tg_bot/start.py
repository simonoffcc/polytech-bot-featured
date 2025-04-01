import asyncio
import logging
from os import getenv

from aiogram.types import ReplyKeyboardRemove

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from config import bot, dp
from utils.env_to_dist import move_env_vars
from utils.mock_data_updaters import update_groups_data, update_teachers_data, create_mock_folder_and_data
from lexicon.messages import lexicon as msgs_lexicon

async def on_startup():

    load_dotenv()
    await bot.send_message(
        chat_id=getenv('ADMIN_1_ID'),
        text=msgs_lexicon['service']['reboot_ok']
    )

    # задачи обновления mock-данных
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_groups_data, 'cron', hour=4, minute=5)
    scheduler.add_job(update_teachers_data, 'cron', hour=4, minute=10)
    scheduler.start()

    # перемещение env переменных в dist
    move_env_vars()

    # проверка наличия папки с mock данными
    await create_mock_folder_and_data()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
