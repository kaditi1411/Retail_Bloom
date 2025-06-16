import streamlit as st
import pandas as pd
from data_cleaning import clean_data
from kpi_analysis import generate_kpis, plot_kpi_bar
from abc_analysis import abc_classification, plot_abc_pie
from ssr_analysis import calculate_ssr, plot_ssr_histogram
from recommendation_engine import generate_recommendations, plot_recommendation_summary
from sales_trend import plot_sales_trend
from app.forecasting import forecast_with_prophet
import plotly.graph_objects as go

st.title("AI-Powered Retail Analytics Dashboard")

uploaded_file = st.file_uploader("Upload your sales and stock Excel/CSV file", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")
    df = clean_data(df)

    # KPIs
    kpis = generate_kpis(df)
    st.subheader("📊 Key Performance Indicators (KPIs)")
    for k, v in kpis.items():
        st.metric(label=k, value=round(v, 2))
    plot_kpi_bar(kpis)
    st.image("kpi_bar.png")

    # ABC
    abc = abc_classification(df)
    st.subheader("🔤 ABC Classification")
    st.dataframe(abc)
    plot_abc_pie(abc)
    st.image("abc_pie.png")

    # SSR
    ssr = calculate_ssr(df)
    st.subheader("📈 Stock to Sales Ratio (SSR)")
    st.dataframe(ssr)
    plot_ssr_histogram(ssr)
    st.image("ssr_hist.png")

    # Recommendations
    recs = generate_recommendations(df)
    st.subheader("💡 Recommendations")
    st.dataframe(recs)
    plot_recommendation_summary(recs)
    st.image("recs_summary.png")

    # Sales Trend
    st.subheader("📅 Sales Trend")
    plot_sales_trend(df)
    st.image("sales_trend.png")

    # --- Forecasting Section ---   
    st.markdown("## 🔮 Sales Forecasting")
    st.subheader("📉 Forecasted Sales")

    # --- Forecast Controls ---
    st.markdown("### 🔧 Forecast Configuration")
    
    forecast_options = {
        "Quarterly (3 months)": 3,
        "Half-Yearly (6 months)": 6,
        "Yearly (12 months)": 12
    }
    
    forecast_choice = st.selectbox("Select Forecast Duration", list(forecast_options.keys()))
    months_to_forecast = forecast_options[forecast_choice]

    min_date = df['date'].min().to_pydatetime()
    max_date = df['date'].max().to_pydatetime()

    forecast_start_date = st.date_input(
        "Select Start Month for Forecasting", 
        value=max_date, 
        min_value=min_date, 
        max_value=max_date
    )

    # Filter data based on selected forecast start month
    df_filtered = df[df["date"] <= pd.to_datetime(forecast_start_date)]

    st.markdown(f"### 📈 Forecasting {months_to_forecast} Months Ahead from {forecast_start_date.strftime('%B %Y')}")

    forecast_results = []
    for sku_id, group in df_filtered.groupby("sku_id"):
        try:
            forecast = forecast_with_prophet(group.rename(columns={
                "date": "Date", "sales": "Sales_Quantity"
            }), industry="textile", periods=months_to_forecast)
            forecast["SKU_ID"] = sku_id
            forecast = forecast.rename(columns={"ds": "Month", "yhat": "Forecasted_Sales"})
            forecast_results.append(forecast)
        except Exception as e:
            st.warning(f"⚠️ Forecasting failed for SKU {sku_id}: {e}")

    if forecast_results:
        forecast_df = pd.concat(forecast_results)
        st.dataframe(forecast_df)

        # Forecast Visualization
        st.markdown("### 🔍 Forecast Visualization with Zoom & Interactivity")

        forecast_df["Month"] = pd.to_datetime(forecast_df["Month"])
        forecast_df["MonthStr"] = forecast_df["Month"].dt.strftime("%Y-%m")
        pivot_df = forecast_df.pivot(index="MonthStr", columns="SKU_ID", values="Forecasted_Sales")

        fig = go.Figure()
        for sku in pivot_df.columns:
            fig.add_trace(go.Bar(
                x=pivot_df.index,
                y=pivot_df[sku],
                name=f"SKU {sku}"
            ))

        fig.update_layout(
            title=f"Forecasted Sales ({forecast_choice})",
            xaxis_title="Month",
            yaxis_title="Forecasted Sales",
            barmode='group',
            height=600,
            width=1200,
            legend_title="SKU ID",
            xaxis=dict(
                tickangle=-45,
                rangeslider=dict(visible=True),
                showgrid=True,
                showline=True
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=True,
                showline=True,
                rangemode='tozero'
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ Forecasting could not be performed on the uploaded data.")
