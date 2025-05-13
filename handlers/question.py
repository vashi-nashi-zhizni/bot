from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.forms import QuestionState
from config.config import GROUP_ID, MESSAGE_THREAD_ID
import logging

def register_question_handlers(dp: Dispatcher):
    dp.message.register(start_question, Command('question'))
    dp.message.register(process_question_message, 
                       QuestionState.collecting,
                       lambda message: message.text and message.text != "/delete")
    dp.message.register(process_question_media, 
                       QuestionState.collecting,
                       lambda message: message.photo or message.video or 
                                     message.voice or message.video_note or 
                                     message.audio)
    dp.callback_query.register(handle_question_callback, QuestionState.collecting)

async def start_question(message: types.Message, state: FSMContext):
    await state.set_state(QuestionState.collecting)
    await state.update_data(messages=[])
    
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✅ Завершить", callback_data="finish_question")],
        [types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_question")]
    ])
    
    await message.answer(
        "Пожалуйста, отправьте ваши сообщения с вопросом.\n\n"
        "Вы можете отправить несколько сообщений подряд (текст, фото, видео, голосовые сообщения).\n"
        "После отправки всех сообщений нажмите кнопку 'Завершить'.\n\n"
        "Чтобы удалить последнее сообщение, используйте команду /delete\n"
        "Чтобы отменить отправку вопроса, нажмите 'Отменить'",
        reply_markup=markup
    )

async def process_question_message(message: types.Message, state: FSMContext):
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
    
    await message.answer("✅ Сообщение добавлено к вопросу")

async def process_question_media(message: types.Message, state: FSMContext):
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
    
    await message.answer("✅ Медиа добавлено к вопросу")

async def handle_question_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "finish_question":
        data = await state.get_data()
        messages = data.get("messages", [])
        
        if not messages:
            await callback_query.message.answer("❌ Нет сообщений для отправки")
            return
        
        username = callback_query.from_user.username or callback_query.from_user.full_name
        header = f"❓ Вопрос от @{username} (ID: {callback_query.from_user.id}):\n\n"
        
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
            "Спасибо за ваш вопрос! Ответим в ближайшее время 🧿",
            reply_markup=types.ReplyKeyboardRemove()
        )
    
    elif callback_query.data == "cancel_question":
        await state.clear()
        await callback_query.message.answer(
            "❌ Отправка вопроса отменена",
            reply_markup=types.ReplyKeyboardRemove()
        )
    
    await callback_query.answer() 