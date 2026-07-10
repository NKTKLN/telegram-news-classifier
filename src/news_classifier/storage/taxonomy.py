"""Reading the category taxonomy from YAML."""

from pathlib import Path

import yaml
from loguru import logger

from news_classifier.domain import Taxonomy


def load_taxonomy(path: Path) -> Taxonomy:
    """Load the category taxonomy from a YAML file.

    Args:
        path: Path to the taxonomy file.

    Returns:
        Taxonomy: The parsed taxonomy.

    Raises:
        FileNotFoundError: If path does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"Taxonomy file {path} does not exist.")

    with path.open(encoding="utf-8") as file:
        raw = yaml.safe_load(file) or {}

    taxonomy = Taxonomy.model_validate(raw)
    logger.info(f"Loaded {len(taxonomy.categories)} categories from {path}.")
    return taxonomy
