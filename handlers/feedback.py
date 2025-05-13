from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states.forms import FeedbackForm
from config.config import GROUP_ID, MESSAGE_THREAD_ID
import logging

def register_feedback_handlers(dp: Dispatcher):
    dp.message.register(start_feedback, Command('feedback'))
    dp.message.register(process_feedback_message, 
                       FeedbackForm.collecting,
                       lambda message: message.text and message.text != "/delete")
    dp.message.register(process_feedback_media, 
                       FeedbackForm.collecting,
                       lambda message: message.photo or message.video or 
                                     message.voice or message.video_note or 
                                     message.audio)
    dp.callback_query.register(handle_feedback_callback, FeedbackForm.collecting)

async def start_feedback(message: types.Message, state: FSMContext):
    await state.set_state(FeedbackForm.collecting)
    await state.update_data(messages=[])
    
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✅ Завершить", callback_data="finish_feedback")],
        [types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_feedback")]
    ])
    
    await message.answer(
        "Пожалуйста, отправьте ваши сообщения для отзыва.\n\n"
        "Вы можете отправить несколько сообщений подряд (текст, фото, видео, голосовые сообщения).\n"
        "После отправки всех сообщений нажмите кнопку 'Завершить'.\n\n"
        "Чтобы удалить последнее сообщение, используйте команду /delete\n"
        "Чтобы отменить отправку отзыва, нажмите 'Отменить'",
        reply_markup=markup
    )

async def process_feedback_message(message: types.Message, state: FSMContext):
    if message.text == "/delete":
        data = await state.get_data()
        messages = data.get("messages", [])
        if messages:
            messages.pop()
            await state.update_data(messages=messages)
            await message.answer("✅ Последнее сообщение удалено")
        else:
            await message.answer("❌ Нет сообщений для удаления")
        return

    data = await state.get_data()
    messages = data.get("messages", [])
    
    # Сохраняем информацию о сообщении
    message_data = {
        "type": "text",
        "content": message.text
    }
    messages.append(message_data)
    await state.update_data(messages=messages)
    
    await message.answer("✅ Сообщение добавлено к отзыву")

async def process_feedback_media(message: types.Message, state: FSMContext):
    data = await state.get_data()
    messages = data.get("messages", [])
    
    # Сохраняем информацию о медиа
    message_data = {
        "type": "media",
        "file_id": None,
        "caption": message.caption
    }
    
    if message.photo:
        message_data["type"] = "photo"
        message_data["file_id"] = message.photo[-1].file_id
    elif message.video:
        message_data["type"] = "video"
        message_data["file_id"] = message.video.file_id
    elif message.voice:
        message_data["type"] = "voice"
        message_data["file_id"] = message.voice.file_id
    elif message.video_note:
        message_data["type"] = "video_note"
        message_data["file_id"] = message.video_note.file_id
    elif message.audio:
        message_data["type"] = "audio"
        message_data["file_id"] = message.audio.file_id
    
    messages.append(message_data)
    await state.update_data(messages=messages)
    
    await message.answer("✅ Медиа добавлено к отзыву")

async def handle_feedback_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "finish_feedback":
        data = await state.get_data()
        messages = data.get("messages", [])
        
        if not messages:
            await callback_query.message.answer("❌ Нет сообщений для отправки")
            return
        
        username = callback_query.from_user.username or callback_query.from_user.full_name
        header = f"📝 Отзыв от @{username}:\n\n"
        
        # Отправляем все сообщения в группу
        for msg in messages:
            try:
                if msg["type"] == "text":
                    await callback_query.bot.send_message(
                        GROUP_ID,
                        header + msg["content"],
                        message_thread_id=MESSAGE_THREAD_ID
                    )
                elif msg["type"] == "photo":
                    await callback_query.bot.send_photo(
                        GROUP_ID,
                        msg["file_id"],
                        caption=header + (msg["caption"] or ""),
                        message_thread_id=MESSAGE_THREAD_ID
                    )
                elif msg["type"] == "video":
                    await callback_query.bot.send_video(
                        GROUP_ID,
                        msg["file_id"],
                        caption=header + (msg["caption"] or ""),
                        message_thread_id=MESSAGE_THREAD_ID
                    )
                elif msg["type"] == "voice":
                    await callback_query.bot.send_voice(
                        GROUP_ID,
                        msg["file_id"],
                        caption=header + (msg["caption"] or ""),
                        message_thread_id=MESSAGE_THREAD_ID
                    )
                elif msg["type"] == "video_note":
                    await callback_query.bot.send_message(
                        GROUP_ID,
                        header,
                        message_thread_id=MESSAGE_THREAD_ID
                    )
                    await callback_query.bot.send_video_note(
                        GROUP_ID,
                        msg["file_id"],
                        message_thread_id=MESSAGE_THREAD_ID
                    )
                elif msg["type"] == "audio":
                    await callback_query.bot.send_audio(
                        GROUP_ID,
                        msg["file_id"],
                        caption=header + (msg["caption"] or ""),
                        message_thread_id=MESSAGE_THREAD_ID
                    )
            except Exception as e:
                logging.error(f"Ошибка при отправке сообщения: {e}")
        
        await state.clear()
        await callback_query.message.answer(
            "Спасибо за ваш отзыв — это поможет нам стать лучше 🖤",
            reply_markup=types.ReplyKeyboardRemove()
        )
    
    elif callback_query.data == "cancel_feedback":
        await state.clear()
        await callback_query.message.answer(
            "❌ Отправка отзыва отменена",
            reply_markup=types.ReplyKeyboardRemove()
        )
    
    await callback_query.answer() 