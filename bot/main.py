import logging
import argparse

from apscheduler.schedulers.background import BackgroundScheduler

from bot.db import DuckDBHandler
from bot.logger import setup_logger
from bot.telegram_bot import TelegramManager
from bot.config import MainConfig, TelegramConfig

# Setting up logging
logger = logging.getLogger(__name__)

def main() -> None:
    # Set up the logger
    setup_logger()

    # Load the configuration files
    try:
        config = MainConfig("config/config.yaml")
        telegram_config = TelegramConfig("config/bot_config.yaml", True)
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        return
    except Exception as e:
        logger.error(f"An error occurred while loading config: {e}")
        return

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Telegram News Classifier")
    parser.add_argument('--login', action='store_true', help="Authorization only, no full launch.")
    args = parser.parse_args()

    # Initialize the database handler with the path from the configuration
    db_handler = DuckDBHandler(db_file=config.bot_settings.get("db_path"))

    # Set up a recurring task to clean up old messages from the database
    scheduler = BackgroundScheduler()
    scheduler.add_job(db_handler.cleanup_old_messages, 'interval', hours=2)
    scheduler.start()

    # Initialize and start the Telegram bot manager
    TelegramManager(config, telegram_config, db_handler, args.login)


if __name__ == "__main__":
    main()
