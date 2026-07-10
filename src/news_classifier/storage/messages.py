"""DuckDB store of the posts the bot has already handled."""

from datetime import UTC, datetime, timedelta
from pathlib import Path

import duckdb
from loguru import logger

from news_classifier.domain import Post

SCHEMA = """
create table if not exists messages (
    message_id bigint,
    channel_id bigint,
    grouped_id bigint,
    text text,
    lemmas text[],
    date timestamptz
);
"""


class MessageStore:
    """Short-term memory of seen posts, used to drop duplicates."""

    def __init__(self, db_path: Path, retention_hours: int) -> None:
        """Connect to DuckDB and create the schema.

        Args:
            db_path: Database file; `:memory:` keeps everything in RAM.
            retention_hours: How long a post stays a duplicate candidate.
        """
        self.retention_hours = retention_hours
        self.db = duckdb.connect(str(db_path))
        self.db.execute(SCHEMA)
        logger.info(f"Message store ready at {db_path}.")

    def _cutoff(self) -> datetime:
        """Return the oldest timestamp still considered recent.

        Returns:
            datetime: Now minus the retention window, in UTC.
        """
        return datetime.now(tz=UTC) - timedelta(hours=self.retention_hours)

    def add(self, post: Post) -> None:
        """Store a post.

        Args:
            post: Post to remember; its lemmas are stored sorted, because
                DuckDB has lists rather than sets.
        """
        self.db.execute(
            """
            insert into messages
                (message_id, channel_id, grouped_id, text, lemmas, date)
            values (?, ?, ?, ?, ?, ?)
            """,
            (
                post.message_id,
                post.channel_id,
                post.grouped_id,
                post.text,
                sorted(post.lemmas),
                post.date,
            ),
        )
        logger.debug(f"Stored message {post.message_id} from {post.channel_id}.")

    def exists(self, message_id: int, channel_id: int, grouped_id: int | None) -> bool:
        """Check whether a post, or its album, has been handled already.

        Args:
            message_id: ID of the post inside its channel.
            channel_id: Channel the post came from.
            grouped_id: Album the post belongs to, if any.

        Returns:
            bool: True if the post is already stored.
        """
        result = self.db.execute(
            """
            select count(*) from messages
            where channel_id = ? and (message_id = ? or grouped_id = ?)
            """,
            (channel_id, message_id, grouped_id),
        ).fetchone()
        return bool(result and result[0] > 0)

    def recent_lemmas(self) -> list[set[str]]:
        """Return the lemma sets of the posts inside the retention window.

        Returns:
            list[set[str]]: One set per recent post.
        """
        rows = self.db.execute(
            "select lemmas from messages where date >= ?", (self._cutoff(),)
        ).fetchall()
        return [set(row[0]) for row in rows]

    def cleanup(self) -> None:
        """Delete the posts that fell out of the retention window."""
        self.db.execute("delete from messages where date < ?", (self._cutoff(),))
        logger.info(f"Removed messages older than {self.retention_hours}h.")

    def close(self) -> None:
        """Close the database connection."""
        self.db.close()
        logger.info("Message store closed.")
