from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states.forms import ExpertForm
from config.config import GROUP_ID, MESSAGE_THREAD_ID
import logging

def register_expert_handlers(dp: Dispatcher):
    dp.message.register(start_expert_form, Command('expert'))
    dp.message.register(process_name, StateFilter(ExpertForm.name))
    dp.message.register(process_country, StateFilter(ExpertForm.country))
    dp.message.register(process_job, StateFilter(ExpertForm.job))
    dp.message.register(process_specialization, StateFilter(ExpertForm.specialization))
    dp.message.register(process_topic, StateFilter(ExpertForm.topic))
    dp.message.register(process_meeting_time, StateFilter(ExpertForm.meeting_time))
    dp.message.register(process_motivation, StateFilter(ExpertForm.motivation))

async def start_expert_form(message: types.Message, state: FSMContext):
    await state.set_state(ExpertForm.name)
    await message.answer("Пожалуйста, ответьте на вопросы:\n1. Как вас зовут?")

async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ExpertForm.country)
    await message.answer("2. В какой вы сейчас стране?")

async def process_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(ExpertForm.job)
    await message.answer("3. Кем вы работаете?")

async def process_job(message: types.Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state(ExpertForm.specialization)
    await message.answer("4. На чём вы специализируетесь?")

async def process_specialization(message: types.Message, state: FSMContext):
    await state.update_data(specialization=message.text)
    await state.set_state(ExpertForm.topic)
    await message.answer("5. Какую тему вы хотите раскрыть в подкасте «ВНЖ»?")

async def process_topic(message: types.Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await state.set_state(ExpertForm.meeting_time)
    await message.answer("6. Когда вы готовы встретиться? (Даты и время)")

async def process_meeting_time(message: types.Message, state: FSMContext):
    await state.update_data(meeting_time=message.text)
    await state.set_state(ExpertForm.motivation)
    await message.answer("7. Почему хотите присоединиться к нам?")

async def process_motivation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = message.from_user.username or message.from_user.full_name
    
    expert_data = (
        f"🎙️ Анкета эксперта от @{username}:\n\n"
        f"1. Имя: {data['name']}\n"
        f"2. Страна: {data['country']}\n"
        f"3. Профессия: {data['job']}\n"
        f"4. Специализация: {data['specialization']}\n"
        f"5. Тема: {data['topic']}\n"
        f"6. Время встречи: {data['meeting_time']}\n"
        f"7. Мотивация: {message.text}"
    )
    
    await message.bot.send_message(GROUP_ID, expert_data, message_thread_id=MESSAGE_THREAD_ID)
    await state.clear()
    await message.answer(
        "Благодарим за ответы на наши вопросы!\n\n"
        "Что дальше?\n\n"
        "🧿 Дождитесь обратной связи по анкете\n"
        "🧿 Встретиться на прединтервью в Zoom"
    ) 