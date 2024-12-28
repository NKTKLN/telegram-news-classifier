from bot.telegram_bot import TelegramBot
import logging

# Configure the logging system
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] : %(name)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

bot = TelegramBot()
bot.client.run_until_disconnected()
