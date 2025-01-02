import logging
import datetime
from typing import List, Set

import duckdb

# Setting up logging
logger = logging.getLogger(__name__)

class DuckDBHandler:
    def __init__(self, db_file: str = ':memory:'):
        """
        Initializes the DuckDB connection and creates the messages table.

        :param db_file: Path to the database file. Default database is in-memory.
        """
        self.db = duckdb.connect(db_file)
        self.create_table()
        logger.info(f"Database connected: {db_file}")

    def create_table(self):
        """Creates the 'messages' table if it does not exist."""
        self.db.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            message_id BIGINT,
            channel_id BIGINT,
            grouped_id BIGINT,
            text TEXT,
            lemma TEXT[],
            date TIMESTAMP
        );
        ''')
        logger.info("Table 'messages' is ready.")

    def insert_message(self, message_id: int, channel_id: int, grouped_id: int, 
                       text: str, lemma: List[str], date: datetime.datetime) -> None:
        """
        Inserts a new message into the 'messages' table.
        
        :param message_id: Unique identifier for the message.
        :param channel_id: Channel where the message was posted.
        :param grouped_id: Group identifier from messages
        :param text: Text content of the message.
        :param lemma: A set of lemmatized tokens.
        :param date: Timestamp when the message was published
        """
        self.db.execute('''
        INSERT INTO messages (message_id, channel_id, grouped_id, text, lemma, date)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (message_id, channel_id, grouped_id, text, lemma, date))
        logger.info(f"Inserted message {message_id} into database.")

    def cleanup_old_messages(self, time_frame: int = 1) -> None:
        """
        Removes messages older than the specified time frame (in hours).
        
        :param time_frame: The number of hours to retain messages. Default is 1 hour.
        """
        time_threshold = datetime.datetime.now() - datetime.timedelta(hours=time_frame)
        self.db.execute('''
        DELETE FROM messages WHERE date < ?
        ''', (time_threshold,))
        logger.info(f"Cleaned up messages older than {time_frame} hour(s).")

    def get_recent_messages_lemmas(self, time_frame: int = 1) -> List[Set[str]]:
        """
        Retrieves the lemmatized tokens from messages created within the last 
        time frame (in hours).
        
        :param time_frame: The number of hours to consider for message retrieval. Default is 1 hour.
        :returns: A list of sets of lemmatized tokens from the recent messages.
        """
        time_threshold = datetime.datetime.now() - datetime.timedelta(hours=time_frame)
        return [set(x[0]) for x in self.db.execute('''
        SELECT lemma FROM messages WHERE date >= ?
        ''', (time_threshold,)).fetchall()]
    
    def check_message_exists(self, message_id: int, channel_id: int, 
                             grouped_id: int) -> bool:
        """
        Checks whether a message with the given message_id, channel_id, 
        or grouped_id exists in the database.
        
        :param message_id: The unique ID of the message.
        :param channel_id: The ID of the channel where the message was posted.
        :param grouped_id: Group identifier from messages
        :return: True if the message exists, False otherwise.
        """
        result = self.db.execute('''
        SELECT COUNT(*) FROM messages WHERE channel_id = ? AND (message_id = ? OR grouped_id = ?)
        ''', (channel_id, message_id, grouped_id)).fetchone()
        return result[0] > 0 # True if message exists, False otherwise

    def close(self) -> None:
        """
        Closes the database connection.
        """
        logger.info("Closing the database connection.")
        self.db.close()
