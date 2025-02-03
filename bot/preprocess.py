import re


def preprocess_text(text: str) -> str:
    """
    Preprocesses the input text and returns the cleaned text.

    :param text: The raw input text to preprocess.
    :returns: The preprocessed text as a lowercase string with special 
              characters and Markdown/HTML tags removed.
    """

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)
    
    # Remove bold Markdown syntax (e.g., **bold** or __bold__)
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
    
    # Remove italic Markdown syntax (e.g., *italic* or _italic_)
    text = re.sub(r"(\*|_)(.*?)\1", r"\2", text)
    
    # Remove strikethrough Markdown syntax (e.g., ~~strikethrough~~)
    text = re.sub(r"~~(.*?)~~", r"\1", text)
    
    # Remove inline code Markdown syntax (e.g., `code`)
    text = re.sub(r"`{1,2}(.*?)`{1,2}", r"\1", text)
    
    # Remove Markdown headings (e.g., # Heading)
    text = re.sub(r"#{1,6}\s*", "", text)
    
    # Remove Markdown links (e.g., [link](url))
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    
    # Remove Markdown images (e.g., ![alt text](image url))
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    
    # Remove blockquotes (e.g., > quoted text)
    text = re.sub(r">\s*", "", text)
    
    # Remove all non-alphabetical characters and digits
    text = re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s]", "", text)
    
    # Replace multiple spaces with a single space and strip leading/trailing spaces
    text = re.sub(r"\s+", " ", text).strip()
    
    # Convert all text to lowercase
    return text.lower()
