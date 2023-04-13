import json

std_out_logging = True
supported_file_types: list[str] = ['.pdf'],
invalid_content_regexs = []
stop_words = []
keywords = {}
keyword_synonyms = { }
word_min_length = 3
config_raw = None


if not config_raw:
    with open('extractlib.config.json', 'r') as f:
        config_raw = json.load(f)

        if "std_out_logging" in config_raw:
            std_out_logging = config_raw['std_out_logging']
        
        if 'supported_file_types' in config_raw:
            supported_file_types = config_raw['supported_file_types']

        if 'invalid_content_regexs' in config_raw:
            invalid_content_regexs = config_raw['invalid_content_regexs']

        if 'stop_words' in config_raw:
            stop_words = config_raw['stop_words']

        if 'keywords' in config_raw:
            keywords = config_raw['keywords']

        if 'keyword_synonyms' in config_raw:
            keyword_synonyms = config_raw['keyword_synonyms']

        if 'word_min_length' in config_raw:
            word_min_length = config_raw['word_min_length']