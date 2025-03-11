from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states.forms import GuestForm
from config.config import GROUP_ID, MESSAGE_THREAD_ID
import logging

def register_guest_handlers(dp: Dispatcher):
    dp.message.register(start_guest_form, Command('guest'))
    dp.message.register(process_name, StateFilter(GuestForm.name))
    dp.message.register(process_age, StateFilter(GuestForm.age))
    dp.message.register(process_country, StateFilter(GuestForm.country))
    dp.message.register(process_job, StateFilter(GuestForm.job))
    dp.message.register(process_story, StateFilter(GuestForm.story))
    dp.message.register(process_meeting_time, StateFilter(GuestForm.meeting_time))

async def start_guest_form(message: types.Message, state: FSMContext):
    await state.set_state(GuestForm.name)
    await message.answer("Пожалуйста, ответьте на вопросы:\n1. Как тебя зовут?")

async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(GuestForm.age)
    await message.answer("2. Сколько тебе лет?")

async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(GuestForm.country)
    await message.answer("3. В какой ты сейчас стране?")

async def process_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(GuestForm.job)
    await message.answer("4. Кем ты работаешь?")

async def process_job(message: types.Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state(GuestForm.story)
    await message.answer("5. О чём ты хочешь рассказать в подкасте?")

async def process_story(message: types.Message, state: FSMContext):
    await state.update_data(story=message.text)
    await state.set_state(GuestForm.meeting_time)
    await message.answer("6. Когда ты готов встретиться? (Даты и время)")

async def process_meeting_time(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = message.from_user.username or message.from_user.full_name
    
    guest_data = (
        f"🎧 Анкета гостя от @{username}:\n\n"
        f"1. Имя: {data['name']}\n"
        f"2. Возраст: {data['age']}\n"
        f"3. Страна: {data['country']}\n"
        f"4. Профессия: {data['job']}\n"
        f"5. История: {data['story']}\n"
        f"6. Время встречи: {message.text}"
    )
    
    await message.bot.send_message(GROUP_ID, guest_data, message_thread_id=MESSAGE_THREAD_ID)
    await state.clear()
    await message.answer(
        "Благодарим за ответы на наши вопросы!\n\n"
        "Что дальше?\n\n"
        "🧿 Дождаться обратной связи по анкете\n"
        "🧿 Встретиться на прединтервью в Zoom"
    ) 