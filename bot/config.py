import os
import yaml
import logging
from typing import Dict, List


class ConfigWorker:
    def __init__(self, config_path: str, create_empty: bool = False):
        """
        Initialize the ConfigWorker.

        :param config_path: Path to the configuration file.
        :param create_empty: Whether to create an empty file if it doesn't exist.
        """
        self.config_path = config_path
        self.create_empty = create_empty
        self._config = self._load_config()

    def _load_config(self) -> Dict:
        """
        Load the configuration from the YAML file.
        Creates an empty file if it doesn't exist and create_empty is True.

        :return: Loaded configuration as a dictionary.
        """
        if not os.path.exists(self.config_path) and self.create_empty:
            with open(self.config_path, 'w', encoding='utf-8'):
                pass  # Create an empty file
            logging.info(f"Created an empty config file at {self.config_path}")

        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file) or {}
                logging.info(f"Configuration loaded from {self.config_path}")
                return config
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file: {e}")
            raise ValueError(f"Error parsing YAML file: {e}")

    def _save_config(self) -> None:
        """
        Save the current configuration to the YAML file.
        """
        with open(self.config_path, 'w', encoding='utf-8') as file:
            yaml.safe_dump(self._config, file, default_flow_style=False, allow_unicode=True)
            logging.info(f"Configuration saved to {self.config_path}")


class MainConfig(ConfigWorker):
    @property
    def telegram(self) -> Dict:
        """
        Access the 'telegram' section of the configuration.

        :return: Dictionary containing Telegram-related settings.
        """
        return self._config.get('telegram', {})

    @property
    def sqlite(self) -> Dict:
        """
        Access the 'sqlite' section of the configuration.

        :return: Dictionary containing SQLite-related settings.
        """
        return self._config.get('sqlite', {})

    @property
    def bot_settings(self) -> Dict:
        """
        Access the 'bot_settings' section of the configuration.

        :return: Dictionary containing bot settings.
        """
        return self._config.get('bot_settings', {})

    @property
    def categories(self) -> Dict:
        """
        Access the 'categories' section of the configuration.

        :return: Dictionary containing category settings.
        """
        return self._config.get('categories', {})

    @property
    def exclude_categories(self) -> List:
        """
        Access the 'exclude_categories' section of the configuration.

        :return: List of excluded categories.
        """
        return self._config.get('exclude_categories', [])


class TelegramConfig(ConfigWorker):
    def _ensure_key(self) -> None:
        """
        Ensure that the 'topics' key exists in the configuration.
        """
        key = "topics"
        if key not in self._config:
            self._config[key] = []
            logging.info("Added 'topics' key to configuration.")

    @property
    def topics(self) -> List:
        """
        Access the list of topics in the configuration.

        :return: List of topics.
        """
        return self._config.get('topics', [])

    @property
    def forum_id(self) -> int:
        """
        Access the forum ID in the configuration.

        :return: Forum ID as an integer.
        """
        return self._config.get('forum_id', None)

    def add_topic(self, topic_id: int, category: int) -> None:
        """
        Add a new topic to the configuration if it doesn't already exist.

        :param topic_id: ID of the topic to add.
        :param category: Category ID associated with the topic.
        """
        self._ensure_key()
        existing_topics = self.topics

        # Add the topic only if it doesn't already exist
        if not any(topic['id'] == topic_id for topic in existing_topics):
            self._config['topics'].append({'id': topic_id, 'category': category})
            self._save_config()
            self._load_config()
            logging.info(f"Topic with ID {topic_id} added to category {category}.")

    def add_forum_id(self, forum_id: int) -> None:
        """
        Set the forum ID in the configuration.

        :param forum_id: Forum ID to set.
        """
        self._config['forum_id'] = forum_id
        self._save_config()
        self._load_config()
        logging.info(f"Forum ID {forum_id} set in configuration.")
