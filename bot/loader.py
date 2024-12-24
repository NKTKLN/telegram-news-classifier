from bot.config import Config
from bot.telegram_bot import TelegramBot
from bot.classifier import TextClassifier

# Configuring the bot
config = Config("bot/config.yaml")

# Initializing the classifier with the model path from the configuration
classifier = TextClassifier(model_path=config.bot_settings.get("model_path"))

# Creating an instance of the Telegram bot
bot = TelegramBot()
