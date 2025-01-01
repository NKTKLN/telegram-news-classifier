from bot.db import DuckDBHandler
from bot.classifier import TextClassifier
from bot.text_similarity import TextSimilarity
from bot.config import MainConfig, TelegramConfig

# Configuring the main bot settings by loading configuration from the YAML file
config = MainConfig("config/config.yaml")
telegram_config = TelegramConfig("config/bot_config.yaml", True)

# Initializing the text classifier with the model path specified in the bot settings
classifier = TextClassifier(model_path=config.bot_settings.get("model_path"))

# Initializing the TextSimilarity object for comparing message text similarity
text_similarity = TextSimilarity()  # Used for checking if new messages are similar to previous ones

# Setting up the database handler with the database file path from the configuration
db_handler = DuckDBHandler(db_file=config.bot_settings.get("db_path"))
