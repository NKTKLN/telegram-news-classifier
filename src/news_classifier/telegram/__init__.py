"""Telegram side of the bot: the client, the forum and the message handler."""

from news_classifier.telegram.bot import run_bot
from news_classifier.telegram.forum import ForumManager
from news_classifier.telegram.handler import MessageHandler

__all__ = ["ForumManager", "MessageHandler", "run_bot"]
