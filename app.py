# Imports
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter

from calculations import (
    calculate_break_even_appreciation,
    create_appreciation_scenarios,
    project_property,
)

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
    min_value=0.00,
    value=350_000.00,
    step=10_000.00,
    format="%.2f",
)

property_a_down_payment = st.sidebar.number_input(
    "Down payment — Property A",
    min_value=0.00,
    value=250_000.00,
    step=10_000.00,
    format="%.2f",
)

property_a_monthly_rent = st.sidebar.number_input(
    "Monthly rent — Property A",
    min_value=0.00,
    value=2_500.00,
    step=100.00,
    format="%.2f",
)

property_a_insurance = st.sidebar.number_input(
    "Annual insurance — Property A",
    min_value=0.00,
    value=3_500.00,
    step=100.00,
    format="%.2f",
)

property_a_maintenance = st.sidebar.number_input(
    "Annual maintenance — Property A",
    min_value=0.00,
    value=3_500.00,
    step=100.00,
    format="%.2f",
)

property_a_monthly_hoa = st.sidebar.number_input(
    "Monthly HOA — Property A",
    min_value=0.00,
    value=0.00,
    step=25.00,
    format="%.2f",
)

# Add Property B inputs
st.sidebar.divider()
st.sidebar.subheader("Property B")

property_b_price = st.sidebar.number_input(
    "Purchase price — Property B",
    min_value=0.00,
    value=550_000.00,
    step=10_000.00,
    format="%.2f",
)

property_b_down_payment = st.sidebar.number_input(
    "Down payment — Property B",
    min_value=0.00,
    value=250_000.00,
    step=10_000.00,
    format="%.2f",
)

property_b_monthly_rent = st.sidebar.number_input(
    "Monthly rent — Property B",
    min_value=0.00,
    value=3_500.00,
    step=100.00,
    format="%.2f",
)

property_b_insurance = st.sidebar.number_input(
    "Annual insurance — Property B",
    min_value=0.00,
    value=5_500.00,
    step=100.00,
    format="%.2f",
)

property_b_maintenance = st.sidebar.number_input(
    "Annual maintenance — Property B",
    min_value=0.00,
    value=5_500.00,
    step=100.00,
    format="%.2f",
)

