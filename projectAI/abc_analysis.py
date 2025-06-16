import pandas as pd
import matplotlib.pyplot as plt

def abc_classification(df):
    sales_by_sku = df.groupby('sku_id')['sales'].sum().sort_values(ascending=False)
    total_sales = sales_by_sku.sum()
    cum_sales = sales_by_sku.cumsum()
    sales_pct = cum_sales / total_sales

    def classify(x):
        if x <= 0.8:
            return 'A'
        elif x <= 0.95:
            return 'B'
        else:
            return 'C'

    classification = sales_pct.apply(classify)
    return pd.DataFrame({'sku_id': sales_by_sku.index, 'sales': sales_by_sku.values, 'class': classification.values})

def plot_abc_pie(abc_df):
    counts = abc_df['class'].value_counts()
    plt.figure(figsize=(6,6))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['gold','silver','brown'])
    plt.title("ABC Classification Distribution")
    plt.savefig("abc_pie.png")
    plt.close()
