import logging
import asyncio
from typing import Dict, List
from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.functions.channels import (
    CreateChannelRequest, 
    CreateForumTopicRequest, 
    # DeleteTopicHistoryRequest, 
    # GetForumTopicsByIDRequest
)
from telethon.tl.functions.messages import ForwardMessagesRequest
from bot.loader import config, telegram_config, classifier, text_similarity
from bot.preprocess import preprocess_text


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

    async def _get_grouped_message_ids(self, chat_id: int, grouped_id: int, timeout: float = 1.0) -> List[int]:
        """
        Retrieves message IDs that belong to the same group within a specific timeout period.

        :param chat_id: The ID of the chat where messages are collected.
        :param grouped_id: The grouped ID to filter messages.
        :param timeout: Time in seconds to collect messages (default is 1.0).
        :returns: A list of message IDs belonging to the group.
        """
        ids = []
        end_time = asyncio.get_event_loop().time() + timeout

        async for message in self.client.iter_messages(chat_id):
            if message.grouped_id == grouped_id:
                ids.append(message.id)
            if asyncio.get_event_loop().time() > end_time:
                break

        return ids

    async def handler(self, event: NewMessage) -> None:
        """
        Handles new incoming messages.

        :param event: The event triggered by a new incoming message.
        :returns: None
        """
        if not event.is_channel:
            return

        # Preprocess the post text
        post_text = event.message.text
        clear_post_text = preprocess_text(post_text)

        # Extract lemmas for similarity check
        text_lemma = text_similarity.get_lemmas(clear_post_text)

        # TODO: Implement similarity check logic
        if False:  # Replace with actual similarity check
            return

        # Classify the message text into a category
        category = classifier.classify_text(clear_post_text)

        # Find the corresponding topic ID for the category
        topic_id = next((topic["id"] for topic in telegram_config.topics if topic["category"] == category), None)
        if not topic_id:
            return

        # Collect grouped messages if applicable
        message_ids = await self._get_grouped_message_ids(event.chat_id, event.message.grouped_id)

        # Forward messages to the forum under the specific topic
        await self.client(ForwardMessagesRequest(
            from_peer=event.chat_id,
            id=message_ids,
            to_peer=telegram_config.forum_id,
            top_msg_id=topic_id,
        ))

    async def create_forum(self, forum_name: str, forum_about: str = "") -> None:
        """
        Creates a new forum channel on Telegram.

        :param forum_name: The name of the forum.
        :param forum_about: A description of the forum (default is an empty string).
        :returns: None
        """
        forum = await self.client(CreateChannelRequest(
            title=forum_name,
            about=forum_about,
            forum=True
        ))

        # Extract forum ID and adjust if necessary
        forum_id = forum.updates[1].channel_id
        if forum_id > 0:
            forum_id = -100 * 10**10 - forum_id

        logging.info(f"Forum created with ID: {forum_id}")

        # Add the forum ID to the configuration
        telegram_config.add_forum_id(forum_id)

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

        topic_id = topic.updates[0].id
        logging.info(f"Topic created with ID: {topic_id}.")

        # Add the topic ID to the configuration under the appropriate category
        telegram_config.add_topic(topic_id, category)

    async def create_topics(self, topics: Dict[int, str]) -> None:
        """
        Creates topics for categories that are not excluded.

        :param topics: A dictionary with category IDs as keys and topic names as values.
        :returns: None
        """
        logging.info("Creating topics for non-excluded categories.")

        for category, topic_name in topics.items():
            if category not in config.exclude_categories:
                await self.create_topic(topic_name, category)

    async def create_new_topics(self, topics: Dict[int, str]) -> None:
        """
        Creates new topics for categories that do not have existing topics.

        :param topics: A dictionary with category IDs as keys and topic names as values.
        :returns: None
        """
        logging.info(f"Creating new topics for categories that do not have topics.")
        
        for category, topic_name in topics.items():
            if category not in config.exclude_categories and not any(category == data["category"] for data in telegram_config.topics):
                logging.info(f"Creating new topic '{topic_name}' for category {category}.")
                await self.create_topic(topic_name, category)   

    async def setup_forum_and_topics(self) -> None:
        """
        Ensures the forum and topics are created if they are not already present.

        :returns: None
        """
        logging.info(f"Checking if forum and topics need to be created.")

        # Create forum if it doesn't exist
        if telegram_config.forum_id is None:
            logging.info("Forum does not exist, creating now.")
            await self.create_forum("News")

        # Create topics if they don't exist
        if not telegram_config.topics:
            logging.info("Topics do not exist, creating now.")
            await self.create_topics(config.categories)

        # Create new topics if they don't exist
        logging.info("Ensuring new topics are created if needed.")
        await self.create_new_topics(config.categories)
