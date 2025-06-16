import matplotlib.pyplot as plt

def generate_kpis(df):
    total_sales = df['sales'].sum()
    avg_stock = df['stock'].mean()
    avg_daily_sales = df.groupby('date')['sales'].sum().mean()
    stock_turnover = total_sales / avg_stock if avg_stock else 0
    return {
        'Total Sales': total_sales,
        'Average Stock': avg_stock,
        'Average Daily Sales': avg_daily_sales,
        'Stock Turnover Ratio': stock_turnover
    }

def plot_kpi_bar(kpis):
    plt.figure(figsize=(8,5))
    plt.bar(kpis.keys(), kpis.values(), color='skyblue')
    plt.title("KPIs Overview")
    plt.savefig("kpi_bar.png")
    plt.close()
