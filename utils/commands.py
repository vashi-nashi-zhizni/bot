from aiogram import Bot, types

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Начать работу"),
        types.BotCommand(command="/feedback", description="Оставить отзыв (можно отправить несколько сообщений)"),
        types.BotCommand(command="/question", description="Задать вопрос (можно отправить несколько сообщений)"),
        types.BotCommand(command="/history", description="Рассказать историю (можно отправить несколько сообщений)"),
        types.BotCommand(command="/expert", description="Стать экспертом"),
        types.BotCommand(command="/guest", description="Стать гостем"),
        types.BotCommand(command="/cancel", description="Отменить действие"),
        types.BotCommand(command="/delete", description="Удалить последнее сообщение")
    ]
    await bot.set_my_commands(commands) 