import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 🔹 Step 1: Choose your products
products = ['iPhone 13', 'MacBook Air', 'Samsung Galaxy S23', 'Sony WH-1000XM5']

# 🔹 Step 2: Define the date range (last 6 months, weekly)
start_date = datetime(2024, 11, 1)
end_date = datetime(2025, 5, 21)
dates = pd.date_range(start=start_date, end=end_date, freq='W')  # 'W' = Weekly

# 🔹 Step 3: Function to simulate price trends
def generate_price_trend(base_price, num_points):
    trend = base_price + np.cumsum(np.random.normal(0, 5, num_points))  # Random price changes
    trend = np.clip(trend, base_price * 0.7, base_price * 1.1)  # Keep within ±30% of base price
    return trend.round(2)

# 🔹 Step 4: Build the dataset
data = []

for product in products:
    base_price = np.random.randint(400, 1500)  # Random base price between 400 and 1500
    price_trend = generate_price_trend(base_price, len(dates))
    
    for date, price in zip(dates, price_trend):
        data.append({
            "date": date,
            "product": product,
            "price": price
        })

# 🔹 Step 5: Create a DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv("synthetic_price_history.csv", index=False)

# 🔹 Step 6: Preview the data
print(df.describe())
