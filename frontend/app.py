# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
import statsmodels
print(statsmodels.__version__)


# Streamlit App Configuration
st.set_page_config(page_title="AI-Powered Retail Insights", layout="wide")

# App Header
st.title("AI-Powered Retail Insights")
st.write("Upload your sales and stock data to get actionable insights!")

# Sidebar for navigation
st.sidebar.header("Navigation")
navigation = st.sidebar.radio("Go to:", ["Upload Data", "Sales Forecasting", "SKU Performance", "Promotion ROI", "Stock Alerts"])

# Function to upload CSV file
def upload_file():
    uploaded_file = st.file_uploader("Upload your CSV file here:", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        return data
    else:
        return None

# Placeholder for forecast model
def forecast_sales(data):
    # Ensure 'Date' column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    
    # Group data by SKU and Date, summing sales quantity
    grouped = data.groupby(['SKU_ID', 'Date']).agg({'Sales_Quantity': 'sum'}).reset_index()
    
    # Forecast for each SKU
    forecasts = []
    for sku, sku_data in grouped.groupby('SKU_ID'):
        sku_data = sku_data.set_index('Date').asfreq('D').fillna(0)
        model = ExponentialSmoothing(sku_data['Sales_Quantity'], trend='add', seasonal=None, initialization_method="estimated")
        model_fit = model.fit()
        forecast = model_fit.forecast(30)
        forecast_df = pd.DataFrame({'Date': forecast.index, 'Forecasted_Sales': forecast.values, 'SKU_ID': sku})
        forecasts.append(forecast_df)
    
    # Combine forecasts
    forecast_results = pd.concat(forecasts)
    return forecast_results

# Upload Data Section
if navigation == "Upload Data":
    st.header("Upload Data")
    data = upload_file()
    if data is not None:
        st.subheader("Preview of Uploaded Data")
        st.write(data.head())
        st.subheader("Data Summary")
        st.write(data.describe())

# Sales Forecasting Section
elif navigation == "Sales Forecasting":
    st.header("Sales Forecasting")
    data = upload_file()
    if data is not None:
        st.subheader("Preview of Uploaded Data")
        st.write(data.head())

        if st.button("Generate Forecast"):
            with st.spinner("Generating forecast..."):
                forecast_results = forecast_sales(data)
                st.success("Forecast generated successfully!")

                st.subheader("Forecast Results")
                st.write(forecast_results)

                st.subheader("Forecast Visualization")
                sku_to_plot = st.selectbox("Select SKU to plot:", forecast_results['SKU_ID'].unique())
                sku_forecast = forecast_results[forecast_results['SKU_ID'] == sku_to_plot]
                plt.figure(figsize=(10, 5))
                plt.plot(sku_forecast['Date'], sku_forecast['Forecasted_Sales'], label='Forecasted Sales')
                plt.title(f"30-Day Sales Forecast for SKU: {sku_to_plot}")
                plt.xlabel("Date")
                plt.ylabel("Sales Quantity")
                plt.legend()
                st.pyplot(plt)

# Other sections (placeholders for now)
elif navigation == "SKU Performance":
    st.header("SKU Performance")
    st.write("This feature is under development.")

elif navigation == "Promotion ROI":
    st.header("Promotion ROI")
    st.write("This feature is under development.")

elif navigation == "Stock Alerts":
    st.header("Stock Alerts")
    st.write("This feature is under development.")
