import matplotlib.pyplot as plt
import pandas as pd

def plot_sales_trend(df):
    sales_trend = df.groupby('date')['sales'].sum()
    plt.figure(figsize=(10,5))
    plt.plot(sales_trend.index, sales_trend.values, marker='o', linestyle='-')
    plt.title("Sales Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("sales_trend.png")
    plt.close()
