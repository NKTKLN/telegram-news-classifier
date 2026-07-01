"""Text processing: cleaning and duplicate detection."""

from news_classifier.services.preprocess import preprocess_text
from news_classifier.services.similarity import TextSimilarity, jaccard_similarity

__all__ = ["TextSimilarity", "jaccard_similarity", "preprocess_text"]
