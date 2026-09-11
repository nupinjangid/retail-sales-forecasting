import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="Retail Sales Forecasting",
    page_icon="📊",
    layout="wide"
)

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv(
    "data/raw/Superstore.csv",
    encoding="latin1"
)

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])

# ==============================
# SIDEBAR FILTERS
# ==============================

if st.sidebar.button("Reset Filters"):
    st.session_state["region_filter"] = sorted(df["Region"].unique())
    st.session_state["category_filter"] = sorted(df["Category"].unique())
    st.session_state["segment_filter"] = sorted(df["Segment"].unique())
    st.rerun()

st.sidebar.header("Dashboard Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique()),
    key="region_filter"
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique()),
    key="category_filter"
)

segment_filter = st.sidebar.multiselect(
    "Select Segment",
    options=sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique()),
    key="segment_filter"
)

# ==============================
# APPLY FILTERS
# ==============================

filtered_df = df[
    df["Region"].isin(region_filter)
    & df["Category"].isin(category_filter)
    & df["Segment"].isin(segment_filter)
]

# Load sales forecast
forecast = pd.read_csv(
    "data/processed/sales_forecast.csv"
)

forecast["Month"] = pd.to_datetime(
    forecast["Month"]
)

# ==============================
# CALCULATE KPIs
# ==============================

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

if total_sales != 0:
    profit_margin = (total_profit / total_sales) * 100
else:
    profit_margin = 0

total_orders = filtered_df["Order ID"].nunique()
average_discount = filtered_df["Discount"].mean() * 100

# ==============================
# PAGE TITLE
# ==============================

st.title("📊 Retail Sales Forecasting & Profitability Intelligence")

st.write(
    "Explore historical retail sales, forecast future demand, "
    "identify profitability drivers, and uncover loss-making products."
)

st.caption(
    "Use the filters in the sidebar to interactively explore the analysis."
)

# ==============================
# DATA COVERAGE
# ==============================

st.info(
    f"Data covers {df['Order Date'].min().strftime('%B %Y')} "
    f"to {df['Order Date'].max().strftime('%B %Y')} "
    f"with {len(df):,} sales records."
)

# ==============================
# DASHBOARD TABS
# ==============================

sales_tab, profitability_tab, recommendations_tab = st.tabs(
    [
        "📈 Sales & Forecast",
        "💰 Profitability",
        "💡 Recommendations"
    ]
)

# ==============================
# EXECUTIVE OVERVIEW
# ==============================

with sales_tab:

    st.header("Executive Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Total Profit", f"${total_profit:,.0f}")
    col3.metric("Profit Margin", f"{profit_margin:.2f}%")
    col4.metric("Total Orders", f"{total_orders:,}")
    col5.metric("Average Discount", f"{average_discount:.2f}%")

# ==============================
# HISTORICAL SALES TREND
# ==============================

