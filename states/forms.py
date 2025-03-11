from aiogram.fsm.state import State, StatesGroup

class FeedbackState(StatesGroup):
    waiting = State()
    media_processing = State()

class QuestionState(StatesGroup):
    waiting = State()
    media_processing = State()

class HistoryState(StatesGroup):
    waiting = State()
    media_processing = State()

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