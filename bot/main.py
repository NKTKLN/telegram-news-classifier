import logging

from apscheduler.schedulers.background import BackgroundScheduler

from bot.db import DuckDBHandler
from bot.logger import setup_logger
from bot.telegram_bot import TelegramManager
from bot.config import MainConfig, TelegramConfig

# Setting up logging
logger = logging.getLogger(__name__)

def main() -> None:
    # Setting up the logger to ensure proper logging throughout the bot's execution
    setup_logger()

    # Configuring the main bot settings by loading configuration from the YAML file
    try:
        config = MainConfig("config/config.yaml")
        telegram_config = TelegramConfig("config/bot_config.yaml", True)
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        return
    except Exception as e:
        logger.error(f"An error occurred while loading config: {e}")
        return

    # Setting up the database handler with the database file path from the configuration
    db_handler = DuckDBHandler(db_file=config.bot_settings.get("db_path"))

    # Initialization of the deferred recurring task of clearing old messages from the database
    scheduler = BackgroundScheduler()
    scheduler.add_job(db_handler.cleanup_old_messages, 'interval', hours=2)
    scheduler.start()

    # Initializing the Telegram bot manager to start the bot and handle events
    TelegramManager(config, telegram_config, db_handler)


if __name__ == "__main__":
    main()
