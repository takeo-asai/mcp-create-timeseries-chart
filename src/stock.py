import os
import pandas as pd
import yfinance as yf

def load_dataframe(ticker_symbol: str = "AAPL", period: str = "1y") -> pd.DataFrame:
    cache_file = f"tmp/{ticker_symbol}_{period}.csv"

    # キャッシュがあれば使用
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
    else:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period).reset_index()[['Date', 'Open']]
        df.columns = ['date', 'price']
        df.to_csv(cache_file, index=False)
    # x_values に余分な文字列が付いているので削除し、日付形式に変換
    df['date'] = df['date'].replace(r' 00:00:00-0\d:00', '', regex=True)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.set_index('date', inplace=True)
    if df.index.freq is None:
        df = df.asfreq('D')  # 日次データとして設定
    df['price'] = df['price'].ffill() # price の NaN を前日の値で埋める
    return df
