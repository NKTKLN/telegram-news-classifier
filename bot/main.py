from bot.telegram_bot import TelegramBot
from bot.logging_config import setup_logger

setup_logger()

bot = TelegramBot()
bot.client.run_until_disconnected()
