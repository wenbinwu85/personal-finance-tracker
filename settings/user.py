from settings.app import USER_SETTINGS_PATH
from functions.funcs import logger, load_data

try:
    user_settings = load_data(USER_SETTINGS_PATH)
except Exception as e:
    error_msg = f'Failed to load user settings from {USER_SETTINGS_PATH}:\n{e}'
    logger.exception(error_msg)
    raise
else:
    logger.info(f'User settings loaded from {USER_SETTINGS_PATH}.')

try:
    stock_header_path = user_settings['stock_header_path']
    stock_data_path = user_settings['stock_data_path']
except KeyError as e:
    error_msg = f'User setting missing:\n{e}'
    logger.exception(error_msg)
    raise
else:
    logger.info('User settings loaded')
