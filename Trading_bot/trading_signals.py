from datetime import datetime
import time
import pandas as pd
import MetaTrader5 as mt5

def bollinger_bands(data, window=20, std=2):
  """
  This function calculates Bollinger Bands (SMA, upper band, lower band) for a given data series.

  Args:
      data (pandas.Series): The data series containing closing prices (or any relevant price data).
      window (int, optional): The window length for the moving average. Defaults to 20.
      std (int, optional): The number of standard deviations for the bands. Defaults to 2.

  Returns:
      pandas.DataFrame: A DataFrame containing the original data, SMA, upper Bollinger Band, and lower Bollinger Band.
  """

  # Calculate Simple Moving Average (SMA)
  sma = data.rolling(window=window).mean()

  # Calculate standard deviation
  stddev = data.rolling(window=window).std()

  # Upper Bollinger Band (SMA + stddev * multiplier)
  upper_band = sma + std * stddev

  # Lower Bollinger Band (SMA - stddev * multiplier)
  lower_band = sma - std * stddev

  # Create DataFrame with results
  results = pd.DataFrame({
      "Close": data,
      "SMA": sma,
      "Upper Band": upper_band,
      "Lower Band": lower_band
  })

  return results


def compute_rsi(data, window=14):
  """
  This function calculates the Relative Strength Index (RSI) for a given data series.

  Args:
      data (pandas.Series): The data series containing closing prices.
      window (int, optional): The window length for RSI calculation. Defaults to 14.

  Returns:
      pandas.Series: A Series containing the RSI values for each data point.
  """

  delta = data.diff()
  delta = delta.dropna()  # Ignore first NaN value

  up = delta[delta > 0]
  down = -delta[delta < 0]

  avg_up = up.ewm(alpha=1/window, min_periods=window).mean()
  avg_down = down.ewm(alpha=1/window, min_periods=window).mean()

  rs = avg_up / avg_down
  rsi = 100 - 100 / (1 + rs)

  return rsi


def compute_macd(data, fast=12, slow=26, signal=9):
  """
  This function calculates the Moving Average Convergence Divergence (MACD) for a given data series.

  Args:
      data (pandas.Series): The data series containing closing prices.
      fast (int, optional): The window length for the fast EMA. Defaults to 12.
      slow (int, optional): The window length for the slow EMA. Defaults to 26.
      signal (int, optional): The window length for the signal EMA. Defaults to 9.

  Returns:
      tuple: A tuple containing MACD, MACD Signal, and MACD Histogram.
  """

  ema_fast = data.ewm(alpha=1/fast, min_periods=fast).mean()
  ema_slow = data.ewm(alpha=1/slow, min_periods=slow).mean()

  macd = ema_fast - ema_slow
  macd_signal = macd.ewm(alpha=1/signal, min_periods=signal).mean()
  macd_hist = macd - macd_signal

  return macd, macd_signal, macd_hist


def forex_signals(data, window=20, std=2, rsi_window=14, macd_fast=12, macd_slow=26, macd_signal=9):
    """
    This function calculates Bollinger Bands, RSI, MACD, and generates Buy/Sell signals for Forex trading.

    Args:
        data (pandas.DataFrame): The DataFrame containing OHLC (Open, High, Low, Close) prices.
        window (int, optional): The window length for Bollinger Bands moving average. Defaults to 20.
        std (int, optional): The number of standard deviations for Bollinger Bands. Defaults to 2.
        rsi_window (int, optional): The window length for RSI calculation. Defaults to 14.
        macd
    """


### Executive
    
def generate_signals(symbol="GBPCHFm"):
    ticker = symbol
    login = 123992590
    password = "Demo5@211993!"
    server = "Exness-MT5Trial7"

    initialize = mt5.initialize()

    if initialize:
        mt5.login(login, password, server)
        print("Info: Connected to MetaTrader5")

    df = mt5.copy_rates_range(ticker, mt5.TIMEFRAME_M5, datetime(2023,7,21), datetime.now())
    # print(pd.DataFrame(df))

    date = []
    open = []
    high = []
    low = []
    close = []
    volume = []
    spread = []
    date_format = "%Y-%m-%d"

    for i in range(len(df)):
        date.append(time.strftime(date_format, time.localtime(df[i]['time'])))
        open.append(df[i]['open'])
        high.append(df[i]['high'])
        low.append(df[i]['low'])
        close.append(df[i]['close'])
        volume.append(df[i]['tick_volume'])
        spread.append(df[i]['spread'])

    date_df = pd.DataFrame(date).rename(columns = {0:'date'})
    open_df = pd.DataFrame(open).rename(columns = {0:'open'})
    high_df = pd.DataFrame(high).rename(columns = {0:'high'})
    low_df = pd.DataFrame(low).rename(columns = {0:'low'})
    close_df = pd.DataFrame(close).rename(columns = {0:'close'})
    volume_df = pd.DataFrame(volume).rename(columns = {0:'tick_volume'})
    spread_df = pd.DataFrame(spread).rename(columns = {0:'spread'})
    frames = [date_df, open_df, high_df, low_df, close_df, volume_df, spread_df]
    df = pd.concat(frames, axis = 1, join = 'inner')

    dataFrame = pd.DataFrame(df)

    print(dataFrame)

    forex_signals(dataFrame)
