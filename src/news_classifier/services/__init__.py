"""Text processing: cleaning, duplicate detection and classification."""

from news_classifier.services.classifier import TextClassifier
from news_classifier.services.preprocess import preprocess_text
from news_classifier.services.similarity import TextSimilarity, jaccard_similarity

__all__ = [
    "TextClassifier",
    "TextSimilarity",
    "jaccard_similarity",
    "preprocess_text",
]
