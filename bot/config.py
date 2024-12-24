import yaml
from typing import Dict, List

class Config:
    def __init__(self, config_path: str):
        """
        Initializes the configuration with the given path to the config file.

        :param config_path: Path to the configuration file
        """
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> Dict:
        """
        Loads the configuration file into memory.

        :return: A dictionary representing the configuration
        """
        with open(self.config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file) or {}

    def _save_config(self) -> None:
        """
        Saves the current configuration to the file.
        """
        with open(self.config_path, 'w', encoding='utf-8') as file:
            yaml.safe_dump(self._config, file, default_flow_style=False, allow_unicode=True)

    def _ensure_key(self, *keys: str) -> None:
        """
        Ensures that the given nested keys exist in the configuration.
        If the keys are missing, empty dictionaries or lists are created.

        :param keys: A sequence of keys for the nested structure
        """
        d = self._config
        for key in keys:
            if key not in d:
                d[key] = {} if key != 'channels' and key != 'topics' else []
            d = d[key]

    @property
    def telegram(self) -> Dict:
        """Returns the Telegram configuration."""
        return self._config.get('telegram', {})

    @property
    def sqlite(self) -> Dict:
        """Returns the SQLite configuration."""
        return self._config.get('sqlite', {})

    @property
    def bot_settings(self) -> Dict:
        """Returns the bot settings."""
        return self._config.get('bot_settings', {})

    @property
    def categories(self) -> Dict:
        """Returns the categories."""
        return self._config.get('categories', {})

    @property
    def exclude_categories(self) -> List:
        """Returns the excluded categories."""
        return self._config.get('exclude_categories', [])

    def get_telegram_topics(self) -> List[Dict]:
        """Returns the list of Telegram topics."""
        return self.telegram.get('topics', [])

    def get_telegram_channels(self) -> List[Dict]:
        """Returns the list of Telegram channels."""
        return self.telegram.get('channels', [])

    def add_telegram_topic(self, topic_id: int, topic_topic_id: int) -> None:
        """
        Adds a new topic to the Telegram configuration if it doesn't already exist.

        :param topic_id: The ID of the topic
        :param topic_topic_id: The ID of the subtopic
        """
        self._ensure_key('telegram', 'topics')
        
        # Check if the topic already exists
        existing_topics = self.get_telegram_topics()
        if not any(topic['id'] == topic_id for topic in existing_topics):
            self._config['telegram']['topics'].append({'id': topic_id, 'topic_id': topic_topic_id})
            self._save_config()
            self._load_config()
