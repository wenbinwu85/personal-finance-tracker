import os

APP_NAME = 'FinTrack'
VERSION = 'v0.0.9'
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
STOCKLIST_DATA_PATH = os.path.join(DATA_PATH, 'stocks.csv')
CREDIT_SCORES_DATA_PATH = os.path.join(DATA_PATH, 'credit_scores.csv')

net_worth_labels = ['Total Debts', 'Total Assets', 'Net Worth', 'D/A Ratio %']
passive_income_labels = [
    'Annual Yield %', 'Annual Yield', 'Monthly Yield', 'Total Dividend Earned'
]
metrics_columns = [
    'Month', 'TSP', 'Schwab', 'Roth IRA', 'Webull', 'Coinbase',
    'Dividend', 'Invested', 'Cash', 'Debts', 'Assets', 'Net Worth'
]

assets_debts_columns = ['Item', 'Value', 'Type', 'Note']
budget_plan_columns = ['Item', 'Amount', 'Time', 'Due Date', 'Type', 'Payback Plan']
accounts_columns = ['Account', 'Type', 'Status']

stocks_columns = [
    'Symbol', 'Shares', 'Cost Avg',
    'Price', 'Cost Basis', 'Market Value', 'Gain / Lost', 'G / L %',
    'Yield %', 'Annual Div', 'Div. Earned',
    'Y / C %', 'Beta', 'P/E', 'EPS', '1Y Target',
    'Payout %', '1Y Div ^', '3Y Div ^', '5Y Div ^',
    'Sector', 'Account'
]

stocks_footer_columns = [
    'Selected', 'Cost Basis', 'Market Value', 'Gain / Lost', 'Gain / Lost %',
    'Yield %', 'Annual Dividend', 'Div. Received', 'Account %'
]
