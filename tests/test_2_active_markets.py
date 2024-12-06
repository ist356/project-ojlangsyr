import pandas as pd

def test_active_markets_filter():
    df_all = pd.read_csv('cache/active_markets.csv')
    df_active = df_all[df_all['active'] == True]
    assert len(df_active) > 0
    assert df_active['active'].all()