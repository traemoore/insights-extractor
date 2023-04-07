keywords = {}

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
    duplicate_keywords = []
    for keyword in user_keywords:
        if keyword in keywords:
            duplicate_keywords.append(keyword)
    if len(duplicate_keywords) > 0:
        raise ValueError(f"Duplicate keywords found: {duplicate_keywords}")
    else:
        keywords.update(user_keywords)

def set_keyword_weight(keyword, weight):
    """
    Set the weight of a keyword.

    Args:
        keyword (str): Keyword to set the weight of.
        weight (float): Weight to set the keyword to.

    Returns: None
    """
    keywords[keyword] = weight

def set_keyword_weights(keyword_weights):
    """
    Set the weights of multiple keywords.

    Args:
        keyword_weights (dict): Dictionary of keywords and weights.

    Returns: None

    Example: set_keyword_weights({"keyword1": 1.0, "keyword2": 2.0})
    """
    keywords.update(keyword_weights)