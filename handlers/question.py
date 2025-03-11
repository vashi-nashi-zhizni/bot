from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.forms import QuestionState
from config.config import GROUP_ID, MESSAGE_THREAD_ID
import logging

def register_question_handlers(dp: Dispatcher):
    dp.message.register(start_question, Command('question'))
    dp.message.register(request_media_for_question,
                       QuestionState.waiting,
                       lambda message: message.text == "Добавить медиа")
    dp.message.register(process_question_text,
                       QuestionState.waiting,
                       lambda message: message.text != "Добавить медиа")
    dp.message.register(process_question_with_media,
                       QuestionState.media_processing,
                       lambda message: message.video or message.audio or 
                                     message.video_note or message.voice)
    dp.message.register(process_question_media_fallback,
                       QuestionState.media_processing)

async def start_question(message: types.Message, state: FSMContext):
    await state.set_state(QuestionState.waiting)
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Отправить без медиа")],
            [types.KeyboardButton(text="Добавить медиа")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Пожалуйста, задайте ваш вопрос:", reply_markup=markup)

# Добавляем после start_question
async def request_media_for_question(message: types.Message, state: FSMContext):
    await state.set_state(QuestionState.media_processing)
    await message.answer(
        "Пожалуйста, отправьте ваше видео, аудио, голосовое сообщение или круговое видео:",
        reply_markup=types.ReplyKeyboardRemove()
    )

async def process_question_text(message: types.Message, state: FSMContext):
    if message.text == "Отправить без медиа":
        await message.answer("Пожалуйста, задайте ваш вопрос:")
        return
    
    username = message.from_user.username or message.from_user.full_name
    question_text = f"❓ Вопрос от @{username} (ID: {message.from_user.id}):\n\n{message.text}"
    await message.bot.send_message(GROUP_ID, question_text, message_thread_id=MESSAGE_THREAD_ID)
    await message.answer("Спасибо за ваш вопрос! Ответим в ближайшее время 🧿")
    await state.clear()

async def process_question_with_media(message: types.Message, state: FSMContext):
    username = message.from_user.username or message.from_user.full_name
    caption = message.caption or "Вопрос без текста"
    header_text = f"❓ Вопрос с медиа от @{username} (ID: {message.from_user.id}):\n\n{caption}"
    
    try:
        if message.video:
            await message.bot.send_video(GROUP_ID, message.video.file_id, caption=header_text, message_thread_id=MESSAGE_THREAD_ID)
        elif message.audio:
            await message.bot.send_audio(GROUP_ID, message.audio.file_id, caption=header_text, message_thread_id=MESSAGE_THREAD_ID)
        elif message.voice:
            await message.bot.send_voice(GROUP_ID, message.voice.file_id, caption=header_text, message_thread_id=MESSAGE_THREAD_ID)
        elif message.video_note:
            await message.bot.send_message(GROUP_ID, header_text, message_thread_id=MESSAGE_THREAD_ID)
            await message.bot.send_video_note(GROUP_ID, message.video_note.file_id, message_thread_id=MESSAGE_THREAD_ID)
        
        await message.answer("Спасибо за ваш вопрос с медиа! Ответим в ближайшее время 🧿")
    except Exception as e:
        logging.error(f"Ошибка при отправке медиа: {e}")
        await message.answer("❌ Произошла ошибка при отправке медиа")
    await state.clear()

async def process_question_media_fallback(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте медиафайл или используйте /cancel для отмены.")

# Остальные обработчики question переносятся аналогично 