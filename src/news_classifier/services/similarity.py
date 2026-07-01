"""Duplicate detection over lemmatized post text."""

from collections.abc import Iterable

import spacy
from loguru import logger


def jaccard_similarity(first: set[str], second: set[str]) -> float:
    """Return the Jaccard similarity of two lemma sets.

    Args:
        first: Lemmas of one post.
        second: Lemmas of the other post.

    Returns:
        float: Size of the intersection over size of the union; 0.0 if either
            set is empty.
    """
    if not first or not second:
        return 0.0
    return len(first & second) / len(first | second)


class TextSimilarity:
    """Lemmatizes posts and compares them against the recent ones."""

    def __init__(
        self, language_model: str = "ru_core_news_sm", threshold: float = 0.1
    ) -> None:
        """Load the spaCy pipeline.

        Args:
            language_model: Installed spaCy pipeline used for lemmatization.
            threshold: Jaccard score above which two posts are the same news.
        """
        self.threshold = threshold
        self.nlp = spacy.load(language_model)
        logger.info(f"Loaded spaCy pipeline {language_model}.")

    def lemmas(self, text: str) -> set[str]:
        """Lemmatize a post, dropping stop words and punctuation.

        Args:
            text: Preprocessed post text.

        Returns:
            set[str]: The lemmas carrying the meaning of the post.
        """
        return {
            token.lemma_
            for token in self.nlp(text)
            if not token.is_stop and not token.is_punct
        }

    def is_duplicate(self, lemmas: set[str], seen: Iterable[set[str]]) -> bool:
        """Check a post against the posts stored in the retention window.

        Args:
            lemmas: Lemmas of the post being handled.
            seen: Lemma sets of the recent posts.

        Returns:
            bool: True if any recent post is similar past the threshold.
        """
        return any(
            jaccard_similarity(lemmas, stored) > self.threshold for stored in seen
        )
