import pandas as pd

def clean_data(df):
    # Basic cleaning: drop rows with missing critical info, convert date, ensure numeric
    df = df.dropna(subset=['sku_id', 'sales', 'stock', 'date'])
    df['date'] = pd.to_datetime(df['date'])
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce').fillna(0)
    df['stock'] = pd.to_numeric(df['stock'], errors='coerce').fillna(0)
    return df
