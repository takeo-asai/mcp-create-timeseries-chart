import altair as alt
import pandas as pd
import yfinance as yf
import os
from statsmodels.tsa.statespace.structural import UnobservedComponents

from src.stock import load_dataframe


def fit_state_space_model(df: pd.DataFrame) -> pd.DataFrame:
    # 元の DataFrame をコピー
    df_copy = df.copy()

    # 状態空間モデルの構築とフィッティング
    model = UnobservedComponents(
        df_copy['price'],
        level='local linear trend',
        freq_seasonal=[
            {'period': 7, 'harmonics': 3},   # 1週間の周期性
            {'period': 30, 'harmonics': 6},  # 1ヶ月の周期性
            {'period': 90, 'harmonics': 9},  # 3ヶ月の周期性
            {'period': 365, 'harmonics': 12} # 1年の周期性
        ]
    )
    results = model.fit(maxiter=1000)

    # フィッティング結果を DataFrame に追加
    df_copy['level'] = results.level.smoothed
    df_copy['trend'] = results.trend.smoothed
    # 各季節成分を取得
    for i, freq in enumerate(model.freq_seasonal_periods):
        df_copy[f'seasonal_{freq}'] = results.freq_seasonal[i].smoothed

    conf_int = results.get_prediction().conf_int(alpha=0.05)  # 95% 信頼区間
    df_copy['lower_ci'] = conf_int.iloc[:, 0]  # 信頼区間の下限
    df_copy['upper_ci'] = conf_int.iloc[:, 1]  # 信頼区間の上限
    df_copy.reset_index(inplace=True)
    return df_copy

def main():
    df = load_dataframe("AAPL", period="2y")
    forecast_df = fit_state_space_model(df)
    forecast_df = forecast_df[forecast_df['date'] >= "2024-06-01"]

    # グラフ汎用設定
    x_axis = alt.X('date:T',  axis=alt.Axis(format='%Y-%m', title='日付', tickCount=6))
    y_axis = alt.Y('v:Q', scale=alt.Scale(zero=False), axis=alt.Axis(title='値'))
    v_legend = alt.Legend(title='レベル・実測値', orient='right', symbolStrokeWidth=5, labelFontSize=14, titleFontSize=14)
    v2_legend = alt.Legend(title='トレンド・季節', orient='right', symbolStrokeWidth=5, labelFontSize=14, titleFontSize=14)

    # 上部のグラフ
    actual_level_df = pd.melt(forecast_df, id_vars=['date'], value_vars=['price', 'level'], var_name='c', value_name='v')
    actual_level_chart = alt.Chart(actual_level_df).mark_line().encode(x=x_axis, y=y_axis, color=alt.Color('c:N', legend=v_legend, scale=alt.Scale(scheme='tableau10')))
    confidence_band =  alt.Chart(forecast_df).mark_area(opacity=0.5, color='lightblue').encode(x=x_axis, y='lower_ci:Q', y2='upper_ci:Q')

    # 下部のグラフ
    trend_season_df = pd.melt(forecast_df, id_vars=['date'], value_vars=['trend', 'seasonal_7', 'seasonal_30', 'seasonal_90', 'seasonal_365'], var_name='c', value_name='v')
    trend_season_chart = alt.Chart(trend_season_df).mark_line().encode(x=x_axis, y=y_axis, color=alt.Color('c:N', legend=v2_legend, scale=alt.Scale(scheme='tableau10')))

    # グラフを縦に結合
    upper_chart = (actual_level_chart + confidence_band).properties(title='サンプル時系列グラフ', width=800, height=300)
    lower_chart = trend_season_chart.properties(title='トレンド・季節成分', width=800, height=300)

    final_chart = alt.vconcat(upper_chart, lower_chart).resolve_scale(y='independent', color='independent')
    final_chart.save("output.svg")
    final_chart.save("output.png")


if __name__ == "__main__":
    main()
