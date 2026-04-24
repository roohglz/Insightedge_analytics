import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
import plotly.express as px
import plotly.graph_objects as go
import io
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Upload Your Data", page_icon="📂", layout="wide")
st.title("📂 Upload Your Data")
st.caption("Upload your own sales CSV and get instant BI insights + ML forecast")

# ── TEMPLATE DOWNLOAD ────────────────────────────────────────────
st.subheader("Step 1 — Download the Template")
st.write("Your CSV must have these columns:")

sample = pd.DataFrame({
    'date': ['2024-01-15', '2024-01-20'],
    'order_id': ['ORD-001', 'ORD-002'],
    'customer_id': ['CUST-001', 'CUST-002'],
    'customer_name': ['John Doe', 'Jane Smith'],
    'category': ['Electronics', 'Clothing'],
    'product': ['Laptop', 'T-Shirt'],
    'region': ['North', 'South'],
    'channel': ['Online', 'Retail'],
    'unit_price': [999.99, 29.99],
    'quantity': [1, 3],
    'discount': [0.10, 0.0],
    'revenue': [899.99, 89.97]
})

st.dataframe(sample, use_container_width=True)

csv_template = sample.to_csv(index=False)
st.download_button(
    label="⬇️ Download CSV Template",
    data=csv_template,
    file_name="insightedge_template.csv",
    mime="text/csv"
)

st.divider()

# ── FILE UPLOAD ──────────────────────────────────────────────────
st.subheader("Step 2 — Upload Your CSV")
uploaded_file = st.file_uploader("Choose your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Validate columns
        required_cols = ['date', 'order_id', 'customer_id', 'customer_name',
                        'category', 'product', 'region', 'channel',
                        'unit_price', 'quantity', 'discount', 'revenue']

        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            st.error(f"❌ Missing columns: {', '.join(missing)}. Please use the template.")
            st.stop()

        df['date'] = pd.to_datetime(df['date'])
        st.success(f"✅ Loaded {len(df):,} records successfully!")

        st.divider()

        # ── KPI CARDS ────────────────────────────────────────────
        st.subheader("📊 Your KPIs")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("💰 Total Revenue", f"${df['revenue'].sum():,.0f}")
        col2.metric("📦 Total Orders", f"{df['order_id'].nunique():,}")
        col3.metric("👥 Unique Customers", f"{df['customer_id'].nunique():,}")
        col4.metric("🛒 Avg Order Value", f"${df['revenue'].mean():,.2f}")
        col5.metric("📊 Units Sold", f"{df['quantity'].sum():,}")

        st.divider()

        # ── CHARTS ───────────────────────────────────────────────
        st.subheader("📈 Sales Analysis")

        col1, col2 = st.columns(2)

        with col1:
            cat_df = df.groupby('category')['revenue'].sum().reset_index()
            fig = px.bar(cat_df, x='category', y='revenue',
                        color='category', title='Revenue by Category',
                        color_discrete_sequence=['#6366f1','#8b5cf6','#ec4899','#f59e0b','#10b981'])
            fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            reg_df = df.groupby('region')['revenue'].sum().reset_index()
            fig = px.pie(reg_df, names='region', values='revenue',
                        title='Revenue by Region', hole=0.4,
                        color_discrete_sequence=['#6366f1','#8b5cf6','#ec4899','#f59e0b','#10b981'])
            st.plotly_chart(fig, use_container_width=True)

        # Monthly trend
        monthly = df.groupby(df['date'].dt.to_period('M'))['revenue'].sum().reset_index()
        monthly['date'] = monthly['date'].astype(str)
        fig = px.line(monthly, x='date', y='revenue',
                     title='Monthly Revenue Trend',
                     color_discrete_sequence=['#6366f1'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ── ML FORECAST ──────────────────────────────────────────
        st.subheader("🤖 ML Sales Forecast")

        monthly_ml = df.groupby(df['date'].dt.to_period('M'))['revenue'].sum().reset_index()
        monthly_ml.columns = ['month', 'monthly_revenue']
        monthly_ml = monthly_ml.iloc[:-1].reset_index(drop=True)  # drop incomplete month
        monthly_ml['month_index'] = range(len(monthly_ml))
        monthly_ml['month_num'] = monthly_ml['month'].dt.month
        monthly_ml['year'] = monthly_ml['month'].dt.year
        monthly_ml['sin_month'] = np.sin(2 * np.pi * monthly_ml['month_num'] / 12)
        monthly_ml['cos_month'] = np.cos(2 * np.pi * monthly_ml['month_num'] / 12)

        if len(monthly_ml) < 15:
            st.warning("⚠️ Need at least 15 months of data for forecasting. Upload more data!")
        else:
            monthly_ml['lag_1'] = monthly_ml['monthly_revenue'].shift(1)
            monthly_ml['lag_2'] = monthly_ml['monthly_revenue'].shift(2)
            monthly_ml['lag_12'] = monthly_ml['monthly_revenue'].shift(12)
            monthly_ml['rolling_3'] = monthly_ml['monthly_revenue'].rolling(3).mean()
            monthly_ml['rolling_6'] = monthly_ml['monthly_revenue'].rolling(6).mean()
            monthly_ml = monthly_ml.dropna().reset_index(drop=True)

            features = ['month_index', 'month_num', 'year', 'sin_month', 'cos_month',
                       'lag_1', 'lag_2', 'lag_12', 'rolling_3', 'rolling_6']

            X = monthly_ml[features]
            y = monthly_ml['monthly_revenue']

            model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.05,
                                              max_depth=3, random_state=42)
            model.fit(X, y)

            r2 = r2_score(y, model.predict(X))
            st.info(f"🎯 Model Accuracy: {r2*100:.2f}%")

            # Forecast 6 months
            last_index = monthly_ml['month_index'].iloc[-1]
            last_month = monthly_ml['month'].iloc[-1]
            history = list(monthly_ml['monthly_revenue'])

            forecasts = []
            for i in range(1, 7):
                next_month = last_month + i
                lag_1 = history[-1]
                lag_2 = history[-2]
                lag_12 = history[-12] if len(history) >= 12 else np.mean(history)
                rolling_3 = np.mean(history[-3:])
                rolling_6 = np.mean(history[-6:])

                feat = pd.DataFrame([{
                    'month_index': last_index + i,
                    'month_num': next_month.month,
                    'year': next_month.year,
                    'sin_month': np.sin(2 * np.pi * next_month.month / 12),
                    'cos_month': np.cos(2 * np.pi * next_month.month / 12),
                    'lag_1': lag_1, 'lag_2': lag_2, 'lag_12': lag_12,
                    'rolling_3': rolling_3, 'rolling_6': rolling_6
                }])

                predicted = max(0, model.predict(feat)[0])
                forecasts.append({'month': str(next_month), 'forecasted_revenue': round(predicted, 2)})
                history.append(predicted)

            forecast_df = pd.DataFrame(forecasts)

            # Plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly_ml['month'].astype(str),
                y=monthly_ml['monthly_revenue'],
                name='Actual', line=dict(color='#6366f1', width=2.5)
            ))
            fig.add_trace(go.Scatter(
                x=forecast_df['month'],
                y=forecast_df['forecasted_revenue'],
                name='Forecast', line=dict(color='#ec4899', width=2.5, dash='dash')
            ))
            fig.update_layout(
                title='Your Sales Forecast — Next 6 Months',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h')
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📅 Forecast Table")
            st.dataframe(forecast_df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")