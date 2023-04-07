import nltk

default_stopwords = nltk.corpus.stopwords.words('english')
stopwords = []
def get_words(user_stopwords=[]):
    """
    Get a list of default stopwords leveraging nltk, optionally including user-provided stopwords.

    Args:
        user_stopwords (list): List of user-provided stopwords (default=[]).

    Returns:
        list: List of stopwords.
    """
    user_stopwords.extend(default_stopwords)
    stopwords = list(set(user_stopwords))
    return stopwords
