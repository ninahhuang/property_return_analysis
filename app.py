# Imports
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter

from calculations import project_property

# Configure the page
st.set_page_config(
    page_title="10-Year Property Return Analysis",
    page_icon="🏠",
    layout="wide",
)

st.title("10-Year Property Return Analysis")

st.caption(
    "Compare rental cash flow, appreciation, mortgage equity, "
    "sale proceeds, and total return for two Celina properties."
)

# Create the common sidebar inputs
st.sidebar.header("Shared Assumptions")

mortgage_rate = st.sidebar.number_input(
    "Mortgage rate (%)",
    min_value=0.0,
    max_value=20.0,
    value=6.8,
    step=0.1,
) / 100

mortgage_term_years = st.sidebar.number_input(
    "Mortgage term (years)",
    min_value=1,
    max_value=40,
    value=30,
    step=1,
)

holding_period_years = st.sidebar.number_input(
    "Holding period (years)",
    min_value=1,
    max_value=30,
    value=10,
    step=1,
)

annual_appreciation = st.sidebar.number_input(
    "Annual appreciation (%)",
    min_value=-10.0,
    max_value=20.0,
    value=3.0,
    step=0.1,
) / 100

annual_rent_growth = st.sidebar.number_input(
    "Annual rent growth (%)",
    min_value=-10.0,
    max_value=20.0,
    value=0.0,
    step=0.5,
) / 100

vacancy_rate = st.sidebar.number_input(
    "Vacancy rate (%)",
    min_value=0.0,
    max_value=50.0,
    value=5.0,
    step=0.5,
) / 100

property_tax_rate = st.sidebar.number_input(
    "Property-tax rate (%)",
    min_value=0.0,
    max_value=10.0,
    value=2.016,
    step=0.01,
) / 100

management_fee_rate = st.sidebar.number_input(
    "Management fee (%)",
    min_value=0.0,
    max_value=30.0,
    value=0.0,
    step=1.0,
) / 100

insurance_growth = st.sidebar.number_input(
    "Annual insurance growth (%)",
    min_value=0.0,
    max_value=20.0,
    value=0.0,
    step=0.5,
) / 100

buying_cost_rate = st.sidebar.number_input(
    "Buying costs (%)",
    min_value=0.0,
    max_value=10.0,
    value=2.0,
    step=0.5,
) / 100

selling_cost_rate = st.sidebar.number_input(
    "Selling costs (%)",
    min_value=0.0,
    max_value=15.0,
    value=7.0,
    step=0.5,
) / 100

# Add Property A inputs
st.sidebar.divider()
st.sidebar.subheader("Property A")

property_a_price = st.sidebar.number_input(
    "Purchase price — Property A",
    min_value=0,
    value=350_000,
    step=10_000,
)

property_a_down_payment = st.sidebar.number_input(
    "Down payment — Property A",
    min_value=0,
    value=250_000,
    step=10_000,
)

property_a_monthly_rent = st.sidebar.number_input(
    "Monthly rent — Property A",
    min_value=0,
    value=2_500,
    step=100,
)

property_a_insurance = st.sidebar.number_input(
    "Annual insurance — Property A",
    min_value=0,
    value=3_500,
    step=100,
)

property_a_maintenance = st.sidebar.number_input(
    "Annual maintenance — Property A",
    min_value=0,
    value=3_500,
    step=100,
)

property_a_monthly_hoa = st.sidebar.number_input(
    "Monthly HOA — Property A",
    min_value=0,
    value=0,
    step=25,
)

# Add Property B inputs
st.sidebar.divider()
st.sidebar.subheader("Property B")

property_b_price = st.sidebar.number_input(
    "Purchase price — Property B",
    min_value=0,
    value=550_000,
    step=10_000,
)

property_b_down_payment = st.sidebar.number_input(
    "Down payment — Property B",
    min_value=0,
    value=250_000,
    step=10_000,
)

property_b_monthly_rent = st.sidebar.number_input(
    "Monthly rent — Property B",
    min_value=0,
    value=3_500,
    step=100,
)