with sales_tab:

    st.header("Historical Sales Trend")

    monthly_sales = (
        filtered_df.groupby(
            filtered_df["Order Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)
    monthly_sales["Order Date"] = pd.to_datetime(
        monthly_sales["Order Date"]
    )

    fig = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        title="Monthly Sales"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==============================
# SALES FORECAST
# ==============================

with sales_tab:

    st.header("6-Month Sales Forecast")

    forecast_total = forecast["Forecast"].sum()

    st.metric(
        "Forecasted Sales — Next 6 Months",
        f"${forecast_total:,.0f}"
    )

    st.caption(
        "The forecast shows expected monthly sales for the next 6 months. "
        "The shaded area represents the forecast uncertainty range."
    )

    # Recent historical sales
    historical_forecast = (
        df.groupby(
            df["Order Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    historical_forecast["Month"] = pd.to_datetime(
        historical_forecast["Order Date"].astype(str)
    )

    # Keep only the last 12 months
    historical_forecast = historical_forecast.tail(12)

    # Forecast data
    forecast_display = forecast.copy()

    # Create combined chart
    forecast_fig = px.line(
        historical_forecast,
        x="Month",
        y="Sales",
        title="Historical Sales and 6-Month Forecast"
    )

    # Add forecast line
    forecast_fig.add_scatter(
        x=forecast_display["Month"],
        y=forecast_display["Forecast"],
        mode="lines+markers",
        name="Forecast"
    )

    # Add upper bound
    forecast_fig.add_scatter(
        x=forecast_display["Month"],
        y=forecast_display["Upper Bound"],
        mode="lines",
        line=dict(width=0),
        showlegend=False
    )

    # Add lower bound
    forecast_fig.add_scatter(
        x=forecast_display["Month"],
        y=forecast_display["Lower Bound"],
        mode="lines",
        fill="tonexty",
        name="Forecast Range"
    )

    # Mark forecast starting point
    forecast_fig.add_vline(
        x=historical_forecast["Month"].max().timestamp() * 1000,
        line_dash="dash",
        annotation_text="Forecast Start"
    )

    forecast_fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales",
        hovermode="x unified"
    )

    st.plotly_chart(
        forecast_fig,
        use_container_width=True
    )

# ==============================
# PROFITABILITY ANALYSIS
# ==============================

with profitability_tab:

    st.header("Profitability Intelligence")

    # ==============================
    # SUB-CATEGORY PROFITABILITY
    # ==============================

    st.subheader("Profit by Sub-Category")

    subcategory_profitability = (
        filtered_df.groupby("Sub-Category")
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

    subcategory_fig = px.bar(
        subcategory_profitability.sort_values("Profit"),
        x="Profit",
        y="Sub-Category",
        orientation="h",
        title="Profit by Sub-Category"
    )

    subcategory_fig.update_layout(
        xaxis_title="Profit",
        yaxis_title="Sub-Category",
        hovermode="y unified"
    )

    st.plotly_chart(
        subcategory_fig,
        use_container_width=True
    )

    # ==============================
    # LOSS-MAKING PRODUCTS
    # ==============================

    st.subheader("Top 10 Loss-Making Products")

    product_profitability = (
        filtered_df.groupby("Product Name")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

    loss_products = (
        product_profitability[
            product_profitability["Profit"] < 0
        ]
        .sort_values("Profit")
        .head(10)
    )

    st.dataframe(
        loss_products,
        use_container_width=True
    )

    # ==============================
    # DISCOUNT VS PROFITABILITY
    # ==============================

    st.subheader("Discount vs Profitability")

    discount_analysis = (
        filtered_df.groupby("Discount")
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

    discount_fig = px.line(
        discount_analysis.sort_values("Discount"),
        x="Discount",
        y="Profit",
        markers=True,
        title="Discount vs Profit"
    )

    discount_fig.add_hline(
        y=0,
        line_dash="dash"
    )

    discount_fig.update_layout(
        xaxis_title="Discount",
        yaxis_title="Profit",
        hovermode="x unified"
    )

    st.plotly_chart(
        discount_fig,
        use_container_width=True
    )

# ==============================
# BUSINESS RECOMMENDATIONS
# ==============================

with recommendations_tab:

    st.header("Business Recommendations")

    st.markdown("""
    ### 📌 Key Recommendations

    **1. Control High Discounts**
    - Higher discount levels are associated with negative profitability.
    - Review discounts of 30% and above carefully.

    **2. Focus on High-Performing Categories**
    - Technology generates the highest overall profit.
    - Continue investing in strong technology sub-categories.

    **3. Review Loss-Making Sub-Categories**
    - Tables, Bookcases, and Supplies show negative profitability.
    - Review pricing, discounts, and product costs.

    **4. Investigate Loss-Making Products**
    - Some individual products generate significant losses.
    - Consider repricing, reducing discounts, or reviewing product costs.

    **5. Prepare for Seasonal Demand**
    - Historical sales show stronger performance toward the later months of the year.
    - Use the forecast to support inventory and sales planning.
    """)

# ==============================
# FOOTER
# ==============================

st.markdown("---")

st.caption(
    "Retail Sales Forecasting & Profitability Intelligence | "
    "Built with Python, Pandas, Plotly, Prophet & Streamlit"
)