"""Handling of incoming channel posts."""

import asyncio

from loguru import logger
from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.functions.messages import ForwardMessagesRequest

from news_classifier.domain import Post, Taxonomy
from news_classifier.services import TextClassifier, TextSimilarity, preprocess_text
from news_classifier.storage import ForumStateStore, MessageStore

# An album arrives as several updates, so the first one waits briefly for the
# rest instead of forwarding a single photo out of a set.
ALBUM_COLLECT_TIMEOUT = 1.0
ALBUM_SCAN_LIMIT = 100


class MessageHandler:
    """Classifies new posts and forwards them into the matching topic."""

    def __init__(
        self,
        client: TelegramClient,
        taxonomy: Taxonomy,
        store: ForumStateStore,
        messages: MessageStore,
        classifier: TextClassifier,
        similarity: TextSimilarity,
    ) -> None:
        """Store the collaborators each post is processed with.

        Args:
            client: Authorized Telethon client.
            taxonomy: Categories and the exclusion lists.
            store: Forum state holding the target forum and its topics.
            messages: Store of recently handled posts.
            classifier: Model assigning a category to a post.
            similarity: Duplicate detector over lemmatized text.
        """
        self.client = client
        self.taxonomy = taxonomy
        self.store = store
        self.messages = messages
        self.classifier = classifier
        self.similarity = similarity

    async def _album_message_ids(self, chat_id: int, grouped_id: int) -> list[int]:
        """Collect the IDs of the posts belonging to one album.

        Args:
            chat_id: Channel the album was posted in.
            grouped_id: Album the posts share.

        Returns:
            list[int]: IDs of the album's posts, newest first.
        """
        ids: list[int] = []
        deadline = asyncio.get_running_loop().time() + ALBUM_COLLECT_TIMEOUT
        async for message in self.client.iter_messages(chat_id, limit=ALBUM_SCAN_LIMIT):
            if message.grouped_id == grouped_id:
                ids.append(message.id)
            if asyncio.get_running_loop().time() > deadline:
                break

        logger.info(f"Collected {len(ids)} messages of album {grouped_id}.")
        return ids

    async def on_new_message(self, event: NewMessage.Event) -> None:
        """Process one incoming post.

        Args:
            event: Update carrying the new post.
        """
        message = event.message
        if (
            not event.is_channel
            or event.chat_id in self.taxonomy.exclude_channels
            or not message.text
        ):
            return

        if self.messages.exists(message.id, event.chat_id, message.grouped_id):
            logger.info(f"Message {message.id} already handled, skipping.")
            return

        text = preprocess_text(message.text)
        lemmas = self.similarity.lemmas(text)
        if self.similarity.is_duplicate(lemmas, self.messages.recent_lemmas()):
            logger.info(f"Message {message.id} repeats a recent post, skipping.")
            return

        self.messages.add(
            Post(
                message_id=message.id,
                channel_id=event.chat_id,
                grouped_id=message.grouped_id,
                text=text,
                lemmas=lemmas,
                date=message.date,
            )
        )

        category = self.classifier.classify(text)
        if category in self.taxonomy.exclude_categories:
            logger.info(f"Message {message.id} is category {category}, skipping.")
            return

        topic_id = self.store.state.topic_id_for(category)
        if topic_id is None:
            logger.warning(f"No topic for category {category}, not forwarding.")
            return

        message_ids = [message.id]
        if message.grouped_id is not None:
            message_ids = (
                await self._album_message_ids(event.chat_id, message.grouped_id)
                or message_ids
            )

        await self.client(
            ForwardMessagesRequest(
                from_peer=event.chat_id,
                id=message_ids,
                to_peer=self.store.state.forum_id,
                top_msg_id=topic_id,
            )
        )
        logger.info(f"Forwarded message {message.id} to topic {topic_id}.")
