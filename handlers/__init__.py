from aiogram import Dispatcher
from aiogram.filters import Command, StateFilter
from .common import send_welcome, cancel_handler
from .feedback import register_feedback_handlers
from .question import register_question_handlers
from .history import register_history_handlers
from .expert import register_expert_handlers
from .guest import register_guest_handlers
from .admin import register_admin_handlers

def register_all_handlers(dp: Dispatcher):
    # Регистрация общих обработчиков
    dp.message.register(send_welcome, Command('start'))
    dp.message.register(cancel_handler, Command('cancel'), StateFilter('*'))
    
    # Регистрация остальных обработчиков
    register_feedback_handlers(dp)
    register_question_handlers(dp)
    register_history_handlers(dp)
    register_expert_handlers(dp)
    register_guest_handlers(dp)
    register_admin_handlers(dp) 