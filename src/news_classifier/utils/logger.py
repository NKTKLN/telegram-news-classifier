"""Loguru setup driven by the application settings."""

import sys

from loguru import logger

from news_classifier.settings import get_settings


def setup_logger() -> None:
    """Configure Loguru from the settings, replacing the default sink."""
    logger.remove()

    settings = get_settings()
    if settings.disable_logging:
        return

    logger.add(
        sys.stdout,
        format=settings.log_format,
        level=settings.log_level,
        colorize=True,
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    if settings.log_path is not None:
        logger.add(
            settings.log_path,
            format=settings.log_format,
            level=settings.log_level,
            colorize=False,
            enqueue=True,
            backtrace=True,
            diagnose=True,
            rotation="10 MB",
            retention="10 days",
            compression="zip",
        )

    logger.info(f"Logging initialized at level {settings.log_level}.")
