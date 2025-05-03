import altair as alt
import pandas as pd

def create_df():
    # DataFrameを作成
    data = {
        'x_values': [1, 2, 3, 4, 5],
        'y_values': [2, 5, 3, 4, 6]
    }
    df = pd.DataFrame(data)
    return df

def main():
    df = create_df()  # DataFrameを作成
    chart = alt.Chart(df).mark_point().encode(
        x='x_values',  # x軸に 'x_values' 列をマッピング
        y='y_values'   # y軸に 'y_values' 列をマッピング
    ).properties(
        title='簡単なサンプルグラフ' # グラフのタイトル (任意)
    )
    chart.save("output.svg")


if __name__ == "__main__":
    main()
