from aiogram.fsm.state import State, StatesGroup
from aiogram import Dispatcher

class FeedbackForm(StatesGroup):
    collecting = State()       # Для сбора сообщений
    media_processing = State() # Для обработки медиафайлов

class QuestionState(StatesGroup):
    collecting = State()       # Для сбора сообщений
    media_processing = State() # Для обработки медиафайлов

class HistoryForm(StatesGroup):
    collecting = State()       # Для сбора сообщений
    media_processing = State() # Для обработки медиафайлов

class ExpertForm(StatesGroup):
    name = State()
    country = State()
    job = State()
    specialization = State()
    topic = State()
    meeting_time = State()
    motivation = State()

class GuestForm(StatesGroup):
    name = State()
    age = State()
    country = State()
    job = State()
    story = State()
    meeting_time = State()

class AdminForm(StatesGroup):
    waiting = State()

def register_all_states(dp: Dispatcher):
    """
    Регистрирует все состояния в диспетчере.
    В текущей версии aiogram это не требуется, но функция оставлена для совместимости
    и возможного расширения в будущем.
    """
    # В aiogram 3.x состояния не требуют явной регистрации в диспетчере
    pass 