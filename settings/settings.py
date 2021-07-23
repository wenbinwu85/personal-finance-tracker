import os
from fintrack import appdir
from functions.funcs import logger, load_data

##### app settings #####
APP_NAME = 'FinTrack'
VERSION = '  v0.0.5.1a'
EMAIL = 'Email: ahbenebha@gmail.com'
DEVELOPER = 'Wenbin Wu'
WEBSITE = 'https://github.com/wenbinwu85/', 'Github'
LICENSE = 'Free for ahben.'
COPYRIGHT = f'\t(c) 2021 {DEVELOPER}, all rights reserved\t'

ADMIN_ACCOUNT = ('ahben', 'ahben')  # hardcoded admin account

STATUS_BAR_MESSAGE = 'Welcome Ahben!'

USER_SETTINGS_PATH = os.path.join(appdir, 'settings', 'user.json')


##### user settings #####
try:
    user_settings = load_data(USER_SETTINGS_PATH)
except Exception as e:
    error_msg = f'Failed to load user settings from {USER_SETTINGS_PATH}:\n{e}'
    logger.exception(error_msg)
    raise
else:
    logger.info(f'User settings loaded from {USER_SETTINGS_PATH}.')

try:
    stock_header_path = user_settings.get('stock_header_path')
    stock_data_path = user_settings.get('stock_data_path')
except KeyError as e:
    error_msg = f'User setting missing:\n{e}'
    logger.exception(error_msg)
    raise
else:
    logger.info('User settings loaded')
