import pandas as pd
from prophet import Prophet

# Load monthly sales data
df = pd.read_csv(
    "data/processed/monthly_sales.csv"
)

# Convert Month to datetime
df["Month"] = pd.to_datetime(df["Month"])

# Split data
train = df[df["Month"] < "2017-07-01"]
test = df[df["Month"] >= "2017-07-01"]

# Prophet requires columns named 'ds' and 'y'
prophet_train = train.rename(
    columns={
        "Month": "ds",
        "Sales": "y"
    }
)

# Create Prophet model
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False
)

# Train model
model.fit(prophet_train)

# Create future dates for the 6 test months
future = model.make_future_dataframe(
    periods=6,
    freq="MS"
)

# Generate forecast
forecast = model.predict(future)

# Display forecast for test period
test_forecast = forecast[
    forecast["ds"] >= "2017-07-01"
][
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
]

print("===== FORECAST FOR TEST PERIOD =====")
print(test_forecast)

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Combine actual sales with forecast
evaluation = test.merge(
    test_forecast,
    left_on="Month",
    right_on="ds"
)

# Calculate MAE
mae = mean_absolute_error(
    evaluation["Sales"],
    evaluation["yhat"]
)

# Calculate RMSE
rmse = np.sqrt(
    mean_squared_error(
        evaluation["Sales"],
        evaluation["yhat"]
    )
)

print("\n===== MODEL EVALUATION =====")

print(f"MAE: ${mae:,.2f}")
print(f"RMSE: ${rmse:,.2f}")

# ==============================
# NAIVE FORECAST
# ==============================

# Create naive predictions
naive_predictions = test.copy()

# Previous month's actual sales
naive_predictions["Naive Forecast"] = (
    df["Sales"]
    .shift(1)
    .loc[test.index]
)

# Calculate Naive MAE
naive_mae = mean_absolute_error(
    naive_predictions["Sales"],
    naive_predictions["Naive Forecast"]
)

# Calculate Naive RMSE
naive_rmse = np.sqrt(
    mean_squared_error(
        naive_predictions["Sales"],
        naive_predictions["Naive Forecast"]
    )
)

print("\n===== NAIVE FORECAST EVALUATION =====")

print(f"Naive MAE: ${naive_mae:,.2f}")
print(f"Naive RMSE: ${naive_rmse:,.2f}")

import matplotlib.pyplot as plt

# Plot actual vs forecast
plt.figure(figsize=(12, 6))

# Actual sales
plt.plot(
    df["Month"],
    df["Sales"],
    label="Actual Sales"
)

# Forecast
plt.plot(
    forecast["ds"],
    forecast["yhat"],
    label="Forecast"
)

# Uncertainty interval
plt.fill_between(
    forecast["ds"],
    forecast["yhat_lower"],
    forecast["yhat_upper"],
    alpha=0.2,
    label="Forecast Range"
)

plt.title("Monthly Sales: Actual vs Forecast")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "screenshots/actual_vs_forecast.png",
    dpi=150
)

plt.show()

# ==============================
# FINAL FORECAST
# ==============================

# Prepare all historical data for Prophet
final_train = df.rename(
    columns={
        "Month": "ds",
        "Sales": "y"
    }
)

# Create final Prophet model
final_model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False
)

# Train using all 48 months
final_model.fit(final_train)

# Create dates for the next 6 months
future_final = final_model.make_future_dataframe(
    periods=6,
    freq="MS"
)

# Generate final forecast
final_forecast = final_model.predict(
    future_final
)

# Keep only the future 6 months
future_forecast = final_forecast[
    final_forecast["ds"] > df["Month"].max()
][
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
]

# Rename columns
future_forecast.columns = [
    "Month",
    "Forecast",
    "Lower Bound",
    "Upper Bound"
]

print("\n===== FINAL 6-MONTH FORECAST =====")
print(future_forecast)

# Save forecast
future_forecast.to_csv(
    "data/processed/sales_forecast.csv",
    index=False
)

print("\nFinal forecast saved successfully!")