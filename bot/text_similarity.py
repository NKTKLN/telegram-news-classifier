import spacy

class TextSimilarity:
    def __init__(self, language_model='ru_core_news_sm'):
        """
        Initializes the TextSimilarity class with the specified language model.
        
        :param language_model: The language model to be used by spaCy. Default is 'ru_core_news_sm'.
        """
        # Load the spaсy language model for NLP tasks
        self.nlp = spacy.load(language_model)

    def get_lemmas(self, text: str) -> set:
        """
        Extracts the set of lemmatized tokens from a given text, excluding 
        stop words and punctuation.

        :param text: The input text for lemma extraction.
        :returns: A set of lemmatized tokens.
        """
        # Process the text and extract lemmas (excluding stop words and punctuation)
        doc = self.nlp(text)
        return {token.lemma_ for token in doc if not token.is_stop and not token.is_punct}

    def calculate_similarity(self, first_lemmas: set, second_lemmas: set, 
                             threshold: float = 0.1) -> bool:
        """
        Calculates the Jaccard similarity between two sets of lemmas and checks 
        if it exceeds the threshold.

        :param first_lemmas: The set of lemmatized tokens from the first text.
        :param second_lemmas: The set of lemmatized tokens from the second text.
        :param threshold: The minimum similarity threshold (default is 0.1).
        :returns: True if the similarity is greater than the threshold, otherwise False.
        """
        # Calculate Jaccard similarity: |A ∩ B| / |A ∪ B|
        if not first_lemmas or not second_lemmas:  # Avoid division by zero if either set is empty
            return False

        similarity = len(first_lemmas & second_lemmas) / len(first_lemmas | second_lemmas)
        return similarity > threshold

    def is_similar_to_last_messages(self, current_lemma_set: set, 
                                    previous_lemmas_list: list) -> bool:
        """
        Checks if the provided lemma set has a similarity greater than the 
        threshold with any of the previous messages' lemmas.

        :param current_lemma_set: The set of lemmatized tokens from the current text.
        :param previous_lemmas_list: A list of lemmatized sets from previous messages.
        :returns: True if the current lemma set is similar to any of the previous 
                  message lemmas, otherwise False.
        """
        # Iterate over each set of lemmas from the previous messages
        for stored_lemma_set in previous_lemmas_list:
            # Check if the similarity exceeds the threshold for any of the previous messages
            if self.calculate_similarity(current_lemma_set, stored_lemma_set):
                return True
        return False
