import logging
from functions.cjs import CJS
from settings.app import USER_SETTINGS_PATH, APP_NAME


class StartUpException(Exception):
    """"""

logger = logging.getLogger(APP_NAME)
logger.setLevel('DEBUG')
# handler = logging.FileHandler('./finman.log')
# formatter = logging.Formatter('%(asctime)s : %(filename)s.%(funcName)s : %(levelname)s : %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


cjs = CJS()

try:
    user_settings = cjs.load(USER_SETTINGS_PATH)
except Exception as e:
    logger.exception(f'Failed to load user settings from {USER_SETTINGS_PATH}.')
    raise StartUpException(e)
else:
    logger.info(f'User settings loaded from {USER_SETTINGS_PATH}')

try:
    stocks_data_path = user_settings['stocks_data_path']
    stocks_data = cjs.load(stocks_data_path)
except Exception as e:
    logger.exception(f'Failed to load stocks data from {stocks_data_path}')
    raise StartUpException(e)
else:
    logger.info(f'Stocks data loaded from {stocks_data_path}.')

try:
    header_path = user_settings['stock_list_headers']
    stock_list_headers = cjs.load(header_path)
except Exception as e:
    logger.exception(f'Failed to load stock list headers from {header_path}')
