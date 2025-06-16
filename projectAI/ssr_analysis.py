import pandas as pd
import matplotlib.pyplot as plt

def calculate_ssr(df):
    total_sales = df.groupby('sku_id')['sales'].sum()
    avg_stock = df.groupby('sku_id')['stock'].mean()
    ssr = (avg_stock / total_sales).fillna(0)
    return pd.DataFrame({'sku_id': total_sales.index, 'SSR': ssr.values})

def plot_ssr_histogram(ssr_df):
    plt.figure(figsize=(8,5))
    plt.hist(ssr_df['SSR'], bins=20, color='green')
    plt.title("Stock to Sales Ratio (SSR) Distribution")
    plt.xlabel("SSR")
    plt.ylabel("Frequency")
    plt.savefig("ssr_hist.png")
    plt.close()
