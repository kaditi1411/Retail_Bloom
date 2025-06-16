import pandas as pd
import numpy as np

dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq='D')

def seasonal_sales(date, base, amplitude, peak_months):
    month = date.month
    # peak months increase sales
    if month in peak_months:
        return base + amplitude + np.random.randint(-2, 3)
    else:
        return base + np.random.randint(-2, 3)

data = []
for sku in ["SKU_001", "SKU_002"]:
    for date in dates:
        if sku == "SKU_001":
            # SKU_001: higher sales in Oct, Nov, Dec (festival/winter season)
            qty = seasonal_sales(date, base=15, amplitude=20, peak_months=[10,11,12])
        else:
            # SKU_002: higher sales in May, Jun, Jul (summer season)
            qty = seasonal_sales(date, base=10, amplitude=15, peak_months=[5,6,7])
        qty = max(qty, 0)  # no negative sales
        data.append({"Date": date.strftime("%Y-%m-%d"), "SKU_ID": sku, "Sales_Quantity": qty})

df = pd.DataFrame(data)
df.to_csv("raw_sales.csv", index=False)
print("raw_sales.csv generated.")
