"""Data structures shared by the storage, service and Telegram layers."""

from news_classifier.domain.forum import ForumState, Topic
from news_classifier.domain.post import Post
from news_classifier.domain.taxonomy import Taxonomy

__all__ = ["ForumState", "Post", "Taxonomy", "Topic"]
