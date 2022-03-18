import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf

# Using yfinance to retrieve data
# soybean_ticker = 'ZS=F'
# soybean_futures_prices = 'zsf'

zsf = yf.Ticker("ZS=F")

# get historical market data
hist_F = zsf.history(period="max")
hist_F = hist_F.drop(columns=['Dividends','Stock Splits'])

mpf.plot(hist_F, type='candle', warn_too_much_data= 10000)
