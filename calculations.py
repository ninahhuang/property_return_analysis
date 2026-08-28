import numpy_financial as npf
import pandas as pd

# Calculate mortgage balance by property
def calculate_mortgage_balance(
    mortgage_amount,
    annual_mortgage_rate,
    mortgage_term_years,
    payments_made,
):
    monthly_rate = annual_mortgage_rate / 12

    monthly_payment = -npf.pmt(
        monthly_rate,
        mortgage_term_years * 12,
        mortgage_amount,
    )

    remaining_balance = -npf.fv(
        monthly_rate,
        payments_made,
        -monthly_payment,
        mortgage_amount,
    )

    return max(float(remaining_balance), 0.0)

# Project property assumptions
def project_property(assumptions):
    property_name = assumptions["property_name"]
    purchase_price = assumptions["purchase_price"]
    down_payment = assumptions["down_payment"]

    mortgage_amount = purchase_price - down_payment
    monthly_rate = assumptions["mortgage_rate"] / 12
    total_mortgage_payments = assumptions["mortgage_term_years"] * 12

    monthly_mortgage_payment = -npf.pmt(
        monthly_rate,
        total_mortgage_payments,
        mortgage_amount,
    )

    annual_mortgage_payment = monthly_mortgage_payment * 12

    initial_cash_investment = (
        down_payment
        + purchase_price * assumptions["buying_cost_rate"]
        + assumptions["initial_renovation_cost"]
    )

    annual_records = []
    beginning_property_value = purchase_price

    for year in range(1, assumptions["holding_period_years"] + 1):
        monthly_rent = (
            assumptions["monthly_rent"]
            * (1 + assumptions["annual_rent_growth"]) ** (year - 1)
        )

        scheduled_rent = monthly_rent * 12
        vacancy_loss = scheduled_rent * assumptions["vacancy_rate"]
        collected_rent = scheduled_rent - vacancy_loss

        property_tax = (
            beginning_property_value
            * assumptions["property_tax_rate"]
        )

        insurance = (
            assumptions["annual_insurance"]
            * (1 + assumptions["annual_insurance_growth"]) ** (year - 1)
        )

        maintenance = assumptions["annual_maintenance"]
        hoa = assumptions["monthly_hoa"] * 12
        management_fee = (
            collected_rent
            * assumptions["management_fee_rate"]
        )

        total_operating_expenses = (
            property_tax
            + insurance
            + maintenance
            + hoa
            + management_fee
        )

        noi = collected_rent - total_operating_expenses
        annual_cash_flow = noi - annual_mortgage_payment

        ending_property_value = (
            beginning_property_value
            * (1 + assumptions["annual_appreciation"])
        )

        payments_made = year * 12

        ending_mortgage_balance = calculate_mortgage_balance(
            mortgage_amount=mortgage_amount,
            annual_mortgage_rate=assumptions["mortgage_rate"],
            mortgage_term_years=assumptions["mortgage_term_years"],
            payments_made=payments_made,
        )

        ending_equity = (
            ending_property_value
            - ending_mortgage_balance
        )

        annual_records.append({
            "Property": property_name,
            "Year": year,
            "Beginning Property Value": beginning_property_value,
            "Monthly Rent": monthly_rent,
            "Scheduled Rent": scheduled_rent,
            "Vacancy Loss": vacancy_loss,
            "Collected Rent": collected_rent,
            "Property Tax": property_tax,
            "Insurance": insurance,
            "Maintenance": maintenance,
            "HOA": hoa,
            "Management Fee": management_fee,
            "Total Operating Expenses": total_operating_expenses,
            "NOI": noi,
            "Mortgage Payments": annual_mortgage_payment,
            "Annual Cash Flow": annual_cash_flow,
            "Ending Property Value": ending_property_value,
            "Ending Mortgage Balance": ending_mortgage_balance,
            "Ending Equity": ending_equity,
        })

        beginning_property_value = ending_property_value

    annual_projection = pd.DataFrame(annual_records)

    projected_sale_price = annual_projection.iloc[-1][
        "Ending Property Value"
    ]

    remaining_mortgage = annual_projection.iloc[-1][
        "Ending Mortgage Balance"
    ]

    selling_costs = (
        projected_sale_price
        * assumptions["selling_cost_rate"]
    )

    net_sale_proceeds = (
        projected_sale_price
        - selling_costs
        - remaining_mortgage
    )

    cumulative_cash_flow = annual_projection[
        "Annual Cash Flow"
    ].sum()

    total_profit = (
        cumulative_cash_flow
        + net_sale_proceeds
        - initial_cash_investment
    )

    total_return = total_profit / initial_cash_investment

    simplified_annualized_return = (
        (1 + total_return)
        ** (1 / assumptions["holding_period_years"])
        - 1
    )

    summary = {
        "Property": property_name,
        "Purchase Price": purchase_price,
        "Down Payment": down_payment,
        "Mortgage Amount": mortgage_amount,
        "Monthly Mortgage Payment": monthly_mortgage_payment,
        "Initial Cash Investment": initial_cash_investment,
        "Year 1 Cash Flow": annual_projection.iloc[0][
            "Annual Cash Flow"
        ],
        "Cumulative Cash Flow": cumulative_cash_flow,
        "Projected Sale Price": projected_sale_price,
        "Selling Costs": selling_costs,
        "Remaining Mortgage": remaining_mortgage,
        "Net Sale Proceeds": net_sale_proceeds,
        "Total Profit": total_profit,
        "Total Return": total_return,
        "Simplified Annualized Return": simplified_annualized_return,
    }

    return annual_projection, summary

