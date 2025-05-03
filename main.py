import argparse

from src.stock import load_dataframe
from src.ssm import caluculate_trend_level
from src.alt import create_trend_season_chart, create_actual_level_chart, concat_chart_vertically


def main(ticker, period, output):
    # データの取得
    df = load_dataframe(args.ticker, period=args.period)
    forecast_df = caluculate_trend_level(df)
    forecast_df = forecast_df[forecast_df['date'] >= "2024-06-01"]

    # グラフを縦に結合
    upper_chart = create_actual_level_chart(forecast_df)
    lower_chart = create_trend_season_chart(forecast_df)
    final_chart = concat_chart_vertically(upper_chart, lower_chart)

    final_chart.save(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a time series chart for a stock ticker.")
    parser.add_argument("ticker", type=str, nargs="?", default="AAPL", help="Stock ticker symbol (e.g., AAPL)")
    parser.add_argument("period", type=str, nargs="?", default="2y", help="Time period (e.g., 2y, 1y, 6mo)")
    parser.add_argument("--output", type=str, default="output.svg", help="Output file name with extension (default: 'output.svg'.)")
    args = parser.parse_args()

    main(args.ticker, args.period, args.output)
