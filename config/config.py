import os
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

try:
    GROUP_ID = int(os.getenv("GROUP_ID", "0"))
    MESSAGE_THREAD_ID = int(os.getenv("MESSAGE_THREAD_ID", "0"))
except ValueError:
    raise ValueError("GROUP_ID and MESSAGE_THREAD_ID must be valid integers")

if GROUP_ID == 0:
    raise ValueError("GROUP_ID environment variable is not set")
if MESSAGE_THREAD_ID == 0:
    raise ValueError("MESSAGE_THREAD_ID environment variable is not set")

DEFAULT_BOT_PROPERTIES = DefaultBotProperties(parse_mode=ParseMode.HTML) 