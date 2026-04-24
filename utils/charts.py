import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']

def revenue_by_category_chart(df):
    fig = px.bar(
        df, x='category', y='total_revenue',
        color='category', color_discrete_sequence=COLORS,
        title='Revenue by Category',
        labels={'total_revenue': 'Total Revenue ($)', 'category': 'Category'}
    )
    fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
    return fig

def revenue_by_region_chart(df):
    fig = px.pie(
        df, names='region', values='total_revenue',
        color_discrete_sequence=COLORS,
        title='Revenue Distribution by Region',
        hole=0.4
    )
    return fig

def revenue_by_channel_chart(df):
    fig = px.bar(
        df, x='channel', y='total_revenue',
        color='channel', color_discrete_sequence=COLORS,
        title='Revenue by Sales Channel',
        labels={'total_revenue': 'Total Revenue ($)', 'channel': 'Channel'}
    )
    fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
    return fig

def monthly_trend_chart(df):
    fig = px.line(
        df, x='month', y='monthly_revenue',
        title='Monthly Revenue Trend',
        labels={'monthly_revenue': 'Revenue ($)', 'month': 'Month'},
        color_discrete_sequence=['#6366f1']
    )
    fig.update_traces(line_width=2.5)
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return fig

def forecast_chart(actual_df, forecast_df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=actual_df['month'],
        y=actual_df['monthly_revenue'],
        name='Actual Revenue',
        line=dict(color='#6366f1', width=2.5)
    ))

    fig.add_trace(go.Scatter(
        x=actual_df['month'],
        y=actual_df['predicted_revenue'],
        name='Predicted Revenue',
        line=dict(color='#10b981', width=2, dash='dot')
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df['month'],
        y=forecast_df['forecasted_revenue'],
        name='Forecast (Next 6 Months)',
        line=dict(color='#ec4899', width=2.5, dash='dash')
    ))

    fig.update_layout(
        title='Sales Forecast — Actual vs Predicted vs Future',
        xaxis_title='Month',
        yaxis_title='Revenue ($)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    return fig

def top_customers_chart(df):
    fig = px.bar(
        df, x='total_spent', y='customer_name',
        orientation='h',
        color_discrete_sequence=['#6366f1'],
        title='Top 10 Customers by Revenue',
        labels={'total_spent': 'Total Spent ($)', 'customer_name': 'Customer'}
    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return fig

def discount_impact_chart(df):
    fig = px.line(
        df, x='discount', y='avg_revenue',
        markers=True,
        color_discrete_sequence=['#ec4899'],
        title='Discount Rate vs Average Order Value',
        labels={'avg_revenue': 'Avg Order Value ($)', 'discount': 'Discount Rate'}
    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return fig