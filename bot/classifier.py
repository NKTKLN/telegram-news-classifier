import os
import torch
from typing import Tuple
from transformers import BertForSequenceClassification, AutoTokenizer
from bot.preprocess import preprocess_text

class TextClassifier:
    def __init__(self, model_path: str):
        """
        Initializes the class by loading the model and tokenizer.

        Args:
            model_path (str): Path to the directory containing the saved model and tokenizer.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.tokenizer = self.load_model(model_path)

    def load_model(self, model_path: str) -> Tuple[BertForSequenceClassification, AutoTokenizer]:
        """
        Loads the saved model and tokenizer from the specified path.

        Args:
            model_path (str): Path to the directory containing the saved model and tokenizer.

        Returns:
            Tuple[BertForSequenceClassification, AutoTokenizer]: The model and tokenizer loaded from the specified path.

        Raises:
            FileNotFoundError: If the model path does not exist.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path {model_path} does not exist.")
        
        model = BertForSequenceClassification.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model.to(self.device)
        model.eval()
        return model, tokenizer

    def classify_text(self, text: str) -> int:
        """
        Classifies the text using the model.

        Args:
            text (str): The input text to classify.

        Returns:
            int: The predicted class index.
        """
        preprocessed_text = preprocess_text(text)
        inputs = self.tokenizer(preprocessed_text, return_tensors="pt", padding="max_length", 
                               truncation=True, max_length=128).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            return torch.argmax(logits, dim=1).item()
