from aiogram import Bot, types

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Начать работу"),
        types.BotCommand(command="/feedback", description="Оставить отзыв"),
        types.BotCommand(command="/question", description="Задать вопрос"),
        types.BotCommand(command="/history", description="Рассказать историю"),
        types.BotCommand(command="/expert", description="Стать экспертом"),
        types.BotCommand(command="/guest", description="Стать гостем"),
        types.BotCommand(command="/cancel", description="Отменить действие")
    ]
    await bot.set_my_commands(commands) 