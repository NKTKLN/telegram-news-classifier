"""Entry point of the bot."""

import argparse
import asyncio

from news_classifier.telegram import run_bot
from news_classifier.utils import setup_logger


def parse_args() -> argparse.Namespace:
    """Parse the command line.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Telegram news classifier bot.")
    parser.add_argument(
        "--login",
        action="store_true",
        help="authorize the Telegram session and exit",
    )
    return parser.parse_args()


def main() -> None:
    """Set up logging and run the bot."""
    args = parse_args()
    setup_logger()
    asyncio.run(run_bot(login_only=args.login))


if __name__ == "__main__":
    main()
