"""Creation of the forum and of one topic per category."""

from loguru import logger
from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import CreateForumTopicRequest

from news_classifier.domain import Taxonomy
from news_classifier.storage import ForumStateStore

# Telegram exposes channels as positive IDs but addresses them with the -100
# prefix, so the ID returned by CreateChannelRequest has to be rewritten.
CHANNEL_ID_OFFSET = -100 * 10**10


class ForumManager:
    """Brings the forum and its topics in line with the taxonomy."""

    def __init__(
        self, client: TelegramClient, taxonomy: Taxonomy, store: ForumStateStore
    ) -> None:
        """Store the collaborators the setup runs against.

        Args:
            client: Authorized Telethon client.
            taxonomy: Categories the topics are created for.
            store: Forum state, updated as the forum and topics are created.
        """
        self.client = client
        self.taxonomy = taxonomy
        self.store = store

    async def create_forum(self, title: str, about: str = "") -> None:
        """Create the forum the bot forwards posts into.

        Args:
            title: Title of the forum.
            about: Description shown in the forum's profile.
        """
        forum = await self.client(
            CreateChannelRequest(title=title, about=about, forum=True)
        )
        forum_id = forum.updates[1].channel_id
        if forum_id > 0:
            forum_id = CHANNEL_ID_OFFSET - forum_id
        self.store.set_forum_id(forum_id)

    async def create_topic(self, name: str, category: int) -> None:
        """Create one topic and register it for a category.

        Args:
            name: Title of the topic.
            category: Category the topic collects.
        """
        topic = await self.client(
            CreateForumTopicRequest(peer=self.store.state.forum_id, title=name)
        )
        self.store.add_topic(topic.updates[0].id, category)

    async def setup(self, forum_title: str) -> None:
        """Create the forum if needed, then any topic that is still missing.

        Args:
            forum_title: Title used when the forum has to be created.
        """
        if self.store.state.forum_id is None:
            logger.info("No forum yet, creating one.")
            await self.create_forum(forum_title)

        for category, name in self.taxonomy.wanted_categories().items():
            if self.store.state.topic_id_for(category) is None:
                logger.info(f"Creating topic '{name}' for category {category}.")
                await self.create_topic(name, category)
