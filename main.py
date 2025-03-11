import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import TOKEN, DEFAULT_BOT_PROPERTIES
from utils.commands import set_commands
from handlers import register_all_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=TOKEN, default=DEFAULT_BOT_PROPERTIES)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация всех обработчиков
    register_all_handlers(dp)
    
    # Установка команд бота
    await set_commands(bot)
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 