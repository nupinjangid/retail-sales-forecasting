import pandas as pd

# Load raw data
df = pd.read_csv(
    "data/raw/Superstore.csv",
    encoding="latin1"
)

# Convert Order Date to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Sort by date
df = df.sort_values("Order Date")

# Create monthly sales
monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

# Convert period to timestamp
monthly_sales["Order Date"] = monthly_sales["Order Date"].dt.to_timestamp()

# Rename columns
monthly_sales.columns = ["Month", "Sales"]

# Save processed dataset
monthly_sales.to_csv(
    "data/processed/monthly_sales.csv",
    index=False
)

print("===== DATA PREPARATION COMPLETE =====")

print("Number of months:", len(monthly_sales))

print(
    "Date range:",
    monthly_sales["Month"].min().date(),
    "to",
    monthly_sales["Month"].max().date()
)

print("\nProcessed dataset:")
print(monthly_sales)

print("\nMonthly sales dataset saved successfully!")
