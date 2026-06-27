"""State of the forum the bot forwards posts into."""

from pydantic import BaseModel, Field


class Topic(BaseModel):
    """A forum topic created for one category."""

    id: int
    category: int


class ForumState(BaseModel):
    """Forum and topic IDs the bot created, persisted between runs."""

    forum_id: int | None = None
    topics: list[Topic] = Field(default_factory=list)

    def topic_id_for(self, category: int) -> int | None:
        """Return the topic a category is forwarded to.

        Args:
            category: Category index predicted by the classifier.

        Returns:
            int | None: The topic ID, or None when no topic exists yet.
        """
        return next(
            (topic.id for topic in self.topics if topic.category == category), None
        )
