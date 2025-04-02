import os
from aiogram import Bot
from dotenv import load_dotenv
from emoji import emojize
from tg_bot.lexicon.messages import lexicon as msgs_lexicon

async def notification(bot: Bot, message: str = msgs_lexicon['service']['reboot_ok']) -> None:
    load_dotenv()
    await bot.send_message(
        chat_id=os.getenv('ADMIN_1_ID'),
        text=f"{emojize(':information:')} {message}"
    )
