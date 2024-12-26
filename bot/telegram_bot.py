from typing import Dict

from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.functions.channels import (
    CreateChannelRequest, 
    CreateForumTopicRequest, 
    # DeleteTopicHistoryRequest, 
    # GetForumTopicsByIDRequest
)
from bot.loader import config, telegram_config


class TelegramBot:
    def __init__(self):
        """
        Initializes the TelegramBot instance by loading the configuration values
        and setting up the Telegram client with the API credentials.
        """
        # Load configuration values from the config file
        self.api_id = config.telegram.get("api_id")  # API ID for Telegram
        self.api_hash = config.telegram.get("api_hash")  # API hash for Telegram
        self.session_name = config.telegram.get("session_name")  # Session name for the Telegram client
        
        # Initialize the TelegramClient with the session name, API ID, and API hash
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

        # Add an event handler for new incoming messages
        self.client.add_event_handler(self.handler, NewMessage())

        # Start the client, which will begin processing events
        self.client.start()
        
        # Create forum and topics if needed
        self.client.loop.run_until_complete(self.setup_forum_and_topics())

    async def handler(self, event: NewMessage) -> None:
        """
        Handles new incoming messages. If the message is from a channel, 
        it will print the text of the message.

        :param event: The event triggered by a new incoming message.
        :returns: None
        """
        if event.is_channel:
            print(event.message.text)

    async def create_forum(self, forum_name: str, forum_about: str = "") -> int:
        """
        Creates a new forum channel on Telegram and returns the forum ID.

        :param forum_name: The name of the forum.
        :param forum_about: A description of the forum.
        :returns: The forum ID.
        """
        forum = await self.client(CreateChannelRequest(
            title=forum_name,
            about=forum_about,
            forum=True
        ))
        return forum.updates[1].channel_id

    async def create_topic(self, topic_name: str, category: int) -> None:
        """
        Creates a new topic within the forum.

        :param topic_name: The name of the topic.
        :param category: The category ID to which the topic belongs.
        :returns: None
        """
        topic = await self.client(CreateForumTopicRequest(
            channel=telegram_config.forum_id,
            title=topic_name
        ))
        telegram_config.add_topic(topic.updates[0].id, category)

    async def create_topics(self, topics: Dict[int, str]) -> None:
        """
        Creates topics for categories that are not excluded.

        :param topics: A dictionary with category IDs as keys and topic names as values.
        :returns: None
        """
        # Create topics for categories that are not excluded
        for category, topic_name in topics.items():
            if category not in config.exclude_categories:
                await self.create_topic(topic_name, category)

    async def create_new_topics(self, topics: Dict[int, str]) -> None:
        """
        Creates new topics for categories that do not have existing topics.

        :param topics: A dictionary with category IDs as keys and topic names as values.
        :returns: None
        """
        # Create new topics only for categories not present in the existing topics
        for category, topic_name in topics.items():
            if category not in config.exclude_categories and not any(category == data["category"] for data in telegram_config.topics):
                await self.create_topic(topic_name, category)   

    async def setup_forum_and_topics(self) -> None:
        """
        Ensures the forum and topics are created if not already present.

        :returns: None
        """
        # Create forum if it doesn't exist
        if telegram_config.forum_id is None:
            forum_id = await self.create_forum("News")
            telegram_config.add_forum_id(forum_id)

        # Create topics if they don't exist
        if not telegram_config.topics:
            await self.create_topics(config.categories)

        # Create new topics if they don't exist
        await self.create_new_topics(config.categories)

bot = TelegramBot()
