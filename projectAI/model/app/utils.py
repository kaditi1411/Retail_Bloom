import pandas as pd
def load_sales_data(path):
    df = pd.read_csv(path, parse_dates=["Date"])
    df = df.groupby(["Product Category", "Date"], as_index=False).agg({"Total Amount": "sum"})
    df = df.rename(columns={"Product Category": "SKU_ID", "Total Amount": "Sales_Quantity"})
    return df.sort_values(["SKU_ID", "Date"])

