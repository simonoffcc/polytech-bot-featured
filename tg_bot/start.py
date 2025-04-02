import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import bot, dp
from utils.env_to_dist import move_env_vars
from utils.mock_data_updaters import update_groups_data, update_teachers_data, create_mock_folder_and_data

from utils.notification import notification

async def on_startup():
    await notification(bot)

    # задачи обновления mock-данных
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_groups_data, 'cron', hour=4, minute=5)
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
