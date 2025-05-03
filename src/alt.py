import altair as alt
import pandas as pd

# TODO: 決め打ちで書いている部分を変数化する

X_AXIS = alt.X('date:T',  axis=alt.Axis(format='%Y-%m', title='日付', tickCount=6))
Y_AXIS = alt.Y('v:Q', scale=alt.Scale(zero=False), axis=alt.Axis(title='値'))

ACTUAL_LEVEL = ['price', 'level']
TREND_SEASON = ['trend', 'seasonal_7', 'seasonal_30', 'seasonal_90', 'seasonal_365']

def create_color(var_name: str, t: str) -> alt.Color:
    l = alt.Legend(title=t, orient='right', symbolStrokeWidth=5, labelFontSize=14, titleFontSize=14)
    color = alt.Color(f'{var_name}:N', legend=l, scale=alt.Scale(scheme='tableau10'))
    return color


def create_actual_level_chart(df: pd.DataFrame) -> alt.Chart:
    long_df = pd.melt(df, id_vars=['date'], value_vars=ACTUAL_LEVEL, var_name='c', value_name='v')
    actual_level_chart = alt.Chart(long_df).mark_line().encode(x=X_AXIS, y=Y_AXIS, color=create_color('c', 'レベル・実測値'))
    confidence_band =  alt.Chart(df).mark_area(opacity=0.5, color='lightblue').encode(x=X_AXIS, y='lower_ci:Q', y2='upper_ci:Q')
    upper_chart = (actual_level_chart + confidence_band).properties(title='サンプル時系列グラフ', width=800, height=300)    
    return upper_chart


def create_trend_season_chart(df: pd.DataFrame) -> alt.Chart:
    long_df = pd.melt(df, id_vars=['date'], value_vars=TREND_SEASON, var_name='c', value_name='v')
    trend_season_chart = alt.Chart(long_df).mark_line().encode(x=X_AXIS, y=Y_AXIS, color=create_color('c', 'トレンド・季節成分'))
    lower_chart = trend_season_chart.properties(title='トレンド・季節成分', width=800, height=300)
    return lower_chart


def concat_chart_vertically(upper_chart: alt.Chart, lower_chart: alt.Chart) -> alt.Chart:
    final_chart = alt.vconcat(upper_chart, lower_chart).resolve_scale(y='independent', color='independent')
    return final_chart
