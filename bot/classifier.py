import os
import re
import torch
from typing import Tuple
from transformers import BertForSequenceClassification, AutoTokenizer

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

    def preprocess_text(self, text: str) -> str:
        """
        Preprocesses the text:
        - removes HTML tags
        - removes Markdown syntax
        - removes special characters and extra spaces
        - converts the text to lowercase

        Args:
            text (str): The raw input text to preprocess.

        Returns:
            str: The preprocessed text.
        """
        text = re.sub(r"<.*?>", "", text)
        text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)   # bold text
        text = re.sub(r"(\*|_)(.*?)\1", r"\2", text)      # italic text
        text = re.sub(r"~~(.*?)~~", r"\1", text)          # strikethrough text
        text = re.sub(r"`{1,2}(.*?)`{1,2}", r"\1", text)  # inline code
        text = re.sub(r"#{1,6}\s*", "", text)             # headings
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)   # links
        text = re.sub(r"!\[.*?\]\(.*?\)", "", text)       # images
        text = re.sub(r">\s*", "", text)                  # blockquotes
        text = re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s]", "", text)   # remove special characters and digits
        text = re.sub(r"\s+", " ", text).strip()          # remove extra spaces
        return text.lower()

    def classify_text(self, text: str) -> int:
        """
        Classifies the text using the model.

        Args:
            text (str): The input text to classify.

        Returns:
            int: The predicted class index.
        """
        preprocessed_text = self.preprocess_text(text)
        inputs = self.tokenizer(preprocessed_text, return_tensors="pt", padding="max_length", 
                               truncation=True, max_length=128).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            return torch.argmax(logits, dim=1).item()

    @staticmethod
    def postprocess_output(output: int) -> str:
        """
        Converts the predicted class index to a label.

        Args:
            output (int): The predicted class index.

        Returns:
            str: The predicted class label.
        """
        unique_labels = ['business', 'it', 'personal', 'other', 'weather', 'gaming', 'finances', 'stuff', 'political', 'advertisement', 'science', 'moscow']
        return unique_labels[output] if 0 <= output < len(unique_labels) else None
