import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.kpi_metrics import get_revenue_by_category, get_revenue_by_region, get_revenue_by_channel, get_monthly_trend
from utils.charts import revenue_by_category_chart, revenue_by_region_chart, revenue_by_channel_chart, monthly_trend_chart

st.set_page_config(page_title="Sales Analysis", page_icon="📊", layout="wide")
st.title("📊 Sales Analysis")

# Monthly Trend
st.subheader("Monthly Revenue Trend")
trend_df = get_monthly_trend()
st.plotly_chart(monthly_trend_chart(trend_df), use_container_width=True)

st.divider()

# Category + Region side by side
col1, col2 = st.columns(2)
with col1:
    cat_df = get_revenue_by_category()
    st.plotly_chart(revenue_by_category_chart(cat_df), use_container_width=True)
with col2:
    reg_df = get_revenue_by_region()
    st.plotly_chart(revenue_by_region_chart(reg_df), use_container_width=True)

st.divider()

# Channel
channel_df = get_revenue_by_channel()
st.plotly_chart(revenue_by_channel_chart(channel_df), use_container_width=True)

# Raw data table
with st.expander("📋 View Raw Category Data"):
    st.dataframe(cat_df, use_container_width=True)