from telethon import TelegramClient, events
from telethon.events import NewMessage
from bot.loader import config

class TelegramBot:
    def __init__(self):
        """
        Initializes the TelegramBot instance by loading the configuration values
        and setting up the Telegram client with the API credentials.
        """
        # Load configuration values from the config file
        self.api_id: int = config.telegram.get("api_id")  # API ID for Telegram
        self.api_hash: str = config.telegram.get("api_hash")  # API hash for Telegram
        self.session_name: str = config.telegram.get("session_name")  # Session name for the Telegram client
        
        # Initialize the TelegramClient with the session name, API ID, and API hash
        self.client: TelegramClient = TelegramClient(self.session_name, self.api_id, self.api_hash)
        
        # Add an event handler for new incoming messages
        self.client.add_event_handler(self.handler, events.NewMessage())

        # Start the client, which will begin processing events
        self.client.start()

    async def handler(self, event: NewMessage) -> None:
        """
        Handles new incoming messages. If the message is from a channel, 
        it will print the text of the message.

        Args:
            event (NewMessage): The event triggered by a new incoming message.
        """
        # Check if the message comes from a channel
        if event.is_channel:
            # Print the message text to the console
            print(event.message.text)
