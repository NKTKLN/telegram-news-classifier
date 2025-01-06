import logging

import torch
from transformers import BertForSequenceClassification, AutoTokenizer

# Setting up logging
logger = logging.getLogger(__name__)

class TextClassifier:
    def __init__(self, model_path: str):
        """
        Initialize the TextClassifier by loading the model and tokenizer.

        :param model_path: Path to the stored model and tokenizer.
        """
        # Determine if a GPU is available, otherwise use CPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Load the model and tokenizer
        self._load_model(model_path)

    def _load_model(self, model_path: str) -> None:
        """
        Loads the saved model and tokenizer from the specified path.

        :param model_path: Path to the stored model and tokenizer.
        :returns: A tuple containing the loaded model and tokenizer.
        """
        # Load the pre-trained model and tokenizer
        logger.info(f"Loading model and tokenizer from {model_path}")
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Move the model to the appropriate device (GPU or CPU)
        self.model.to(self.device)
        self.model.eval()  # Set the model to evaluation mode
        logger.info("Model and tokenizer successfully loaded.")

    def classify_text(self, text: str) -> int:
        """
        Classifies the input text and returns the predicted class index.

        :param text: The input text to classify.
        :returns: The predicted class index as an integer.
        """
        # Tokenize the preprocessed text and prepare it for the model
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=128
        ).to(self.device)

        # Perform inference without calculating gradients
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits  # Extract logits from the model's output

            # Get the index of the class with the highest score
            predicted_class = torch.argmax(logits, dim=1).item()

        return predicted_class
