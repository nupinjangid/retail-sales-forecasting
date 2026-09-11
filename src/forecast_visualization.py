import pandas as pd
import matplotlib.pyplot as plt

# Load historical sales
historical = pd.read_csv(
    "data/processed/monthly_sales.csv"
)

historical["Month"] = pd.to_datetime(
    historical["Month"]
)

# Load future forecast
forecast = pd.read_csv(
    "data/processed/sales_forecast.csv"
)

forecast["Month"] = pd.to_datetime(
    forecast["Month"]
)

# Create figure
plt.figure(figsize=(12, 6))

# Historical sales
plt.plot(
    historical["Month"],
    historical["Sales"],
    label="Historical Sales"
)

# Forecast
plt.plot(
    forecast["Month"],
    forecast["Forecast"],
    label="Forecast"
)

# Forecast uncertainty
plt.fill_between(
    forecast["Month"],
    forecast["Lower Bound"],
    forecast["Upper Bound"],
    alpha=0.2,
    label="Forecast Range"
)

# Add vertical line separating historical and forecast
plt.axvline(
    historical["Month"].max(),
    linestyle="--",
    label="Forecast Start"
)

plt.title("Retail Sales Forecast")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.grid(True)

plt.tight_layout()

# Save chart
plt.savefig(
    "screenshots/sales_forecast.png",
    dpi=150
)

plt.show()