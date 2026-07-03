import os
import pandas as pd
from binance.client import Client
from binance.enums import *
import numpy as np

# Binance API credentials
API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Define symbols and time intervals
symbol = 'BTCUSDT'
time_interval = '1d'

# Define moving average days
short_ma = 50
long_ma = 200

# Get historical data
def get_historical_data(symbol, time_interval):
    bars = client.get_klines(symbol=symbol, interval=time_interval, limit=1000)
    df = pd.DataFrame(bars)
    df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Can be ignored'
                   ']
    df['Open'] = pd.to_numeric(df['Open'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])
    return df

# Calculate moving averages
def calculate_moving_averages(df, short_ma, long_ma):
    df['Short MA'] = df['Close'].rolling(window=short_ma).mean()
    df['Long MA'] = df['Close'].rolling(window=long_ma).mean()
    return df

# Define trading logic
def trading_logic(df):
    buy_signal = False
    sell_signal = False
    if df['Short MA'].iloc[-1] > df['Long MA'].iloc[-1] and df['Short MA'].iloc[-2] < df['Long MA'].iloc[-2]:
        buy_signal = True
    elif df['Short MA'].iloc[-1] < df['Long MA'].iloc[-1] and df['Short MA'].iloc[-2] > df['Long MA'].iloc[-2]:
        sell_signal = True
    return buy_signal, sell_signal

# Main function
def main():
    df = get_historical_data(symbol, time_interval)
    df = calculate_moving_averages(df, short_ma, long_ma)
    buy_signal, sell_signal = trading_logic(df)
    if buy_signal:
        print('Buy signal generated')
        # Place buy order
    elif sell_signal:
        print('Sell signal generated')
        # Place sell order
    else:
        print('No signal generated')

if __name__ == '__main__':
    main()