from ...settings import config

keywords = {}
keywords.update(config.keywords)

def get_keywords():
    """
    Get a list of default keywords leveraging nltk.

    Returns:
        dict: dictionary of keywords and weights.
    """
    return keywords

def set_keywords(user_keywords={}):
    """
    Set a list of default keywords and weights, optionally including user-provided keywords.

    Args:
        user_keywords (dict): dictionary of user-provided keywords and weights (default={}).

    Raises:
        ValueError: If duplicate keywords are found in user-provided keywords.

    Returns: None

    Example: set_keywords({"keyword1": 1.0, "keyword2": 2.0})
    """
    if user_keywords:
        keywords.update(user_keywords)

