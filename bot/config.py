import os
import yaml
import logging
from typing import Dict, List

# Setting up logging
logger = logging.getLogger(__name__)

class ConfigWorker:
    def __init__(self, file_path: str, create_empty: bool = False):
        """
        Initialize the FileConfigStorage.

        :param file_path: Path to the configuration file.
        :param create_empty: Whether to create an empty file if it doesn't exist.
        """
        self.file_path = file_path
        self.config = {}
        if create_empty:
            self._create_empty_file()
        self.load()

    def _create_empty_file(self) -> None:
        """Create an empty config file if it doesn't exist."""
        if os.path.exists(self.file_path):
            return
        with open(self.file_path, 'w', encoding='utf-8'):
            pass  # Create an empty file
        logger.info(f"Created an empty config file at {self.file_path}")

    def load(self) -> None:
        """Load the configuration from the YAML file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file) or {}
            logger.info(f"Configuration loaded from {self.file_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            raise ValueError(f"Error parsing YAML file: {e}")

    def save(self) -> None:
        """Save the configuration to the YAML file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                yaml.safe_dump(self.config, file, default_flow_style=False, allow_unicode=True)
            logger.info(f"Configuration saved to {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise

class MainConfig(ConfigWorker):
    @property
    def telegram(self) -> Dict:
        """Access the 'telegram' section of the configuration."""
        return self.config.get('telegram', {})

    # @property
    # def sqlite(self) -> Dict:
    #     """Access the 'sqlite' section of the configuration."""
    #     return self.config.get('sqlite', {})

    @property
    def bot_settings(self) -> Dict:
        """Access the 'bot_settings' section of the configuration."""
        return self.config.get('bot_settings', {})

    @property
    def categories(self) -> Dict:
        """Access the 'categories' section of the configuration."""
        return self.config.get('categories', {})

    @property
    def exclude_categories(self) -> List:
        """Access the 'exclude_categories' section of the configuration."""
        return self.config.get('exclude_categories', [])

class TelegramConfig(ConfigWorker):
    @property
    def topics(self) -> List:
        """Access the list of topics in the configuration."""
        return self.config.setdefault('topics', [])

    @property
    def forum_id(self) -> int:
        """Access the forum ID in the configuration."""
        return self.config.get('forum_id', None)

    def add_topic(self, topic_id: int, category: int) -> None:
        """
        Add a new topic to the configuration if it doesn't already exist.

        :param topic_id: ID of the topic to add.
        :param category: Category ID associated with the topic.
        """
        topics = self.topics
        if not any(topic['id'] == topic_id for topic in topics):
            topics.append({'id': topic_id, 'category': category})
            self.save()  # Save the updated config
            logger.info(f"Topic with ID {topic_id} added to category {category}.")

    def add_forum_id(self, forum_id: int) -> None:
        """
        Set the forum ID in the configuration.

        :param forum_id: Forum ID to set.
        """
        self.config['forum_id'] = forum_id
        self.save()  # Save the updated config
        logger.info(f"Forum ID {forum_id} set in configuration.")
