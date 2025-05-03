import altair as alt
import pandas as pd

def create_trend_season_chart(df: pd.DataFrame) -> alt.Chart:
    # 下部のグラフ
    x_axis = alt.X('date:T',  axis=alt.Axis(format='%Y-%m', title='日付', tickCount=6))
    y_axis = alt.Y('v:Q', scale=alt.Scale(zero=False), axis=alt.Axis(title='値'))
    v2_legend = alt.Legend(title='トレンド・季節', orient='right', symbolStrokeWidth=5, labelFontSize=14, titleFontSize=14)

    trend_season_df = pd.melt(df, id_vars=['date'], value_vars=['trend', 'seasonal_7', 'seasonal_30', 'seasonal_90', 'seasonal_365'], var_name='c', value_name='v')
    trend_season_chart = alt.Chart(trend_season_df).mark_line().encode(x=x_axis, y=y_axis, color=alt.Color('c:N', legend=v2_legend, scale=alt.Scale(scheme='tableau10')))


    lower_chart = trend_season_chart.properties(title='トレンド・季節成分', width=800, height=300)
    return lower_chart

