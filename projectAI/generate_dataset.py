import pandas as pd
import numpy as np

# Parameters
num_skus = 100          # Number of unique SKUs
days = 90               # Number of days (about 3 months)

# Generate SKU IDs like SKU001, SKU002, ...
sku_ids = [f"SKU{str(i).zfill(3)}" for i in range(1, num_skus+1)]

# Generate date range
date_range = pd.date_range(start='2025-01-01', periods=days)

data = []

for date in date_range:
    for sku in sku_ids:
        sales = np.random.poisson(lam=5)       # average daily sales ~5 units
        stock = np.random.randint(20, 100)     # random stock level between 20 and 100
        data.append([sku, sales, stock, date])

# Create DataFrame
df = pd.DataFrame(data, columns=['sku_id', 'sales', 'stock', 'date'])

# Shuffle data rows
df = df.sample(frac=1).reset_index(drop=True)

# Save as CSV
df.to_csv('large_retail_dataset.csv', index=False)

# Save as Excel
df.to_excel('large_retail_dataset.xlsx', index=False)

print("Large retail dataset generated as 'large_retail_dataset.csv' and 'large_retail_dataset.xlsx'")
