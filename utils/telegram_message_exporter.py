import os
import json
import logging
from typing import List, Dict

from telethon.tl.types import Message
from telethon.sync import TelegramClient
from telethon.tl.custom.dialog import Dialog

# Replace with your API ID and API Hash
API_ID = 'your_api_id'  # Replace with your actual API ID
API_HASH = 'your_api_hash'  # Replace with your actual API Hash

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
OUTPUT_FILE_TEMPLATE = "{}_messages.json"
MESSAGE_LIMIT = 3000  # Default message limit


async def fetch_channel_messages(client: TelegramClient, channel: Dialog) -> List[Dict]:
    """
    Fetch messages from a specific Telegram channel.

    :param client: Instance of the Telegram client.
    :param channel: The channel from which to fetch messages.
    :returns: A list of dictionaries containing message details.
    """
    logger.info(f"Fetching the last {MESSAGE_LIMIT} messages from channel: {channel.name}")
    messages = []

    async for message in client.iter_messages(channel.id, limit=MESSAGE_LIMIT):
        if isinstance(message, Message) and message.text:
            messages.append({
                'message_id': message.id,
                'sender_id': message.sender_id,
                'text': message.text,
                'date': message.date.isoformat(),
                'channel': channel.name
            })

    logger.info(f"Fetched {len(messages)} messages from channel: {channel.name}")
    return messages


def save_messages_to_file(messages: List[Dict], channel_id: int) -> None:
    """
    Save messages to a JSON file.

    :param messages: List of message dictionaries to save.
    :param channel_id: ID of the channel (used for file naming).
    """
    if not messages:
        logger.warning("No messages to save.")
        return

    file_path = OUTPUT_FILE_TEMPLATE.format(abs(channel_id))

    # Load existing messages if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_messages = json.load(file)
        messages.extend(existing_messages)

    # Save all messages to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)

    logger.info(f"Messages saved to {file_path}")


async def process_channels(client: TelegramClient) -> None:
    """
    Process all channels the user has access to and fetch messages.

    :param client: Instance of the Telegram client.
    """
    await client.start()
    channels = [dialog for dialog in await client.get_dialogs() if dialog.is_channel]

    for channel in channels:
        logger.info(f"Processing channel: {channel.name}")
        messages = await fetch_channel_messages(client, channel)
        save_messages_to_file(messages, channel.id)


def main() -> None:
    client = TelegramClient('telegram_message_exporter', API_ID, API_HASH)
    client.loop.run_until_complete(process_channels(client))


if __name__ == '__main__':
    main()
