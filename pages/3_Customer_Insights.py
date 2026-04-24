import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.kpi_metrics import get_top_customers, get_discount_impact
from utils.charts import top_customers_chart, discount_impact_chart

st.set_page_config(page_title="Customer Insights", page_icon="👥", layout="wide")
st.title("👥 Customer Insights")

col1, col2 = st.columns(2)
with col1:
    customers_df = get_top_customers()
    st.plotly_chart(top_customers_chart(customers_df), use_container_width=True)
with col2:
    discount_df = get_discount_impact()
    st.plotly_chart(discount_impact_chart(discount_df), use_container_width=True)

st.divider()
st.subheader("📋 Top 10 Customers Detail")
st.dataframe(customers_df, use_container_width=True)