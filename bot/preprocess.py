import re


def preprocess_text(text: str) -> str:
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