property_b_insurance = st.sidebar.number_input(
    "Annual insurance — Property B",
    min_value=0,
    value=5_500,
    step=100,
)

property_b_maintenance = st.sidebar.number_input(
    "Annual maintenance — Property B",
    min_value=0,
    value=5_500,
    step=100,
)

property_b_monthly_hoa = st.sidebar.number_input(
    "Monthly HOA — Property B",
    min_value=0,
    value=0,
    step=25,
)

# Validate the inputs
if property_a_down_payment > property_a_price:
    st.error(
        "Property A down payment cannot exceed its purchase price."
    )
    st.stop()

if property_b_down_payment > property_b_price:
    st.error(
        "Property B down payment cannot exceed its purchase price."
    )
    st.stop()

# Build the assumption dictionaries
common_assumptions = {
    "location": "Celina, TX",
    "mortgage_rate": mortgage_rate,
    "mortgage_term_years": mortgage_term_years,
    "holding_period_years": holding_period_years,
    "annual_rent_growth": annual_rent_growth,
    "vacancy_rate": vacancy_rate,
    "property_tax_rate": property_tax_rate,
    "management_fee_rate": management_fee_rate,
    "annual_appreciation": annual_appreciation,
    "buying_cost_rate": buying_cost_rate,
    "selling_cost_rate": selling_cost_rate,
    "initial_renovation_cost": 0,
    "annual_insurance_growth": insurance_growth,
}


property_a = {
    **common_assumptions,
    "property_name": "Property A",
    "purchase_price": property_a_price,
    "down_payment": property_a_down_payment,
    "monthly_rent": property_a_monthly_rent,
    "annual_insurance": property_a_insurance,
    "annual_maintenance": property_a_maintenance,
    "monthly_hoa": property_a_monthly_hoa,
}


property_b = {
    **common_assumptions,
    "property_name": "Property B",
    "purchase_price": property_b_price,
    "down_payment": property_b_down_payment,
    "monthly_rent": property_b_monthly_rent,
    "annual_insurance": property_b_insurance,
    "annual_maintenance": property_b_maintenance,
    "monthly_hoa": property_b_monthly_hoa,
}


property_a_projection, property_a_summary = project_property(
    property_a
)

property_b_projection, property_b_summary = project_property(
    property_b
)

combined_projection = pd.concat(
    [
        property_a_projection,
        property_b_projection,
    ],
    ignore_index=True,
)

# Run the model
property_a_projection, property_a_summary = project_property(
    property_a
)

property_b_projection, property_b_summary = project_property(
    property_b
)

combined_projection = pd.concat(
    [
        property_a_projection,
        property_b_projection,
    ],
    ignore_index=True,
)

# Create headline results
profit_difference = (
    property_b_summary["Total Profit"]
    - property_a_summary["Total Profit"]
)

better_property = (
    "Property B"
    if profit_difference > 0
    else "Property A"
)

st.subheader("Investment Summary")

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

metric_1.metric(
    "Property A Total Profit",
    f"${property_a_summary['Total Profit']:,.0f}",
)

metric_2.metric(
    "Property B Total Profit",
    f"${property_b_summary['Total Profit']:,.0f}",
)

metric_3.metric(
    "Profit Difference",
    f"${abs(profit_difference):,.0f}",
    delta=f"{better_property} advantage",
    delta_color="off",
)

metric_4.metric(
    "Higher Total Profit",
    better_property,
)

st.info(
    f"At {annual_appreciation:.1%} annual appreciation, "
    f"{better_property} produces approximately "
    f"${abs(profit_difference):,.0f} more total profit "
    f"over {holding_period_years} years."
)

