import asyncio
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config import bot, dp
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
    
    # Запускаем uvicorn вместе с ботом
    config = uvicorn.Config(
        app="webapp.main:app",
        host="0.0.0.0",
        port=8000,
        loop="asyncio"
    )
    server = uvicorn.Server(config)
    
    # Запускаем поллинг бота и сервер uvicorn параллельно
    await asyncio.gather(
        dp.start_polling(bot),
        server.serve()
    )


if __name__ == "__main__":
    # Этот блок больше не будет выполняться при стандартном запуске через uvicorn,
    # но полезен для прямого запуска файла, например, для отладки.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
