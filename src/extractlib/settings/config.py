import json

std_out_logging = True
supported_file_types = [".pdf"],
invalid_content_regexs = []
stop_words = []
keywords = {}
keyword_synonyms = { }
word_min_length = 3


def read_config_file():
    with open('extractlib.config.json', 'r') as f:
        config = json.load(f)

    std_out_logging = config.get('std_out_logging', True)
    supported_file_types = config.get('supported_file_types', [])
    invalid_content_regexs = config.get('invalid_content_regexs', [])
    stop_words = config.get('stop_words', [])
    keywords = config.get('keywords', {})
    keyword_synonyms = config.get('keyword_synonyms', {})
    word_min_length = config.get('word_min_length', 0)

    return {
        'std_out_logging': std_out_logging,
        'supported_file_types': supported_file_types,
        'invalid_content_regexs': invalid_content_regexs,
        'stop_words': stop_words,
        'keywords': keywords,
        'keyword_synonyms': keyword_synonyms,
        'word_min_length': word_min_length
    }