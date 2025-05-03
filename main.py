import altair as alt
import pandas as pd
import yfinance as yf
import os

def create_df(ticker_symbol: str = "AAPL", period: str = "1y") -> pd.DataFrame:
    cache_file = f"{ticker_symbol}_{period}.csv"

    # キャッシュがあれば使用
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
    else:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period).reset_index()[['Date', 'Open']]
        df.columns = ['x_values', 'y_values']
        df.to_csv(cache_file, index=False)
    return df

def main():
    df = create_df("AAPL", period="2y")

    # グラフの作成
    x_axis = alt.X('x_values:T', timeUnit='yearmonth', axis=alt.Axis(format='%Y-%m', title='日付', tickCount=6))
    y_axis = alt.Y('y_values:Q', aggregate='mean', axis=alt.Axis(title='平均株価 $'))
    line = alt.Chart(df).mark_line().encode(x=x_axis, y=y_axis)
    error_band = alt.Chart(df).mark_errorband(extent='ci').encode(x=x_axis, y=y_axis)

    final_chart = (line + error_band).properties(
        title='AAPLの株価時系列グラフ',
        width=800,
        height=300
    )
    final_chart.save("output.svg")


if __name__ == "__main__":
    main()
