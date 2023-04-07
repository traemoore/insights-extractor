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

    # Remove all single quotes from the text
    re.sub(r"'", "", text)

    # Remove all new line characters from the text
    text = re.sub('\n', ' ', text)

    # Remove any extra whitespace from the text
    text = re.sub('\s+', ' ', text).strip()

    if remove_punctuation:
        # Remove all punctuation from the text
        text = text.translate(str.maketrans('', '', string.punctuation))

    if regex_list is not None:
        # Remove any substrings that match a regex pattern
        for pattern in regex_list:
            text = re.sub(pattern, '', text)

    # Remove any non-ASCII characters from the text
    text = text.encode('ascii', 'ignore').decode()

    # Return the cleaned text string
    return text
