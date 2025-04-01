from aiogram import Router
from aiogram.types import Message

from datetime import date
from db_orm.crud import update_puffins_status
from db_orm.models import PuffinsHistory

CHANNEL_ID = '-1001711842554'

router = Router()

@router.channel_post(lambda message: message.chat.type == 'channel' and str(message.chat.id) == CHANNEL_ID)
async def channel_post_handler(channel_post: Message):
    try:
        # Определяем, были ли пышки на основе сообщения
        message_text = channel_post.text.lower()
        is_puffins = None
        
        if "да" in message_text:
            is_puffins = True
        elif "нет" in message_text:
            is_puffins = False
            
        # Обновляем запись в базе данных
        update_puffins_status(
            message=channel_post.text,
            is_puffins=is_puffins
        )
        
    except Exception as e:
        print(f"Error saving puffins data: {e}")