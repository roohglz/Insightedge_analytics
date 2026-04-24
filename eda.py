from utils.kpi_metrics import (
    get_top_kpis,
    get_revenue_by_category,
    get_revenue_by_region,
    get_revenue_by_channel,
    get_monthly_trend,
    get_top_customers,
    get_discount_impact
)

print("=" * 50)
print("TOP KPIs")
print("=" * 50)
print(get_top_kpis().to_string(index=False))

print("\n" + "=" * 50)
print("REVENUE BY CATEGORY")
print("=" * 50)
print(get_revenue_by_category().to_string(index=False))

print("\n" + "=" * 50)
print("REVENUE BY REGION")
print("=" * 50)
print(get_revenue_by_region().to_string(index=False))

print("\n" + "=" * 50)
print("REVENUE BY CHANNEL")
print("=" * 50)
print(get_revenue_by_channel().to_string(index=False))

print("\n" + "=" * 50)
print("MONTHLY TREND (first 6 months)")
print("=" * 50)
print(get_monthly_trend().head(6).to_string(index=False))

print("\n" + "=" * 50)
print("TOP 10 CUSTOMERS")
print("=" * 50)
print(get_top_customers().to_string(index=False))

print("\n" + "=" * 50)
print("DISCOUNT IMPACT")
print("=" * 50)
print(get_discount_impact().to_string(index=False))