from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
import logging

async def send_welcome(message: types.Message):
    text = (
        "Привет!\n\nРады видеть тебя в нашем боте! О чём бы ты хотел рассказать? 🧿\n\n"
        "Доступные команды:\n"
        "/feedback - Оставить отзыв\n"
        "/question - Задать вопрос\n"
        "/history - Рассказать историю\n"
        "/expert - Стать экспертом\n"
        "/guest - Стать гостем\n"
        "/cancel - Отменить текущее действие"
    )
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())

async def cancel_handler(message: types.Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        if not current_state:
            await message.answer("Нет активных действий для отмены")
            return
        
        await state.clear()
        await message.answer(
            "✅ Опрос успешно отменен",
            reply_markup=types.ReplyKeyboardRemove()
        )
    except Exception as e:
        logging.error(f"Ошибка при отмене: {e}")
        await message.answer("❌ Не удалось отменить опрос") 