import logging
from functions.funcs import load_data
from settings.app import USER_SETTINGS_PATH, APP_NAME


class StartUpException(Exception):
    """"""

logger = logging.getLogger(APP_NAME)
logger.setLevel('DEBUG')
# handler = logging.FileHandler('./finman.log')
# formatter = logging.Formatter('%(asctime)s : %(filename)s.%(funcName)s : %(levelname)s : %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


try:
    user_settings = load_data(USER_SETTINGS_PATH)
except Exception as e:
    error_msg = f'Failed to load user settings from {USER_SETTINGS_PATH}.'
    logger.exception(error_msg)
    raise StartUpException(error_msg)
else:
    logger.info(f'User settings loaded from {USER_SETTINGS_PATH}')

try:
    headers_path = user_settings['stock_list_headers']
    stock_list_headers = load_data(headers_path)
except Exception as e:
    error_msg = f'Failed to load stock list headers from {headers_path}'
    logger.exception(error_msg)
    raise StartUpException(error_msg)
else:
    logger.info(f'Stock list headers loaded from {headers_path}')

try:
    stocks_data_path = user_settings['stocks_data_path']
    stocks_data = load_data(stocks_data_path)
except Exception as e:
    error_msg = f'Failed to load stocks data from {stocks_data_path}'
    logger.exception(error_msg)
    raise StartUpException(error_msg)
else:
    logger.info(f'Stocks data loaded from {stocks_data_path}.')
