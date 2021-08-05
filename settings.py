import os

APP_NAME = 'Personal FinTrack'
VERSION = '  v0.0.5.5a'
EMAIL = 'Email: ahbenebha@gmail.com'
DEVELOPER = 'Wenbin Wu'
WEBSITE = 'https://github.com/wenbinwu85/', 'Github'
LICENSE = ''
COPYRIGHT = f'\t(c) 2021 {DEVELOPER}\t'

ADMIN_ACCOUNT = ('ahben', 'ahben')  # hardcoded admin account

STATUS_BAR_MESSAGE = VERSION

APP_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(APP_DIR, 'data')
METRICS_DATA_PATH = os.path.join(DATA_PATH, 'metrics.csv')
ASSETS_DEBTS_DATA_PATH = os.path.join(DATA_PATH, 'assets_debts.csv')
BUDGET_PLAN_DATA_PATH = os.path.join(DATA_PATH, 'budget.csv')
ACCOUNTS_DATA_PATH = os.path.join(DATA_PATH, 'accounts.csv')
STOCKLIST_DATA_PATH = os.path.join(DATA_PATH, 'stocklist.csv')
PERSONAL_SUMMARY_DATA_PATH = os.path.join(DATA_PATH, 'personal_summary.csv')
PASSIVE_INCOME_DATA_PATH = os.path.join(DATA_PATH, 'passive_income.csv')
CREDIT_SCORES_DATA_PATH = os.path.join(DATA_PATH, 'credit_scores.csv')
