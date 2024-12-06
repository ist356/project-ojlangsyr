import pandas as pd

def test_all_markets_load():
    df_all = pd.read_csv('cache/all_markets.csv')
    assert len(df_all) > 23000
    required_columns = ['id', 'question', 'volume', 'liquidityNum', 'startDateIso', 'endDateIso']
    assert all(column in df_all.columns for column in required_columns)

def test_all_markets_unique_ids():
    df_all = pd.read_csv('cache/all_markets.csv')
    assert df_all['id'].is_unique
