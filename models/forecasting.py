import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import pickle
import os
from utils.db_connector import run_query

# ── 1. PREPARE DATA ─────────────────────────────────────────────
def prepare_forecast_data():
    query = """
        SELECT
            strftime('%Y-%m', date)     AS month,
            ROUND(SUM(revenue), 2)      AS monthly_revenue
        FROM sales
        GROUP BY month
        ORDER BY month ASC
    """
    df = run_query(query)

    # Drop last month (incomplete)
    df = df.iloc[:-1].reset_index(drop=True)

    df['month_index'] = range(len(df))
    df['month_num'] = pd.to_datetime(df['month']).dt.month
    df['year'] = pd.to_datetime(df['month']).dt.year

    # Seasonality
    df['sin_month'] = np.sin(2 * np.pi * df['month_num'] / 12)
    df['cos_month'] = np.cos(2 * np.pi * df['month_num'] / 12)

    # Lag features
    df['lag_1'] = df['monthly_revenue'].shift(1)
    df['lag_2'] = df['monthly_revenue'].shift(2)
    df['lag_12'] = df['monthly_revenue'].shift(12)  # same month last year

    # Rolling features
    df['rolling_3'] = df['monthly_revenue'].rolling(3).mean()
    df['rolling_6'] = df['monthly_revenue'].rolling(6).mean()

    df = df.dropna().reset_index(drop=True)

    return df


# ── 2. TRAIN MODEL ──────────────────────────────────────────────
def train_model():
    df = prepare_forecast_data()

    features = [
        'month_index', 'month_num', 'year',
        'sin_month', 'cos_month',
        'lag_1', 'lag_2', 'lag_12',
        'rolling_3', 'rolling_6'
    ]

    X = df[features]
    y = df['monthly_revenue']

    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
    model.fit(X, y)

    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    accuracy = round(r2 * 100, 2)

    print(f"✅ Model trained successfully")
    print(f"📊 R² Score: {r2:.4f} ({accuracy}% accuracy)")
    print(f"📊 MAE: ${mae:,.2f}")

    os.makedirs('models', exist_ok=True)
    with open('models/sales_forecast_model.pkl', 'wb') as f:
        pickle.dump((model, df), f)
    print("✅ Model saved to models/sales_forecast_model.pkl")

    return model, df, accuracy


# ── 3. FORECAST NEXT 6 MONTHS ───────────────────────────────────
def forecast_next_6_months():
    with open('models/sales_forecast_model.pkl', 'rb') as f:
        model, df = pickle.load(f)

    last_month = pd.to_datetime(df['month'].iloc[-1])
    last_index = df['month_index'].iloc[-1]

    # Keep a running history for lag features
    history = list(df['monthly_revenue'])

    forecasts = []
    for i in range(1, 7):
        next_month = last_month + pd.DateOffset(months=i)
        month_num = next_month.month

        lag_1 = history[-1]
        lag_2 = history[-2]
        lag_12 = history[-12] if len(history) >= 12 else np.mean(history)
        rolling_3 = np.mean(history[-3:])
        rolling_6 = np.mean(history[-6:])

        features = pd.DataFrame([{
            'month_index': last_index + i,
            'month_num': month_num,
            'year': next_month.year,
            'sin_month': np.sin(2 * np.pi * month_num / 12),
            'cos_month': np.cos(2 * np.pi * month_num / 12),
            'lag_1': lag_1,
            'lag_2': lag_2,
            'lag_12': lag_12,
            'rolling_3': rolling_3,
            'rolling_6': rolling_6
        }])

        predicted = max(0, model.predict(features)[0])
        forecasts.append({
            'month': next_month.strftime('%Y-%m'),
            'forecasted_revenue': round(predicted, 2)
        })
        history.append(predicted)

    return pd.DataFrame(forecasts)


# ── 4. GET ACTUAL VS PREDICTED ──────────────────────────────────
def get_actual_vs_predicted():
    with open('models/sales_forecast_model.pkl', 'rb') as f:
        model, df = pickle.load(f)

    features = [
        'month_index', 'month_num', 'year',
        'sin_month', 'cos_month',
        'lag_1', 'lag_2', 'lag_12',
        'rolling_3', 'rolling_6'
    ]
    df['predicted_revenue'] = model.predict(df[features])
    return df[['month', 'monthly_revenue', 'predicted_revenue']]


if __name__ == '__main__':
    print("Training model...")
    model, df, accuracy = train_model()

    print("\n📈 Next 6 Months Forecast:")
    print("=" * 40)
    forecast = forecast_next_6_months()
    print(forecast.to_string(index=False))

    print("\n📊 Actual vs Predicted (last 5 months):")
    print("=" * 40)
    avp = get_actual_vs_predicted()
    print(avp.tail().to_string(index=False))