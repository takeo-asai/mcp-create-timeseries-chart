import altair as alt
import pandas as pd

from src.stock import load_dataframe
from src.ssm import caluculate_trend_level
from src.alt import create_trend_season_chart, create_actual_level_chart


def main():
    df = load_dataframe("AAPL", period="2y")
    forecast_df = caluculate_trend_level(df)
    forecast_df = forecast_df[forecast_df['date'] >= "2024-06-01"]

    # グラフを縦に結合
    upper_chart = create_actual_level_chart(forecast_df)
    lower_chart = create_trend_season_chart(forecast_df)
    final_chart = alt.vconcat(upper_chart, lower_chart).resolve_scale(y='independent', color='independent')

    final_chart.save("output.svg")
    final_chart.save("output.png")


if __name__ == "__main__":
    main()
