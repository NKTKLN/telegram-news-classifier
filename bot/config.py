import yaml

class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self._load_config()
    
    def _load_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as file:
            self._config = yaml.safe_load(file)

    @property
    def telegram(self):
        return self._config.get('telegram', {})
    
    @property
    def sqlite(self):
        return self._config.get('sqlite', {})
    
    @property
    def bot_settings(self):
        return self._config.get('bot_settings', {})
    
    @property
    def categories(self):
        return self._config.get('categories', {})
    
    @property
    def exclude_categories(self):
        return self._config.get('exclude_categories', [])

    def get_telegram_topic(self):
        return self.telegram.get('topics', [])
    
    def get_telegram_channels(self):
        return self.telegram.get('channels', [])

    def add_telegram_channel(self, channel_id: int, name: str = ""):
        if 'telegram' not in self._config:
            self._config['telegram'] = {}
        if 'channels' not in self._config['telegram']:
            self._config['telegram']['channels'] = []
        
        existing_channels = self.get_telegram_channels()
        if not any(channel['id'] == channel_id for channel in existing_channels):
            self._config['telegram']['channels'].append({'id': channel_id, 'name': name})
            self._save_config()
            self._load_config()

    def add_telegram_topic(self,  topic_id: int, topic_topic_id: int):
        if 'telegram' not in self._config:
            self._config['telegram'] = {}
        if 'topics' not in self._config['telegram']:
            self._config['telegram']['topics'] = []
        
        existing_topics = self.get_telegram_topics()
        if not any(topic['id'] == topic_id for topic in existing_topics):
            self._config['telegram']['topics'].append({'id': topic_id, 'topic_id': topic_topic_id})
            self._save_config()
            self._load_config()

    def _save_config(self):
        """Сохраняет текущую конфигурацию в файл."""
        with open(self.config_path, 'w', encoding='utf-8') as file:
            yaml.safe_dump(self._config, file, default_flow_style=False, allow_unicode=True)
