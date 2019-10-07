import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

def unix_to_date(value):
    return [dt.datetime.utcfromtimestamp(ts) for ts in value]

filename = r'D:\Code\cs-lib-bitcoin-predictions\omittones\datasets\bitstamp\complete\.bitstampUSD.csv'
input = pd.read_csv(filepath_or_buffer=filename, 
                    header=None, 
                    dtype={
                        'timestamp':np.int64,
                        'price per BTC': np.float32,
                        'amount': np.float32
                        },
                    names=["timestamp","price per BTC","amount"],
                    parse_dates=[0],
                    date_parser=unix_to_date,
                    memory_map=True,
                    na_filter=False,
                    index_col=0,
                    nrows=None)

print("loaded csv...")
print(input.head(20))

print("resampling...")
candlesticks = input['price per BTC'].resample('1d').ohlc()
print(candlesticks.head(20))

# type hints
x: pd.Series = candlesticks['timestamp']
y: pd.Series = candlesticks['high']

# print(input.head())
# print(x.head())
# print(y.head())

_, ax = plt.subplots()
ax.plot(x, y)
ax.set(xlabel=x.name, ylabel=y.name,
       title='Price')
ax.grid()
plt.show()