import pandas as pd
from utils.db_connector import run_query

# ── 1. TOP-LEVEL KPIs ───────────────────────────────────────────
def get_top_kpis():
    query = """
        SELECT
            COUNT(DISTINCT order_id)            AS total_orders,
            COUNT(DISTINCT customer_id)         AS unique_customers,
            ROUND(SUM(revenue), 2)              AS total_revenue,
            ROUND(AVG(revenue), 2)              AS avg_order_value,
            ROUND(SUM(quantity), 0)             AS total_units_sold
        FROM sales
    """
    return run_query(query)


# ── 2. REVENUE BY CATEGORY ──────────────────────────────────────
def get_revenue_by_category():
    query = """
        SELECT
            category,
            ROUND(SUM(revenue), 2)              AS total_revenue,
            COUNT(DISTINCT order_id)            AS total_orders,
            ROUND(AVG(revenue), 2)              AS avg_order_value
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC
    """
    return run_query(query)


# ── 3. REVENUE BY REGION ────────────────────────────────────────
def get_revenue_by_region():
    query = """
        SELECT
            region,
            ROUND(SUM(revenue), 2)              AS total_revenue,
            COUNT(DISTINCT order_id)            AS total_orders
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    """
    return run_query(query)


# ── 4. REVENUE BY CHANNEL ───────────────────────────────────────
def get_revenue_by_channel():
    query = """
        SELECT
            channel,
            ROUND(SUM(revenue), 2)              AS total_revenue,
            COUNT(DISTINCT order_id)            AS total_orders,
            ROUND(SUM(revenue) * 100.0 / (SELECT SUM(revenue) FROM sales), 2) AS revenue_pct
        FROM sales
        GROUP BY channel
        ORDER BY total_revenue DESC
    """
    return run_query(query)


# ── 5. MONTHLY REVENUE TREND ────────────────────────────────────
def get_monthly_trend():
    query = """
        SELECT
            strftime('%Y-%m', date)             AS month,
            ROUND(SUM(revenue), 2)              AS monthly_revenue,
            COUNT(DISTINCT order_id)            AS monthly_orders
        FROM sales
        GROUP BY month
        ORDER BY month ASC
    """
    return run_query(query)


# ── 6. TOP 10 CUSTOMERS ─────────────────────────────────────────
def get_top_customers():
    query = """
        SELECT
            customer_id,
            customer_name,
            COUNT(DISTINCT order_id)            AS total_orders,
            ROUND(SUM(revenue), 2)              AS total_spent
        FROM sales
        GROUP BY customer_id, customer_name
        ORDER BY total_spent DESC
        LIMIT 10
    """
    return run_query(query)


# ── 7. DISCOUNT IMPACT ──────────────────────────────────────────
def get_discount_impact():
    query = """
        SELECT
            discount,
            COUNT(order_id)                     AS total_orders,
            ROUND(AVG(revenue), 2)              AS avg_revenue,
            ROUND(SUM(revenue), 2)              AS total_revenue
        FROM sales
        GROUP BY discount
        ORDER BY discount ASC
    """
    return run_query(query)