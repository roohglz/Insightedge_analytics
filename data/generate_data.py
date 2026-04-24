import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)
random.seed(42)

NUM_RECORDS = 10000
CATEGORIES = ['Electronics', 'Clothing', 'Food & Beverages', 'Home & Garden', 'Sports']
REGIONS = ['North', 'South', 'East', 'West', 'Central']
CHANNELS = ['Online', 'Retail', 'Wholesale']

def get_seasonal_multiplier(month):
    # Real-world seasonality pattern
    seasonality = {
        1: 0.7, 2: 0.75, 3: 0.85, 4: 0.90,
        5: 0.95, 6: 1.0, 7: 1.05, 8: 1.1,
        9: 1.15, 10: 1.2, 11: 1.4, 12: 1.6
    }
    return seasonality[month]

def generate_sales_data():
    records = []
    start_date = datetime(2021, 1, 1)

    for i in range(NUM_RECORDS):
        category = random.choice(CATEGORIES)
        region = random.choice(REGIONS)
        channel = random.choice(CHANNELS)

        price_map = {
            'Electronics': (200, 2000),
            'Clothing': (20, 300),
            'Food & Beverages': (5, 100),
            'Home & Garden': (50, 800),
            'Sports': (30, 500)
        }

        days_offset = random.randint(0, 365 * 5)
        date = start_date + timedelta(days=days_offset)

        # Apply seasonality to quantity
        seasonal_multiplier = get_seasonal_multiplier(date.month)
        base_quantity = random.randint(1, 20)
        quantity = max(1, int(base_quantity * seasonal_multiplier))

        # Apply yearly growth trend (5% per year)
        year_multiplier = 1 + (0.05 * (date.year - 2021))

        unit_price = round(random.uniform(*price_map[category]) * year_multiplier, 2)
        discount = round(random.choice([0, 0.05, 0.10, 0.15, 0.20]), 2)
        revenue = round(unit_price * quantity * (1 - discount), 2)

        records.append({
            'order_id': f'ORD-{10000 + i}',
            'date': date.strftime('%Y-%m-%d'),
            'customer_id': f'CUST-{random.randint(1000, 5000)}',
            'customer_name': fake.name(),
            'category': category,
            'product': f'{category} Product {random.randint(1, 50)}',
            'region': region,
            'channel': channel,
            'unit_price': unit_price,
            'quantity': quantity,
            'discount': discount,
            'revenue': revenue
        })

    df = pd.DataFrame(records)
    df = df.sort_values('date').reset_index(drop=True)
    df.to_csv('data/sales_data.csv', index=False)
    print(f"✅ Generated {len(df)} records with seasonality + growth trend")
    print(df.head())
    return df

if __name__ == '__main__':
    generate_sales_data()