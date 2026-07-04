"""Wiring of the bot: client, storage, models and the cleanup schedule."""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from telethon import TelegramClient
from telethon.events import NewMessage

from news_classifier.services import TextClassifier, TextSimilarity
from news_classifier.settings import get_settings
from news_classifier.storage import ForumStateStore, MessageStore, load_taxonomy
from news_classifier.telegram.forum import ForumManager
from news_classifier.telegram.handler import MessageHandler


async def run_bot(login_only: bool = False) -> None:
    """Start the bot and run it until Telegram disconnects.

    Args:
        login_only: Authorize the session and return, leaving the session file
            behind for later runs; used for the interactive first login.
    """
    settings = get_settings()
    client = TelegramClient(settings.session_name, settings.api_id, settings.api_hash)
    await client.start()

    if login_only:
        logger.info("Session authorized, stopping because --login was given.")
        await client.disconnect()
        return

    taxonomy = load_taxonomy(settings.taxonomy_path)
    store = ForumStateStore(settings.forum_state_path)
    messages = MessageStore(settings.db_path, settings.message_lifetime)

    await ForumManager(client, taxonomy, store).setup(settings.forum_title)

    handler = MessageHandler(
        client,
        taxonomy,
        store,
        messages,
        TextClassifier(settings.model_path),
        TextSimilarity(settings.spacy_model, settings.similarity_threshold),
    )
    client.add_event_handler(handler.on_new_message, NewMessage())

    # Messages outlive their duplicate window only as dead weight, so they are
    # dropped on the same period they are kept for.
    scheduler = AsyncIOScheduler()
    scheduler.add_job(messages.cleanup, "interval", hours=settings.message_lifetime)
    scheduler.start()

    logger.info("Bot started, waiting for posts.")
    try:
        await client.run_until_disconnected()
    finally:
        scheduler.shutdown()
        messages.close()
        await client.disconnect()
        logger.info("Bot stopped.")
