import pandas as pd
import matplotlib.pyplot as plt

def generate_recommendations(df):
    sales_by_sku = df.groupby('sku_id')['sales'].sum().sort_values(ascending=False)
    recommendations = []
    for sku, sales in sales_by_sku.items():
        if sales < 50:
            recommendations.append({'sku_id': sku, 'recommendation': 'Increase Promotion'})
        else:
            recommendations.append({'sku_id': sku, 'recommendation': 'Maintain'})
    return pd.DataFrame(recommendations)

def plot_recommendation_summary(recs_df):
    counts = recs_df['recommendation'].value_counts()
    plt.figure(figsize=(6,6))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['lightcoral','lightblue'])
    plt.title("Recommendations Summary")
    plt.savefig("recs_summary.png")
    plt.close()
