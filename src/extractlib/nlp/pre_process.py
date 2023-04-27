import re
import string

def clean_text(text, remove_punctuation=False, regex_list=None):
    """
    Clean a text string by removing new lines, extra whitespace, and optionally punctuation and non-ASCII characters,
    and matching against a list of regex patterns.

    Args:
        text (str): The input text string to clean.
        remove_punctuation (bool): Whether to remove punctuation from the text (default=False).
        regex_list (list): A list of regex patterns to match against the input text (default=None).

    Returns:
        str: The cleaned text string.
    """

    if regex_list is not None:
        # Remove any substrings that match a regex pattern
        for pattern in regex_list:
            text = re.sub(pattern, '', text)

    # Remove all single quotes from the text
    result = re.sub(r"'", "", text)

    # Remove all new line characters from the text
    result = re.sub('\n', ' ', result)

    if remove_punctuation:
    # Remove all punctuation from the text
        result = result.translate(str.maketrans('', '', string.punctuation))

    # Remove any non-ASCII characters from the text
    result = result.encode('ascii', 'ignore').decode()
    
    result = re.sub(r'\s+', ' ', result).strip()
    result = re.sub(r'\t+', ' ', result).strip()
    # Return the cleaned text string
    return result