property_b_monthly_hoa = st.sidebar.number_input(
    "Monthly HOA — Property B",
    min_value=0.00,
    value=0.00,
    step=25.00,
    format="%.2f",
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

# Scenarios
break_even_appreciation = (
    calculate_break_even_appreciation(
        property_a,
        property_b,
    )
)

appreciation_scenarios = (
    create_appreciation_scenarios(
        property_a,
        property_b,
        minimum_rate=0.00,
        maximum_rate=0.10,
        step=0.005,
    )
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
    f"${property_a_summary['Total Profit']:,.2f}",
)

metric_2.metric(
    "Property B Total Profit",
    f"${property_b_summary['Total Profit']:,.2f}",
)

metric_3.metric(
    "Profit Difference",
    f"${abs(profit_difference):,.2f}",
    delta=f"{better_property} advantage",
    delta_color="off",
)

metric_4.metric(
    "Higher Total Profit",
    better_property,
)

st.info(
    f"At {annual_appreciation:.2%} annual appreciation, "
    f"{better_property} produces approximately "
    f"${abs(profit_difference):,.2f} more total profit "
    f"over {holding_period_years} years."
)

def format_currency(value):
    if value < 0:
        return f"-${abs(value):,.2f}"

    return f"${value:,.2f}"

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

currency_metrics = {
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
}

percentage_metrics = {
    "Total Return",
    "Simplified Annualized Return",
}

formatted_comparison = comparison_table.copy()

display_value_columns = [
    "Property A",
    "Property B",
    "B Minus A",
]

formatted_comparison[
    display_value_columns
] = formatted_comparison[
    display_value_columns
].astype(object)

for row_index, row in formatted_comparison.iterrows():
    metric = row["Metric"]

    if metric in currency_metrics:
        formatted_comparison.loc[
            row_index,
            ["Property A", "Property B", "B Minus A"],
        ] = [
            format_currency(row["Property A"]),
            format_currency(row["Property B"]),
            format_currency(row["B Minus A"]),
        ]

    elif metric in percentage_metrics:
        formatted_comparison.loc[
            row_index,
            ["Property A", "Property B", "B Minus A"],
        ] = [
            f"{row['Property A']:.2%}",
            f"{row['Property B']:.2%}",
            f"{row['B Minus A']:.2%}",
        ]

st.subheader("Detailed Comparison")

st.dataframe(
    formatted_comparison,
    use_container_width=True,
    hide_index=True,
)

# Create the chart helper
property_colors = {
    "Property A": "#2563EB",
    "Property B": "#F59E0B",
}


def currency_axis(value, position):
    return f"${value:,.2f}"


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

# Create appreciation chart
def create_appreciation_chart(
    scenario_data,
    break_even_rate,
    property_a,
    property_b,
):
    fig, ax = plt.subplots(figsize=(11, 6))

    ax.plot(
        scenario_data["Appreciation Rate"],
        scenario_data["Property A Total Profit"],
        marker="o",
        markersize=4,
        linewidth=2.5,
        label="Property A",
        color=property_colors["Property A"],
    )

    ax.plot(
        scenario_data["Appreciation Rate"],
        scenario_data["Property B Total Profit"],
        marker="o",
        markersize=4,
        linewidth=2.5,
        label="Property B",
        color=property_colors["Property B"],
    )

    if break_even_rate is not None:
        break_even_property_a = {
            **property_a,
            "annual_appreciation": break_even_rate,
        }

        break_even_property_b = {
            **property_b,
            "annual_appreciation": break_even_rate,
        }

        _, break_even_summary_a = project_property(
            break_even_property_a
        )

        _, break_even_summary_b = project_property(
            break_even_property_b
        )

        break_even_profit = (
            break_even_summary_a["Total Profit"]
            + break_even_summary_b["Total Profit"]
        ) / 2

        ax.scatter(
            break_even_rate,
            break_even_profit,
            s=110,
            color="#DC2626",
            edgecolor="white",
            linewidth=1.5,
            zorder=5,
        )

        ax.axvline(
            x=break_even_rate,
            color="#DC2626",
            linestyle="--",
            linewidth=1.2,
            alpha=0.7,
        )

        ax.annotate(
            f"Break-even: {break_even_rate:.2%}",
            xy=(
                break_even_rate,
                break_even_profit,
            ),
            xytext=(14, 18),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
            color="#991B1B",
            bbox={
                "boxstyle": "round,pad=0.3",
                "facecolor": "white",
                "edgecolor": "#DC2626",
                "alpha": 0.95,
            },
            arrowprops={
                "arrowstyle": "->",
                "color": "#DC2626",
                "linewidth": 1,
            },
        )

    ax.axhline(
        y=0,
        color="black",
        linewidth=1,
    )

    ax.set_title(
        "10-Year Total Profit by Appreciation Rate",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("Annual Appreciation Rate")
    ax.set_ylabel("10-Year Total Profit")

    ax.xaxis.set_major_formatter(
        FuncFormatter(
            lambda value, position: f"{value:.2%}"
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

st.divider()
st.subheader("Appreciation and Break-Even Analysis")

st.caption(
    "Both properties are assigned the same appreciation rate. "
    "The break-even rate is where their 10-year total profits "
    "are equal."
)

current_profit_difference = (
    property_b_summary["Total Profit"]
    - property_a_summary["Total Profit"]
)

current_winner = (
    "Property B"
    if current_profit_difference > 0
    else "Property A"
)

break_even_column, current_column, margin_column = (
    st.columns(3)
)

if break_even_appreciation is not None:
    break_even_column.metric(
        "Break-Even Appreciation",
        f"{break_even_appreciation:.2%}",
    )

    appreciation_margin = (
        annual_appreciation
        - break_even_appreciation
    )

    margin_column.metric(
        "Current Rate vs. Break-Even",
        f"{appreciation_margin:+.2%}",
    )

else:
    break_even_column.metric(
        "Break-Even Appreciation",
        "No crossover",
    )

    margin_column.metric(
        "Current Rate vs. Break-Even",
        "N/A",
    )

current_column.metric(
    "Winner at Current Rate",
    current_winner,
)

# Display the chart
appreciation_figure = create_appreciation_chart(
    appreciation_scenarios,
    break_even_appreciation,
    property_a,
    property_b,
)

st.pyplot(
    appreciation_figure,
    use_container_width=True,
)

plt.close(appreciation_figure)

# Add interpretation message
if break_even_appreciation is None:
    st.warning(
        "No break-even appreciation rate was found between "
        "0% and 20% under the current assumptions."
    )

elif annual_appreciation < break_even_appreciation:
    st.info(
        f"At {annual_appreciation:.2%} appreciation, "
        f"Property A produces more total profit. "
        f"Property B requires appreciation above approximately "
        f"{break_even_appreciation:.2%} to become the stronger "
        f"investment."
    )

else:
    st.success(
        f"At {annual_appreciation:.2%} appreciation, "
        f"Property B produces more total profit because the "
        f"assumed rate exceeds the {break_even_appreciation:.2%} "
        f"break-even threshold."
    )

# Add bounded scenario table
scenario_display = appreciation_scenarios.copy()

scenario_display["Appreciation Rate"] = (
    scenario_display["Appreciation Rate"]
    .map(lambda value: f"{value:.2%}")
)

for column in [
    "Property A Total Profit",
    "Property B Total Profit",
    "B Minus A",
]:
    scenario_display[column] = (
        scenario_display[column]
        .map(lambda value: f"${value:,.2f}")
    )

with st.expander("View appreciation scenario table"):
    st.dataframe(
        scenario_display,
        use_container_width=True,
        hide_index=True,
    )

# Create copies
property_a_projection_display = (
    property_a_projection.copy()
)

property_b_projection_display = (
    property_b_projection.copy()
)

numeric_columns_a = (
    property_a_projection_display
    .select_dtypes(include="number")
    .columns
)

numeric_columns_b = (
    property_b_projection_display
    .select_dtypes(include="number")
    .columns
)

property_a_projection_display[
    numeric_columns_a
] = property_a_projection_display[
    numeric_columns_a
].round(2)

property_b_projection_display[
    numeric_columns_b
] = property_b_projection_display[
    numeric_columns_b
].round(2)

# Add the annual projection tables
with st.expander("View annual projection tables"):
    property_a_tab, property_b_tab = st.tabs(
        ["Property A", "Property B"]
    )

    with property_a_tab:
        st.dataframe(
            property_a_projection_display,
            use_container_width=True,
            hide_index=True,
        )

    with property_b_tab:
        st.dataframe(
            property_b_projection_display,
            use_container_width=True,
            hide_index=True,
        )
