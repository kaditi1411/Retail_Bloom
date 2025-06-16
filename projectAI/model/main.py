
import os
import pandas as pd
import matplotlib.pyplot as plt
from app.utils import load_sales_data
from app.forecasting import forecast_with_prophet

# Step 1: Forecast Settings
months_to_forecast = 12
df = load_sales_data("data/large_retail_dataset.csv")
results = []

# Step 2: Forecast per SKU
for sku_id, group in df.groupby("SKU_ID"):
    forecast = forecast_with_prophet(group, industry="textile", periods=months_to_forecast)
    forecast["SKU_ID"] = sku_id
    forecast = forecast.rename(columns={"ds": "Month", "yhat": "Forecasted_Monthly_Sales"})
    results.append(forecast)

# Step 3: Combine and Save Forecasts
forecast_df = pd.concat(results)
os.makedirs("output", exist_ok=True)
forecast_df.to_csv("output/monthly_forecast_results.csv", index=False)
print(f"Monthly forecast saved to output/monthly_forecast_results.csv for {months_to_forecast} months")

# Step 4: Visualization
# Convert to string month labels for X-axis
forecast_df["Month"] = pd.to_datetime(forecast_df["Month"])
forecast_df["MonthStr"] = forecast_df["Month"].dt.strftime("%Y-%m")

# Pivot for grouped bar plot
pivot_df = forecast_df.pivot(index="MonthStr", columns="SKU_ID", values="Forecasted_Monthly_Sales")

# Plotting grouped bar chart
plt.figure(figsize=(14, 6))
pivot_df.plot(kind="bar", width=0.85, figsize=(16, 6), colormap="tab20")

plt.title("Monthly Forecasted Sales per SKU")
plt.xlabel("Month")
plt.ylabel("Forecasted Sales")
plt.xticks(rotation=45, ha="right")
plt.legend(title="SKU ID", bbox_to_anchor=(1.01, 1), loc='upper left')
plt.tight_layout()
plt.grid(axis="y", linestyle="--", alpha=0.5)

# Save and show plot
plt.savefig("output/sku_monthly_forecast.png", dpi=300)
plt.show()
