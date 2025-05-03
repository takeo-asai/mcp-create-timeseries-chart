import altair as alt
import pandas as pd

# TODO: 決め打ちで書いている部分を変数化する

def create_actual_level_chart(df: pd.DataFrame) -> alt.Chart:
    # グラフ汎用設定
    x_axis = alt.X('date:T',  axis=alt.Axis(format='%Y-%m', title='日付', tickCount=6))
    y_axis = alt.Y('v:Q', scale=alt.Scale(zero=False), axis=alt.Axis(title='値'))
    v_legend = alt.Legend(title='レベル・実測値', orient='right', symbolStrokeWidth=5, labelFontSize=14, titleFontSize=14)

    # 上部のグラフ
    actual_level_df = pd.melt(df, id_vars=['date'], value_vars=['price', 'level'], var_name='c', value_name='v')
    actual_level_chart = alt.Chart(actual_level_df).mark_line().encode(x=x_axis, y=y_axis, color=alt.Color('c:N', legend=v_legend, scale=alt.Scale(scheme='tableau10')))
    confidence_band =  alt.Chart(df).mark_area(opacity=0.5, color='lightblue').encode(x=x_axis, y='lower_ci:Q', y2='upper_ci:Q')
    upper_chart = (actual_level_chart + confidence_band).properties(title='サンプル時系列グラフ', width=800, height=300)    
    return upper_chart


def create_trend_season_chart(df: pd.DataFrame) -> alt.Chart:
    # 下部のグラフ
    x_axis = alt.X('date:T',  axis=alt.Axis(format='%Y-%m', title='日付', tickCount=6))
    y_axis = alt.Y('v:Q', scale=alt.Scale(zero=False), axis=alt.Axis(title='値'))
    v2_legend = alt.Legend(title='トレンド・季節', orient='right', symbolStrokeWidth=5, labelFontSize=14, titleFontSize=14)

    trend_season_df = pd.melt(df, id_vars=['date'], value_vars=['trend', 'seasonal_7', 'seasonal_30', 'seasonal_90', 'seasonal_365'], var_name='c', value_name='v')
    trend_season_chart = alt.Chart(trend_season_df).mark_line().encode(x=x_axis, y=y_axis, color=alt.Color('c:N', legend=v2_legend, scale=alt.Scale(scheme='tableau10')))

    lower_chart = trend_season_chart.properties(title='トレンド・季節成分', width=800, height=300)
    return lower_chart


def concat_chart_vertically(upper_chart: alt.Chart, lower_chart: alt.Chart) -> alt.Chart:
    final_chart = alt.vconcat(upper_chart, lower_chart).resolve_scale(y='independent', color='independent')
    return final_chart
