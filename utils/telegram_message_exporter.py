"""Export the posts of every channel an account follows into JSON files.

Standalone script: it shares the Telegram credentials with the bot through the
same `.env` variables, but nothing in the package imports it.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from loguru import logger
from telethon import TelegramClient
from telethon.tl.custom.dialog import Dialog
from telethon.tl.types import Message

OUTPUT_DIR = Path("data/raw")
MESSAGE_LIMIT = 3000
SESSION_NAME = "telegram_message_exporter"


async def fetch_channel_messages(
    client: TelegramClient, channel: Dialog
) -> list[dict[str, Any]]:
    """Read the most recent posts of one channel.

    Args:
        client: Authorized Telethon client.
        channel: Dialog to read from.

    Returns:
        list[dict[str, Any]]: One record per post that carries text.
    """
    logger.info(f"Fetching up to {MESSAGE_LIMIT} messages from {channel.name}.")
    messages = [
        {
            "message_id": message.id,
            "sender_id": message.sender_id,
            "text": message.text,
            "date": message.date.isoformat(),
            "channel": channel.name,
        }
        async for message in client.iter_messages(channel.id, limit=MESSAGE_LIMIT)
        if isinstance(message, Message) and message.text
    ]
    logger.info(f"Fetched {len(messages)} messages from {channel.name}.")
    return messages


def save_messages(messages: list[dict[str, Any]], channel_id: int) -> None:
    """Append the posts of one channel to its JSON file.

    Args:
        messages: Records returned by `fetch_channel_messages`.
        channel_id: Channel the records came from; names the file.
    """
    if not messages:
        logger.warning(f"Nothing to save for channel {channel_id}.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{abs(channel_id)}_messages.json"
    if path.exists():
        with path.open(encoding="utf-8") as file:
            messages.extend(json.load(file))

    with path.open("w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)
    logger.info(f"Saved {len(messages)} messages to {path}.")


async def export_all_channels(client: TelegramClient) -> None:
    """Export every channel the account follows.

    Args:
        client: Telethon client; started by this function.
    """
    await client.start()
    for dialog in await client.get_dialogs():
        if dialog.is_channel:
            save_messages(await fetch_channel_messages(client, dialog), dialog.id)


def main() -> None:
    """Run the export against the credentials in the environment."""
    client = TelegramClient(
        SESSION_NAME, int(os.environ["API_ID"]), os.environ["API_HASH"]
    )
    asyncio.run(export_all_channels(client))


if __name__ == "__main__":
    main()
