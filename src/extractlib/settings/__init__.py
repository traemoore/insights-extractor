import logging
from config import read_config_file

logging.basicConfig(level=logging.INFO)

config_settings = None

try:
    config_settings = read_config_file()
    logging.info('Successfully read config file')
except Exception as e:
    logging.error('Error reading config file: %s', str(e))
