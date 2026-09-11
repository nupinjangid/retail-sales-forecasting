import pandas as pd
import matplotlib.pyplot as plt

# Load category profitability data
df = pd.read_csv(
    "data/processed/category_profitability.csv"
)

# Create figure
fig, ax1 = plt.subplots(figsize=(10, 6))

# Sales bars
ax1.bar(
    df["Category"],
    df["Sales"],
    label="Sales"
)

ax1.set_xlabel("Category")
ax1.set_ylabel("Sales")

# Profit line
ax2 = ax1.twinx()

ax2.plot(
    df["Category"],
    df["Profit"],
    marker="o",
    linewidth=2,
    label="Profit"
)

ax2.set_ylabel("Profit")

plt.title("Sales vs Profit by Category")

fig.tight_layout()

# Save chart
plt.savefig(
    "screenshots/category_sales_profit.png",
    dpi=150
)

plt.show()

# ==============================
# SUB-CATEGORY PROFITABILITY
# ==============================

# Load sub-category data
subcategory = pd.read_csv(
    "data/processed/subcategory_profitability.csv"
)

# Sort by profit
subcategory = subcategory.sort_values(
    "Profit"
)

# Create figure
plt.figure(figsize=(10, 7))

plt.barh(
    subcategory["Sub-Category"],
    subcategory["Profit"]
)

plt.title("Profit by Sub-Category")
plt.xlabel("Profit")
plt.ylabel("Sub-Category")

plt.grid(axis="x")

plt.tight_layout()

# Save chart
plt.savefig(
    "screenshots/subcategory_profitability.png",
    dpi=150
)

plt.show()

# ==============================
# DISCOUNT VS PROFITABILITY
# ==============================

# Load discount data
discount = pd.read_csv(
    "data/processed/discount_profitability.csv"
)

# Create figure
plt.figure(figsize=(10, 6))

plt.plot(
    discount["Discount"] * 100,
    discount["Profit"],
    marker="o",
    linewidth=2
)

plt.axhline(
    0,
    linestyle="--"
)

plt.title("Discount vs Profit")
plt.xlabel("Discount (%)")
plt.ylabel("Profit")

plt.grid(True)

plt.tight_layout()

# Save chart
plt.savefig(
    "screenshots/discount_profit.png",
    dpi=150
)

plt.show()