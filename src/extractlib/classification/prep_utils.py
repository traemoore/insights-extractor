import re
import string
from collections import Counter
from nltk.tokenize import word_tokenize
import spacy

from ..nlp.pre_process import clean_text
from ..nlp.stopwords import get_words
from ..utils.json_utils import extract_text_elements, cleanse_and_tag_json_structure

from ..settings import config

def calculate_keyword_frequencies(content, keywords={}, keyword_synonyms={} , regex_list=[], use_default_stop_words=True, stop_words=[]):
    """
    Calculate the frequency of occurrence for each keyword in the given content.

    Args:
        content (str): The text content to analyze.
        keywords (dict): A dictionary containing the keywords to search for and their corresponding weights (default={}).
        keyword_synonyms (dict): A dictionary containing synonyms for each keyword (default={}).
        regex_list (list): A list of regular expressions to remove from the content (default=[]).
        use_default_stop_words (bool): A flag indicating whether or not to use the default stop words (default=True).
        stop_words (list): A list of stop words to remove from the content (default=[]).

    Returns:
        list: A list of tuples containing the keyword and its frequency of occurrence in the content, sorted by frequency in descending order.
    """
    try:
        # update keywords with default keywords
        keywords.update(config.keywords) 

        # update synonyms with default synonyms
        keyword_synonyms.update(config.keyword_synonyms)

        # udpate regex list with default regex list
        regex_list.extend(config.invalid_content_regexs)
        
        for regex in regex_list:
            content = re.sub(regex, '', content)

        # Remove punctuation
        content = content.translate(str.maketrans('', '', string.punctuation))

        # Tokenize the data column into words
        words = tokenize_content(content, use_default_stop_words, stop_words)
        
        # Count the frequency of each word
        word_counts = Counter(words)

        # Apply classification keyword weights
        results = {}
        for word, freq in word_counts.items():
            if len(word) <= config.min_word_length:
                continue
            
            for keyword, synonyms in keyword_synonyms.items():
                if word in synonyms:
                    results[keyword] += freq * keywords[keyword]

            results[word] = freq * keywords[word] if word in keywords else freq
                    

        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        return sorted_results
    except Exception as e:
        print(f'Error processing: {e}')
        raise e
    

def extract_classification_text(json_data, validation_regexs=[], stop_words=[]):
    """
    Extract the text from a JSON data structure that contains the used for text classification.

    Args:
        json_data (dict): The JSON data structure to extract the text from.
        validation_regexs (list): A list of regular expressions used to invalidate text instances (default=[]).
        stop_words (list): A list of stop words to remove from the content (default=[]).

    Returns:
        str: The extracted text from the given JSON data structure where element['valid'] == True.
    """
    try:
        cleanse_and_tag_json_structure(json_data, validation_regexs)
        text = extract_text_elements(json_data, lambda x: 'valid' in x and x['valid'] == True)
        text = clean_text(text, True, validation_regexs)
        words = tokenize_content(text, True, stop_words)
        return clean_text(' '.join(words))
    except Exception as e:
        print(f'Error processing: {e}')
        raise e
    
def tokenize_content(content, use_default_stop_words, stop_words=[]):
    """
    Tokenize the given content into a list of words.

    Args:
        content (str): The text content to tokenize.
        use_default_stop_words (bool): A flag indicating whether or not to use the default stop words.
        stop_words (list): A list of stop words to remove from the content (default=[]).

    Returns:
        list: A list of words and their frequency from the given content.
    """
    try:
        if use_default_stop_words:
            stop_words  = get_words(stop_words)

        nlp = spacy.load('en_core_web_sm')
        # Use the tokenizer to split the text into tokens
        doc = nlp(content)
        # Extract the tokens from the spaCy document object
        tokens = [token for token in doc]
        
        return [token.text for token in tokens if token.text.lower() not in stop_words]
    
    except Exception as e:
        print(f'Error processing: {e}')
        raise e
