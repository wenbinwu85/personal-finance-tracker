import yfinance as yf
from .funcs import dump_data

ticker = yf.Ticker('MSFT')
dump_data(ticker, 'msft')
