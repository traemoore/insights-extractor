import logging
from settings.config import read_config_file

logging.basicConfig(level=logging.INFO)

config_settings = None

try:
    config_settings = read_config_file()
    logging.info('Successfully read config file with values:\n {config_settings}')
except Exception as e:
    logging.error('Error reading config file: %s', str(e))
