"""Settings of the bot, loaded from the environment or a .env file.

Everything a deployment has to change lives here: Telegram credentials, the
paths the bot reads and writes, and the logging setup. The category taxonomy and
the created topics stay in YAML, because they are structures rather than knobs.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Runtime configuration of the bot."""

    api_id: int = Field(description="Telegram API ID from https://my.telegram.org.")
    api_hash: str = Field(description="Telegram API hash from https://my.telegram.org.")
    session_name: str = Field(
        default="news_classifier",
        description="Name of the Telethon session file, without the extension.",
    )

    model_path: Path = Field(
        default=Path("model"),
        description="Directory holding the fine-tuned RuBERT model and tokenizer.",
    )
    db_path: Path = Field(
        default=Path("messages.db"),
        description="DuckDB file with the recently seen messages.",
    )
    taxonomy_path: Path = Field(
        default=Path("config/categories.yaml"),
        description="Category names and the exclusion lists.",
    )
    forum_state_path: Path = Field(
        default=Path("config/forum_state.yaml"),
        description="Forum and topic IDs the bot created; written by the bot.",
    )

    forum_title: str = Field(
        default="News",
        description="Title of the forum created on the first run.",
    )
    message_lifetime: int = Field(
        default=2,
        gt=0,
        description="Hours a message stays in the database as a duplicate candidate.",
    )
    similarity_threshold: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="Jaccard score above which two posts count as the same news.",
    )
    spacy_model: str = Field(
        default="ru_core_news_sm",
        description="spaCy pipeline used for lemmatization.",
    )

    disable_logging: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    log_path: Path | None = Field(
        default=None,
        description="File to mirror the logs into; stdout only when unset.",
    )
    log_format: str = (
        "<cyan>[{time:DD/MM/YY HH:mm:ss}]</cyan> "
        "<light-magenta>[{file}:{function}:{line}]</light-magenta> "
        "<lvl>[{level}]</lvl> - {message}"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Return the settings, reading the environment only on the first call.

    Returns:
        AppSettings: The cached settings instance.
    """
    return AppSettings()
