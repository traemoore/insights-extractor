import re
import string
from collections import Counter
from nltk.tokenize import word_tokenize
from ..nlp.stopwords import get_words

from settings import config

def calculate_keyword_frequencies(content, keywords={}, keyword_synonyms={} , regex_list=[], stop_words=[]):
    """
    Calculate the frequency of occurrence for each keyword in the given content.

    Args:
        content (str): The text content to analyze.
        keywords (dict): A dictionary containing the keywords to search for and their corresponding weights (default={}).
        keyword_synonyms (dict): A dictionary containing synonyms for each keyword (default={}).
        regex_list (list): A list of regular expressions to remove from the content (default=[]).
        stop_words (list): A list of stop words to remove from the content (default=[]).

    Returns:
        list: A list of tuples containing the keyword and its frequency of occurrence in the content, sorted by frequency in descending order.
    """
    try:
        keywords.update(config.keywords) 
        stop_words.extend(list(set(get_words(config.stop_words))))
        
        for regex in regex_list:
            content = re.sub(regex, '', content)

        # Remove punctuation
        content = content.translate(str.maketrans('', '', string.punctuation))

        # Tokenize the data column into words
        words = word_tokenize(content)
        words = [word for word in words if word.lower() not in stop_words]
        
        # Count the frequency of each word
        word_counts = Counter(words)

        # Apply classification keyword weights
        results = {}
        for word, freq in word_counts.items():
            if len(word) <= config.min_word_length:
                continue

            for keyword, synonyms in keyword_synonyms.items():
                if word in synonyms:
                    results[keyword] = freq * keywords[keyword]
                else:
                    results[word] = freq * keywords[word] if word in keywords else freq

        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        return sorted_results
    except Exception as e:
        print(f'Error processing: {e}')
        raise e