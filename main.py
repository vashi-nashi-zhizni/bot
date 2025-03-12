import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import TOKEN, DEFAULT_BOT_PROPERTIES, GROUP_ID, MESSAGE_THREAD_ID
from utils.commands import set_commands
from handlers import register_all_handlers
from states.forms import register_all_states

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# Инициализация бота глобально для использования в функции уведомления
bot = Bot(token=TOKEN, default=DEFAULT_BOT_PROPERTIES)

async def send_startup_notification():
    """Отправляет уведомление о запуске бота в админ-канал"""
    try:
        environment = "PRODUCTION" if GROUP_ID else "DEVELOPMENT"
        await bot.send_message(
            GROUP_ID,
            f"🚀 Бот запущен в режиме {environment}\n"
            f"Версия: {sys.version}\n"
            f"Время запуска: {logging.Formatter().formatTime(logging.LogRecord('', 0, '', 0, '', 0, None, None))}",
            message_thread_id=MESSAGE_THREAD_ID
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления о запуске: {e}")

async def main():
    # Инициализация диспетчера
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация состояний и обработчиков
    register_all_states(dp)
    register_all_handlers(dp)
    
    # Установка команд бота
    await set_commands(bot)
    
    # Запуск бота
    logging.info("Бот запускается...")
    
    # Отправка уведомления о запуске
    await send_startup_notification()
    
    # Запуск поллинга
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 