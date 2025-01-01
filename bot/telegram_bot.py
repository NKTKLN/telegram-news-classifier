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
from bot.loader import config, telegram_config, classifier, text_similarity, db_handler
from bot.preprocess import preprocess_text

# Setting up logging
logger = logging.getLogger(__name__)

class TelegramManager:
    def __init__(self):
        """
        Initializes the TelegramManager instance by loading the configuration values
        and setting up the Telegram client with the API credentials.
        """
        # Load configuration values from the config file
        self.api_id = config.telegram.get("api_id")  # API ID for Telegram
        self.api_hash = config.telegram.get("api_hash")  # API hash for Telegram
        self.session_name = config.telegram.get("session_name")  # Session name for the Telegram client

        # Initialize the TelegramClient with the session name, API ID, and API hash
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

        # Initialize event handler and forum setup
        self.message_handler = MessageHandler(self.client)
        self.forum_setup = ForumSetup(self.client)

        # Start the client, which will begin processing events
        self.client.start()

        # Create forum and topics if needed
        asyncio.get_event_loop().run_until_complete(self.forum_setup.setup_forum_and_topics())
        
        # Keep the client running until it is disconnected
        self.client.run_until_disconnected()

class MessageHandler:
    def __init__(self, client: TelegramClient):
        """
        Initialize the handler with the Telegram client and set up event handler for new messages.
        
        :param client: The Telegram client instance.
        """
        self.client = client
        self.client.add_event_handler(self.handler, NewMessage())

    async def _get_grouped_message_ids(self, chat_id: int, grouped_id: int, timeout: float = 1.0, limit: int = 100) -> List[int]:
        """
        Retrieves message IDs that belong to the same group within a specific timeout period.
        
        :param chat_id: The ID of the chat where messages are collected.
        :param grouped_id: The grouped ID to filter messages.
        :param timeout: Time in seconds to collect messages (default is 1.0).
        :param limit: The maximum number of messages to retrieve (default is 100).
        :returns: A list of message IDs belonging to the group.
        """
        ids = []
        end_time = asyncio.get_event_loop().time() + timeout
        async for message in self.client.iter_messages(chat_id, limit=limit):  # The limit is applied here
            if message.grouped_id == grouped_id:
                ids.append(message.id)
            if asyncio.get_event_loop().time() > end_time:
                break
        logger.info(f"Collected {len(ids)} messages with grouped ID {grouped_id}.")
        return ids

    async def handler(self, event: NewMessage) -> None:
        """
        Handles new incoming messages by processing, checking for similarity, and forwarding them.
        
        :param event: The event triggered by a new incoming message.
        :returns: None
        """
        # Skip messages that do not belong to a channel, messages from excluded channels or empty messages
        if not event.is_channel or event.chat_id in config.exclude_channels or event.message.text == "":
            return

        # Check if the message has already been processed
        if db_handler.check_message_exists(event.message.id, event.chat_id, event.message.grouped_id):
            logger.info(f"Message {event.message.id} already processed. Skipping.")
            return

        # Preprocess the post text and extract lemmas for similarity check
        post_text = event.message.text
        clear_post_text = preprocess_text(post_text)
        text_lemma = text_similarity.get_lemmas(clear_post_text)
        
        # Get recent lemmas from the database and check for similarity
        lemma_list = db_handler.get_recent_messages_lemmas()
        if text_similarity.is_similar_to_last_messages(text_lemma, lemma_list):
            logger.info(f"Text is similar to recent messages. Skipping message {event.message.id}.")
            return
        
        # Insert the message into the database
        db_handler.insert_message(event.message.id, event.chat_id, event.message.grouped_id, clear_post_text, list(text_lemma), event.date)

        # Classify the message into a category
        category = classifier.classify_text(clear_post_text)
        if category in config.exclude_categories:
            logger.info(f"Message belongs to excluded category {category}. Skipping.")
            return

        # Find the topic ID for the category
        topic_id = next((topic["id"] for topic in telegram_config.topics if topic["category"] == category), None)
        if not topic_id:
            logger.warning(f"No topic found for category {category}. Skipping forwarding.")
            return

        # Collect grouped messages if applicable
        message_ids = await self._get_grouped_message_ids(event.chat_id, event.message.grouped_id)

        # Forward messages to the forum under the specific topic
        await self.client(ForwardMessagesRequest(
            from_peer=event.chat_id,
            id=message_ids or [event.message.id],
            to_peer=telegram_config.forum_id,
            top_msg_id=topic_id,
        ))

        logger.info(f"Successfully forwarded message {event.message.id} to the forum under topic {topic_id}.")

class ForumSetup:
    def __init__(self, client: TelegramClient):
        self.client = client

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
        logger.info(f"Forum created with ID: {forum_id}")
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
        logger.info(f"Topic created with ID: {topic_id}.")
        # Add the topic ID to the configuration under the appropriate category
        telegram_config.add_topic(topic_id, category)

    async def create_topics(self, topics: Dict[int, str]) -> None:
        """
        Creates topics for categories that are not excluded.

        :param topics: A dictionary with category IDs as keys and topic names as values.
        :returns: None
        """
        logger.info("Creating topics for non-excluded categories.")
        for category, topic_name in topics.items():
            if category not in config.exclude_categories:
                await self.create_topic(topic_name, category)

    async def create_new_topics(self, topics: Dict[int, str]) -> None:
        """
        Creates new topics for categories that do not have existing topics.

        :param topics: A dictionary with category IDs as keys and topic names as values.
        :returns: None
        """
        logger.info("Creating new topics for categories that do not have topics.")
        for category, topic_name in topics.items():
            if category not in config.exclude_categories and not any(category == data["category"] for data in telegram_config.topics):
                logger.info(f"Creating new topic '{topic_name}' for category {category}.")
                await self.create_topic(topic_name, category)

    async def setup_forum_and_topics(self) -> None:
        """
        Ensures the forum and topics are created if they are not already present.

        :returns: None
        """
        logger.info("Checking if forum and topics need to be created.")
        # Create forum if it doesn't exist
        if telegram_config.forum_id is None:
            logger.info("Forum does not exist, creating now.")
            await self.create_forum("News")

        # Create topics if they don't exist
        if not telegram_config.topics:
            logger.info("Topics do not exist, creating now.")
            await self.create_topics(config.categories)

        # Create new topics if they don't exist
        logger.info("Ensuring new topics are created if needed.")
        await self.create_new_topics(config.categories)
