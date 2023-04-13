import logging
import json
from .config import *

logging.basicConfig(level=logging.INFO)

try:
    config_settings = config_raw
    logging.info(f'Successfully read config file with values:\n {json.dumps(config_settings, indent=4)}')
except Exception as e:
    logging.error('Error reading config file: %s', str(e))