# Add the comparison table
comparison_table = pd.DataFrame({
    "Metric": [
        "Purchase Price",
        "Initial Cash Investment",
        "Monthly Mortgage Payment",
        "Year 1 Cash Flow",
        "Cumulative Cash Flow",
        "Projected Sale Price",
        "Selling Costs",
        "Remaining Mortgage",
        "Net Sale Proceeds",
        "Total Profit",
        "Total Return",
        "Simplified Annualized Return",
    ],
    "Property A": [
        property_a_summary["Purchase Price"],
        property_a_summary["Initial Cash Investment"],
        property_a_summary["Monthly Mortgage Payment"],
        property_a_summary["Year 1 Cash Flow"],
        property_a_summary["Cumulative Cash Flow"],
        property_a_summary["Projected Sale Price"],
        property_a_summary["Selling Costs"],
        property_a_summary["Remaining Mortgage"],
        property_a_summary["Net Sale Proceeds"],
        property_a_summary["Total Profit"],
        property_a_summary["Total Return"],
        property_a_summary["Simplified Annualized Return"],
    ],
    "Property B": [
        property_b_summary["Purchase Price"],
        property_b_summary["Initial Cash Investment"],
        property_b_summary["Monthly Mortgage Payment"],
        property_b_summary["Year 1 Cash Flow"],
        property_b_summary["Cumulative Cash Flow"],
        property_b_summary["Projected Sale Price"],
        property_b_summary["Selling Costs"],
        property_b_summary["Remaining Mortgage"],
        property_b_summary["Net Sale Proceeds"],
        property_b_summary["Total Profit"],
        property_b_summary["Total Return"],
        property_b_summary["Simplified Annualized Return"],
    ],
})

comparison_table["B Minus A"] = (
    comparison_table["Property B"]
    - comparison_table["Property A"]
)

st.subheader("Detailed Comparison")
st.dataframe(
    comparison_table,
    use_container_width=True,
    hide_index=True,
)

# Create the chart helper
property_colors = {
    "Property A": "#2563EB",
    "Property B": "#F59E0B",
}


def currency_axis(value, position):
    return f"${value:,.0f}"


currency_formatter = FuncFormatter(currency_axis)


def create_projection_chart(
    data,
    y_column,
    title,
    y_label,
):
    fig, ax = plt.subplots(figsize=(10, 5))

    for property_name, property_data in data.groupby(
        "Property"
    ):
        ax.plot(
            property_data["Year"],
            property_data[y_column],
            marker="o",
            linewidth=2.5,
            markersize=5,
            label=property_name,
            color=property_colors[property_name],
        )

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("Year")
    ax.set_ylabel(y_label)
    ax.set_xticks(
        range(
            1,
            int(holding_period_years) + 1,
        )
    )
    ax.yaxis.set_major_formatter(currency_formatter)
    ax.grid(axis="y", alpha=0.3)
    ax.legend()

    fig.tight_layout()
    return fig

# Add the first three charts
st.subheader("Annual Projections")

chart_column_1, chart_column_2 = st.columns(2)

with chart_column_1:
    cash_flow_figure = create_projection_chart(
        combined_projection,
        "Annual Cash Flow",
        "Annual Cash Flow",
        "Cash Flow",
    )

    st.pyplot(
        cash_flow_figure,
        use_container_width=True,
    )

    plt.close(cash_flow_figure)

with chart_column_2:
    property_value_figure = create_projection_chart(
        combined_projection,
        "Ending Property Value",
        "Projected Property Value",
        "Property Value",
    )

    st.pyplot(
        property_value_figure,
        use_container_width=True,
    )

    plt.close(property_value_figure)

mortgage_figure = create_projection_chart(
    combined_projection,
    "Ending Mortgage Balance",
    "Remaining Mortgage Balance",
    "Mortgage Balance",
)

st.pyplot(
    mortgage_figure,
    use_container_width=True,
)

plt.close(mortgage_figure)

# Add the annual projection tables
with st.expander("View annual projection tables"):
    property_a_tab, property_b_tab = st.tabs(
        ["Property A", "Property B"]
    )

    with property_a_tab:
        st.dataframe(
            property_a_projection,
            use_container_width=True,
            hide_index=True,
        )

    with property_b_tab:
        st.dataframe(
            property_b_projection,
            use_container_width=True,
            hide_index=True,
        )

