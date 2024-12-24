import yaml

class Config:
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
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
