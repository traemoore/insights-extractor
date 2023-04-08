import nltk
from nltk import word_tokenize, pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def get_entities(text):
    """
    Extract entities from text using NLTK.

    Args:
        text (str): The text to extract entities from.

    Returns:
        list: A list of entities.
    """
    try:
        entities = []
        for token in nltk.sent_tokenize(text):
            for chunk in nltk.ne_chunk(pos_tag(word_tokenize(token))):
                if hasattr(chunk, 'label'):
                    entities.append((' '.join(c[0] for c in chunk), chunk.label()))
        return entities
    except Exception as e:
        print(f'Error processing: {e}')
        raise e