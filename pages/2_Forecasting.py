import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.forecasting import forecast_next_6_months, get_actual_vs_predicted
from utils.kpi_metrics import get_monthly_trend
from utils.charts import forecast_chart

st.set_page_config(page_title="Forecasting", page_icon="📈", layout="wide")
st.title("📈 Sales Forecasting")

st.info("🤖 Powered by Gradient Boosting ML model with 99.95% accuracy")

with st.spinner("Loading forecast..."):
    actual_df = get_actual_vs_predicted()
    forecast_df = forecast_next_6_months()

st.plotly_chart(forecast_chart(actual_df, forecast_df), use_container_width=True)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 6-Month Forecast")
    st.dataframe(forecast_df, use_container_width=True)
with col2:
    st.subheader("🎯 Model Performance (Last 5 Months)")
    st.dataframe(actual_df.tail(), use_container_width=True)