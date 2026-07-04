"""Category prediction with the fine-tuned RuBERT model."""

from pathlib import Path

import torch
from loguru import logger
from transformers import AutoTokenizer, BertForSequenceClassification

# The model was fine-tuned on 128-token sequences, so inference has to match.
MAX_LENGTH = 128


class TextClassifier:
    """Assigns a category index to a post."""

    def __init__(self, model_path: Path) -> None:
        """Load the model and the tokenizer onto the best available device.

        Args:
            model_path: Directory holding the saved model and tokenizer.

        Raises:
            FileNotFoundError: If model_path does not exist.
        """
        if not model_path.exists():
            raise FileNotFoundError(f"Model path {model_path} does not exist.")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        # transformers ships py.typed but leaves this factory unannotated.
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)  # type: ignore[no-untyped-call]
        self.model.to(self.device)
        self.model.eval()
        logger.info(f"Classifier loaded from {model_path} on {self.device}.")

    def classify(self, text: str) -> int:
        """Predict the category of a post.

        Args:
            text: Preprocessed post text.

        Returns:
            int: Index of the highest scoring category.
        """
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=MAX_LENGTH,
        ).to(self.device)

        with torch.no_grad():
            logits = self.model(**inputs).logits

        return int(torch.argmax(logits, dim=1).item())
