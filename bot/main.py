from bot.telegram_bot import TelegramManager
from bot.logger import setup_logger


if __name__ == "__main__":
    # Setting up the logger to ensure proper logging throughout the bot's execution
    setup_logger()

    # Initializing the Telegram bot manager to start the bot and handle events
    TelegramManager()
