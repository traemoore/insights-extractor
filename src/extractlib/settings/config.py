import json
import logging
import os

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#create logger
logger = logging.getLogger(__name__)

std_out_logging = True
supported_file_types = ['.pdf']
invalid_content_regexs = []
stop_words = []
keywords = {}
keyword_synonyms = { }
min_word_length = 2
exclude_pages = []
config_raw = None

def update(settings):
    global std_out_logging, supported_file_types, invalid_content_regexs, stop_words, keywords, keyword_synonyms, min_word_length, config_raw, exclude_pages

    if 'std_out_logging' in settings:
        std_out_logging = settings['std_out_logging']
    
    if 'supported_file_types' in settings:
        supported_file_types = list(set(supported_file_types + settings['supported_file_types']))

    if 'invalid_content_regexs' in settings:
        invalid_content_regexs = list(set(invalid_content_regexs + settings['invalid_content_regexs']))

    if 'stop_words' in settings:
        stop_words = list(set(stop_words + settings['stop_words']))

    if 'keywords' in settings:
        keywords.update(settings['keywords'])

    if 'keyword_synonyms' in settings:
        keyword_synonyms.update(settings['keyword_synonyms'])

    if 'word_min_length' in settings:
        min_word_length = settings['word_min_length']
        
    if 'exclude_pages' in settings:
        exclude_pages = settings['exclude_pages']

if __name__ == '__main__':

    # Load configuration file
    if not config_raw:
        if not os.path.exists('extractlib.config.json'):
            logger.warning('No configuration file found. Using empty configuration.')
        else:
            with open('extractlib.config.json', 'r') as f:
                config_raw = json.load(f)

                if "std_out_logging" in config_raw:
                    std_out_logging = config_raw['std_out_logging']

                if 'invalid_content_regexs' in config_raw:
                    invalid_content_regexs = config_raw['invalid_content_regexs']

                if 'stop_words' in config_raw:
                    stop_words = config_raw['stop_words']

                if 'keywords' in config_raw:
                    keywords = config_raw['keywords']

                if 'keyword_synonyms' in config_raw:
                    keyword_synonyms = config_raw['keyword_synonyms']

                if 'word_min_length' in config_raw:
                    min_word_length = config_raw['word_min_length']