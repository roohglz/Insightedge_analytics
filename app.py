import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils.kpi_metrics import get_top_kpis, get_monthly_trend
from utils.charts import monthly_trend_chart

st.set_page_config(
    page_title="InsightEdge Analytics",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 InsightEdge Analytics")
st.caption("Business Intelligence Dashboard — Powered by Python, SQL & ML")

st.divider()

# ── KPI CARDS ───────────────────────────────────────────────────
with st.spinner("Loading KPIs..."):
    kpis = get_top_kpis().iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💰 Total Revenue", f"${kpis['total_revenue']:,.0f}")
col2.metric("📦 Total Orders", f"{kpis['total_orders']:,}")
col3.metric("👥 Unique Customers", f"{kpis['unique_customers']:,}")
col4.metric("🛒 Avg Order Value", f"${kpis['avg_order_value']:,.2f}")
col5.metric("📊 Units Sold", f"{kpis['total_units_sold']:,.0f}")

st.divider()

# ── TREND CHART ─────────────────────────────────────────────────
st.subheader("📈 Revenue Trend Overview")
trend_df = get_monthly_trend()
st.plotly_chart(monthly_trend_chart(trend_df), use_container_width=True)

st.divider()
st.markdown("👈 **Use the sidebar to explore Sales Analysis, Forecasting, and Customer Insights**")