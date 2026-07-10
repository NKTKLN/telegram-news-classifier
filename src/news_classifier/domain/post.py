"""A channel post as it travels through the pipeline."""

from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    """A post reduced to what the duplicate filter and the store need."""

    message_id: int
    channel_id: int
    grouped_id: int | None
    text: str
    lemmas: set[str]
    date: datetime
