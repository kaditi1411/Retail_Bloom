from prophet import Prophet
import pandas as pd
from app.holidays import get_industry_holidays

def forecast_with_prophet(sku_data, industry="general", periods=12):
    # Step 1: Aggregate daily sales into monthly
    sku_data = sku_data.set_index("Date").resample("Me").sum().reset_index()
    df = sku_data.rename(columns={"Date": "ds", "Sales_Quantity": "y"})

    # Step 2: Get holidays based on industry
    holidays = get_industry_holidays(industry)

    # Step 3: Fit Prophet model
    model = Prophet(holidays=holidays, yearly_seasonality=True)
    model.fit(df)

    # Step 4: Forecast future months
    future = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future)

    return forecast[["ds", "yhat"]].tail(periods)  # Only return future months
