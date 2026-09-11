import pandas as pd

# Load raw data
df = pd.read_csv(
    "data/raw/Superstore.csv",
    encoding="latin1"
)

# Calculate profit margin
df["Profit Margin"] = (
    df["Profit"] / df["Sales"]
) * 100

# ==============================
# CATEGORY PROFITABILITY
# ==============================

category_profitability = (
    df.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

category_profitability["Profit Margin"] = (
    category_profitability["Profit"]
    / category_profitability["Sales"]
) * 100

category_profitability = category_profitability.sort_values(
    "Profit",
    ascending=False
)

print("===== CATEGORY PROFITABILITY =====")
print(category_profitability)


# ==============================
# SUB-CATEGORY PROFITABILITY
# ==============================

subcategory_profitability = (
    df.groupby("Sub-Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

subcategory_profitability["Profit Margin"] = (
    subcategory_profitability["Profit"]
    / subcategory_profitability["Sales"]
) * 100

subcategory_profitability = subcategory_profitability.sort_values(
    "Profit",
    ascending=False
)

print("\n===== SUB-CATEGORY PROFITABILITY =====")
print(subcategory_profitability)


# ==============================
# LOSS-MAKING PRODUCTS
# ==============================

product_profitability = (
    df.groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

loss_products = product_profitability[
    product_profitability["Profit"] < 0
].sort_values(
    "Profit"
)

print("\n===== TOP 10 LOSS-MAKING PRODUCTS =====")
print(loss_products.head(10))


# ==============================
# DISCOUNT ANALYSIS
# ==============================

discount_analysis = (
    df.groupby("Discount")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

discount_analysis["Profit Margin"] = (
    discount_analysis["Profit"]
    / discount_analysis["Sales"]
) * 100

print("\n===== DISCOUNT VS PROFITABILITY =====")
print(discount_analysis)

# ==============================
# SAVE PROCESSED DATASETS
# ==============================

category_profitability.to_csv(
    "data/processed/category_profitability.csv",
    index=False
)

subcategory_profitability.to_csv(
    "data/processed/subcategory_profitability.csv",
    index=False
)

loss_products.to_csv(
    "data/processed/loss_making_products.csv",
    index=False
)

discount_analysis.to_csv(
    "data/processed/discount_profitability.csv",
    index=False
)

print("\n===== FILES SAVED SUCCESSFULLY =====")
print("Category profitability saved.")
print("Sub-category profitability saved.")
print("Loss-making products saved.")
print("Discount profitability saved.")