import copy


import numpy_financial as npf
import pandas as pd
import numpy as np
import numpy_financial as npf
import pandas as pd

from scipy.optimize import brentq


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

def calculate_profit_difference(
    appreciation_rate,
    property_a,
    property_b,
):
    scenario_a = copy.deepcopy(property_a)
    scenario_b = copy.deepcopy(property_b)

    scenario_a["annual_appreciation"] = appreciation_rate
    scenario_b["annual_appreciation"] = appreciation_rate

    _, summary_a = project_property(scenario_a)
    _, summary_b = project_property(scenario_b)

    return (
        summary_b["Total Profit"]
        - summary_a["Total Profit"]
    )

def calculate_break_even_appreciation(
    property_a,
    property_b,
    lower_bound=0.00,
    upper_bound=0.20,
):
    def profit_difference(appreciation_rate):
        return calculate_profit_difference(
            appreciation_rate,
            property_a,
            property_b,
        )

    lower_difference = profit_difference(lower_bound)
    upper_difference = profit_difference(upper_bound)

    if lower_difference == 0:
        return lower_bound

    if upper_difference == 0:
        return upper_bound

    if lower_difference * upper_difference > 0:
        return None

    return brentq(
        profit_difference,
        lower_bound,
        upper_bound,
    )

def create_appreciation_scenarios(
    property_a,
    property_b,
    minimum_rate=0.00,
    maximum_rate=0.10,
    step=0.005,
):
    scenario_rates = np.arange(
        minimum_rate,
        maximum_rate + step / 2,
        step,
    )

    scenario_records = []

    for appreciation_rate in scenario_rates:
        scenario_a = copy.deepcopy(property_a)
        scenario_b = copy.deepcopy(property_b)

        scenario_a[
            "annual_appreciation"
        ] = appreciation_rate

        scenario_b[
            "annual_appreciation"
        ] = appreciation_rate

        _, summary_a = project_property(scenario_a)
        _, summary_b = project_property(scenario_b)

        profit_difference = (
            summary_b["Total Profit"]
            - summary_a["Total Profit"]
        )

        scenario_records.append({
            "Appreciation Rate": appreciation_rate,
            "Property A Total Profit": summary_a["Total Profit"],
            "Property B Total Profit": summary_b["Total Profit"],
            "B Minus A": profit_difference,
            "Better Property": (
                "Property B"
                if profit_difference > 0
                else "Property A"
            ),
        })

    return pd.DataFrame(scenario_records)

def run_operating_sensitivity(
    property_a,
    property_b,
    annual_rent_growth,
    vacancy_rate,
    management_fee_rate,
    annual_insurance_growth,
):
    """
    Run both properties using the selected operating assumptions
    without modifying the original property dictionaries.
    """
    sensitivity_a = property_a.copy()
    sensitivity_b = property_b.copy()

    for property_inputs in (sensitivity_a, sensitivity_b):
        property_inputs["annual_rent_growth"] = annual_rent_growth
        property_inputs["vacancy_rate"] = vacancy_rate
        property_inputs["management_fee_rate"] = management_fee_rate
        property_inputs["annual_insurance_growth"] = (
            annual_insurance_growth
        )

    projection_a, summary_a = project_property(sensitivity_a)
    projection_b, summary_b = project_property(sensitivity_b)

    profit_difference = (
        summary_b["Total Profit"]
        - summary_a["Total Profit"]
    )

    winner = (
        "Property B"
        if profit_difference > 0
        else "Property A"
    )

    break_even_rate = calculate_break_even_appreciation(
        sensitivity_a,
        sensitivity_b,
    )

    return {
        "Property A Inputs": sensitivity_a,
        "Property B Inputs": sensitivity_b,
        "Property A Projection": projection_a,
        "Property B Projection": projection_b,
        "Property A Summary": summary_a,
        "Property B Summary": summary_b,
        "B Minus A": profit_difference,
        "Winner": winner,
        "Break-Even Appreciation": break_even_rate,
    }


def create_rent_vacancy_sensitivity(
    property_a,
    property_b,
    rent_growth_rates,
    vacancy_rates,
    management_fee_rate,
    annual_insurance_growth,
):
    """
    Calculate Property B's profit advantage across combinations
    of rent growth and vacancy assumptions.
    """
    records = []

    for rent_growth in rent_growth_rates:
        for vacancy_rate in vacancy_rates:
            result = run_operating_sensitivity(
                property_a=property_a,
                property_b=property_b,
                annual_rent_growth=rent_growth,
                vacancy_rate=vacancy_rate,
                management_fee_rate=management_fee_rate,
                annual_insurance_growth=(
                    annual_insurance_growth
                ),
            )

            records.append(
                {
                    "Rent Growth": rent_growth,
                    "Vacancy Rate": vacancy_rate,
                    "Property A Total Profit": result[
                        "Property A Summary"
                    ]["Total Profit"],
                    "Property B Total Profit": result[
                        "Property B Summary"
                    ]["Total Profit"],
                    "B Minus A": result["B Minus A"],
                    "Winner": result["Winner"],
                }
            )

    return pd.DataFrame(records)