import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

# fix_yahoo_finance is used to fetch data
import yfinance as yf
yf.pdr_override()

# input
symbol = 'AAPL'
start = '2014-01-01'
end = '2018-12-31'

# Read data
df = yf.download(tickers=symbol,start=start,end=end)

df['SMA_20'] = df['Adj Close'].rolling(20).mean()
df['SMA_40'] = df['Adj Close'].rolling(40).mean()
df['SMA_80'] = df['Adj Close'].rolling(80).mean()

fig, ax = plt.subplots(figsize=(16,9))

ax.plot(df.index, df['Adj Close'], label='Price')
ax.plot(df.index, df['SMA_20'], label = '20-days SMA')
ax.plot(df.index, df['SMA_40'], label = '40-days SMA')
ax.plot(df.index, df['SMA_80'], label = '80-days SMA')

ax.legend(loc='best')
ax.set_ylabel('Price')
ax.set_title('Big Three Trading Strategy')

plt.show()