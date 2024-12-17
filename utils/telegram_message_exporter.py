import os
import json
import logging
from telethon.sync import TelegramClient
from telethon.tl.types import Message

# Replace with your API ID and API Hash
api_id = 'your_api_id'  # Replace with your actual API ID
api_hash = 'your_api_hash'  # Replace with your actual API Hash

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to the file for saving messages
OUTPUT_FILE = 'messages.json'

# Configurable message limit
LIMIT = 3000  # Default message limit (you can change this value)


async def get_last_messages_from_channels(client: TelegramClient) -> None:
    """
    Fetches the last 'limit' messages from all available Telegram channels
    and saves them into individual JSON files.

    Args:
        client (TelegramClient): The TelegramClient instance used to interact with Telegram.

    Returns:
        None
    """
    # Connect to the client
    await client.start()

    # Get all dialogs (channels, groups, private chats)
    dialogs = await client.get_dialogs()

    # Filter only channels
    channels = [dialog for dialog in dialogs if dialog.is_channel]

    # Iterate over all channels
    for channel in channels:
        logger.info(f"Fetching the last {LIMIT} messages from the channel: {channel.name}")

        # Get the last 'LIMIT' messages from the channel
        messages = []
        async for message in client.iter_messages(channel.id, limit=LIMIT):
            # If the message exists and is text, save it
            if isinstance(message, Message):
                messages.append({
                    'message_id': message.id,
                    'sender_id': message.sender_id,
                    'text': message.text,
                    'date': message.date.isoformat(),
                    'channel': channel.name
                })

        # Add the fetched messages to the overall list
        logger.info(f"Total messages fetched from the channel {channel.name}: {len(messages)}")

        # Save all messages to the JSON file
        if not messages:
            logger.warning("No messages to save.")
            continue

        # If the file exists, load it to append new messages
        if os.path.exists(f"{abs(channel.id)}_{OUTPUT_FILE}"):
            with open(f"{abs(channel.id)}_{OUTPUT_FILE}", 'r', encoding='utf-8') as f:
                existing_messages = json.load(f)
            messages.extend(existing_messages)

        # Write all messages to the file
        with open(f"{abs(channel.id)}_{OUTPUT_FILE}", 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)

        logger.info(f"All messages have been successfully saved to the file {abs(channel.id)}_{OUTPUT_FILE}")


def main() -> None:
    # Create and connect the client
    client = TelegramClient('telegram_message_exporter', api_id, api_hash)

    # Start the process of fetching messages
    client.loop.run_until_complete(get_last_messages_from_channels(client))


if __name__ == '__main__':
    main()
