"""Reading and writing the forum state the bot builds up as it runs."""

from pathlib import Path

import yaml
from loguru import logger

from news_classifier.domain import ForumState, Topic


class ForumStateStore:
    """Keeps the forum state in memory and mirrors every change to YAML."""

    def __init__(self, path: Path) -> None:
        """Load the state, starting from an empty one when the file is missing.

        Args:
            path: YAML file the state is stored in; created on the first write.
        """
        self.path = path
        self.state = self._load()

    def _load(self) -> ForumState:
        """Read the state file.

        Returns:
            ForumState: The stored state, or an empty one if there is no file.
        """
        if not self.path.exists():
            logger.info(f"No forum state at {self.path}, starting from scratch.")
            return ForumState()

        with self.path.open(encoding="utf-8") as file:
            raw = yaml.safe_load(file) or {}

        state = ForumState.model_validate(raw)
        logger.info(f"Loaded forum state with {len(state.topics)} topics.")
        return state

    def save(self) -> None:
        """Write the current state back to disk."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(
                self.state.model_dump(),
                file,
                default_flow_style=False,
                allow_unicode=True,
            )
        logger.info(f"Forum state saved to {self.path}.")

    def set_forum_id(self, forum_id: int) -> None:
        """Remember the forum the bot forwards posts into.

        Args:
            forum_id: ID of the created forum.
        """
        self.state.forum_id = forum_id
        self.save()
        logger.info(f"Forum ID set to {forum_id}.")

    def add_topic(self, topic_id: int, category: int) -> None:
        """Remember a topic, ignoring a category that already has one.

        Args:
            topic_id: ID of the created topic.
            category: Category the topic collects.
        """
        if self.state.topic_id_for(category) is not None:
            logger.warning(f"Category {category} already has a topic, skipping.")
            return

        self.state.topics.append(Topic(id=topic_id, category=category))
        self.save()
        logger.info(f"Topic {topic_id} registered for category {category}.")
