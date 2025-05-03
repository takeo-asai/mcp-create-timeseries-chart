import pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents

def caluculate_trend_level(df: pd.DataFrame) -> pd.DataFrame:
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
