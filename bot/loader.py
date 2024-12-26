from bot.config import MainConfig, TelegramConfig
from bot.classifier import TextClassifier

# Configuring the bot
config = MainConfig("config/config.yaml")
telegram_config = TelegramConfig("config/bot_config.yaml", True)

# Initializing the classifier with the model path from the configuration
# classifier = TextClassifier(model_path=config.bot_settings.get("model_path"))
