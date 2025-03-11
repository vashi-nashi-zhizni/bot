from aiogram import types, Bot, Dispatcher
from config.config import GROUP_ID
import logging

def register_admin_handlers(dp: Dispatcher):
    dp.message.register(handle_admin_reply,
                       lambda message: message.chat.id == GROUP_ID and 
                                     message.reply_to_message)

async def handle_admin_reply(message: types.Message):
    try:
        original_message = message.reply_to_message.text
        if "(ID: " in original_message:
            user_id = int(original_message.split('(ID: ')[1].split(')')[0])
            await message.bot.send_message(
                user_id,
                f"📩 Ответ от администратора:\n\n{message.text}"
            )
    except Exception as e:
        logging.error(f"Ошибка обработки ответа: {e}") 