"""Cleaning of raw post text before it reaches the model."""

import re

# Ordered because the later patterns assume the markup is already gone: bold has
# to be stripped before italics, and links before the alphabet filter eats URLs.
_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"<.*?>"), ""),  # HTML tags
    (re.compile(r"!\[.*?\]\(.*?\)"), ""),  # images, before links
    (re.compile(r"\[(.*?)\]\(.*?\)"), r"\1"),  # links, keeping the label
    (re.compile(r"(\*\*|__)(.*?)\1"), r"\2"),  # bold
    (re.compile(r"(\*|_)(.*?)\1"), r"\2"),  # italics
    (re.compile(r"~~(.*?)~~"), r"\1"),  # strikethrough
    (re.compile(r"`{1,2}(.*?)`{1,2}"), r"\1"),  # inline code
    (re.compile(r"#{1,6}\s*"), ""),  # headings
    (re.compile(r">\s*"), ""),  # blockquotes
    (re.compile(r"[^a-zA-Zа-яА-ЯёЁ\s]"), ""),  # digits, punctuation, emoji
    (re.compile(r"\s+"), " "),  # collapsed whitespace
)


def preprocess_text(text: str) -> str:
    """Strip markup and non-letter characters, and lowercase the result.

    Args:
        text: Raw post text as Telegram delivered it.

    Returns:
        str: Lowercase text of Latin and Cyrillic words separated by spaces.
    """
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text.strip().lower()
