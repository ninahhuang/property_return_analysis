# 10-Year Rental Property Return Analysis

An interactive financial model for comparing the projected 10-year performance of two long-term rental properties in Celina, Texas.

The project evaluates rental cash flow, operating expenses, mortgage amortization, property appreciation, accumulated equity, sale proceeds, and total investment return. It also identifies the annual appreciation rate at which the more expensive property begins producing more total profit.

## Project objective

The central investment question is:

> At what annual appreciation rate does Property B produce a higher 10-year total profit than Property A after accounting for rental cash flow, operating costs, mortgage payments, and sale proceeds?

The model compares:

| Assumption         | Property A | Property B |
| ------------------ | ---------: | ---------: |
| Location           | Celina, TX | Celina, TX |
| Purchase price     |   $350,000 |   $520,000 |
| Down payment       |   $250,000 |   $250,000 |
| Starting mortgage  |   $100,000 |   $270,000 |
| Monthly rent       |     $2,500 |     $3,500 |
| Annual insurance   |     $3,500 |     $5,500 |
| Annual maintenance |     $3,500 |     $5,500 |
| Mortgage rate      |       6.8% |       6.8% |
| Mortgage term      |   30 years |   30 years |
| Holding period     |   10 years |   10 years |

These are default inputs only. The Streamlit dashboard allows the user to change the assumptions interactively.

## Main features

### Interactive property inputs

The dashboard allows users to modify:

* Purchase price
* Down payment
* Monthly rent
* Annual homeowners’ insurance
* Annual maintenance
* Monthly HOA fees

### Shared investment assumptions

Users can also modify:

* Mortgage rate
* Mortgage term
* Holding period
* Annual property appreciation
* Annual rent growth
* Vacancy rate
* Property-tax rate
* Management fee
* Annual insurance growth
* Buying costs
* Selling costs

### Investment summary

The dashboard calculates and compares:

* Initial cash investment
* Mortgage amount
* Monthly mortgage payment
* Year-one cash flow
* Cumulative cash flow
* Projected sale price
* Remaining mortgage balance
* Net sale proceeds
* Total profit
* Total return
* Simplified annualized return

### Annual projections

The model produces annual projections for:

* Rental income
* Vacancy loss
* Collected rent
* Property taxes
* Insurance
* Maintenance
* HOA fees
* Management fees
* Net operating income
* Mortgage payments
* Annual cash flow
* Property value
* Mortgage balance
* Owner equity

### Appreciation sensitivity analysis

The model recalculates total profit across a range of annual appreciation assumptions.

It estimates the break-even appreciation rate by solving for the rate at which:

```text
Property A Total Profit = Property B Total Profit
```

A rate below the break-even threshold favors Property A. A rate above the threshold favors Property B, assuming both properties experience the same annual appreciation rate.

### Operating sensitivity analysis

The dashboard provides separate sensitivity controls for:

* Annual rent growth
* Vacancy rate
* Management fee
* Annual insurance growth

These controls allow the user to test operating scenarios without changing the base-case headline results.

A rent-growth and vacancy heatmap shows which property produces more total profit under different combinations of assumptions:

* Positive “B Minus A” values indicate that Property B produces more profit.
* Negative “B Minus A” values indicate that Property A produces more profit.

### Formula reference

The dashboard includes a Formula Reference tab documenting the calculations used for:

* Rental revenue
* Vacancy
* Operating expenses
* Net operating income
* Mortgage payments
* Remaining mortgage balance
* Annual cash flow
* Property appreciation
* Sale proceeds
* Total profit
* Total return
* Annualized return
* Break-even appreciation

The formulas are displayed using LaTeX notation.

## Repository structure

```text
rental_property_analysis/
├── app.py
├── calculations.py
├── rental_property_analysis.ipynb
├── requirements.txt
├── README.md
├── .gitignore
└── visualizations/
```

### `app.py`

Contains the Streamlit dashboard, including:

* Sidebar inputs
* Input validation
* Summary metrics
* Comparison tables
* Matplotlib charts
* Appreciation sensitivity analysis
* Operating sensitivity controls
* Formula reference

### `calculations.py`

Contains the reusable financial-model functions:

* `calculate_mortgage_balance()`
* `project_property()`
* `calculate_profit_difference()`
* `calculate_break_even_appreciation()`
* `create_appreciation_scenarios()`
* `run_operating_sensitivity()`
* `create_rent_vacancy_sensitivity()`

Keeping the financial calculations separate from the dashboard makes the model easier to test, audit, and reuse.

### `rental_property_analysis.ipynb`

Contains the original analysis and validation workflow, including:

* Base assumptions
* Mortgage calculations
* Ten-year property projections
* Property comparison tables
* Matplotlib visualizations
* Appreciation scenarios
* Break-even analysis
* Validation checks

### `requirements.txt`

Lists the Python packages required to run the notebook and dashboard.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR-REPOSITORY-URL>
cd rental_property_analysis
```

Replace `<YOUR-REPOSITORY-URL>` with the GitHub URL for this repository.

### 2. Create a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
```

On Windows:

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows Command Prompt:

```bash
.venv\Scripts\activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Once activated, the terminal prompt should begin with:

```text
(.venv)
```

### 4. Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The main dependencies are:

```text
streamlit
pandas
numpy
numpy-financial
matplotlib
scipy
jupyter
```

## Running the dashboard

From the repository folder, activate the virtual environment and run:

```bash
python -m streamlit run app.py
```

Streamlit should open the dashboard automatically. If it does not, open:

```text
http://localhost:8501
```

Keep the terminal open while using the dashboard.

To stop the dashboard, return to the terminal and press:

```text
Control + C
```

## Running the analysis notebook

Start Jupyter:

```bash
python -m jupyter notebook
```

Then open:

```text
rental_property_analysis.ipynb
```

Alternatively, open the notebook directly in VS Code and select the Python interpreter from the project’s `.venv`.

When changing an assumption, restart the kernel and run all cells from top to bottom. This prevents older values stored in memory from affecting later tables or charts.

## Core methodology

### Mortgage amount

```text
Mortgage Amount = Purchase Price − Down Payment
```

### Monthly mortgage payment

The model uses the standard fixed-rate mortgage formula:

```text
Monthly Payment =
Loan Amount × [r(1 + r)^n] / [(1 + r)^n − 1]
```

Where:

* `r` is the monthly mortgage rate.
* `n` is the total number of monthly payments.

The implementation uses `numpy_financial.pmt()`.

### Initial cash investment

```text
Initial Cash Investment =
Down Payment
+ Buying Costs
+ Initial Renovation Cost
```

Buying costs are calculated as:

```text
Buying Costs = Purchase Price × Buying Cost Rate
```

Initial cash investment is therefore usually greater than the down payment alone.

### Monthly rent

```text
Monthly Rent in Year t =
Initial Monthly Rent × (1 + Rent Growth Rate)^(t − 1)
```

### Scheduled rent

```text
Scheduled Rent = Monthly Rent × 12
```

### Vacancy loss

```text
Vacancy Loss = Scheduled Rent × Vacancy Rate
```

### Collected rent

```text
Collected Rent = Scheduled Rent − Vacancy Loss
```

### Property tax

```text
Property Tax =
Beginning Property Value × Property-Tax Rate
```

The current model allows property taxes to increase as the projected property value increases.

### Insurance

```text
Insurance in Year t =
Initial Insurance × (1 + Insurance Growth Rate)^(t − 1)
```

### Management fee

```text
Management Fee =
Collected Rent × Management Fee Rate
```

### Total operating expenses

```text
Total Operating Expenses =
Property Tax
+ Insurance
+ Maintenance
+ HOA
+ Management Fee
```

### Net operating income

```text
NOI = Collected Rent − Total Operating Expenses
```

Mortgage payments are excluded from NOI and handled separately.

### Annual cash flow

```text
Annual Cash Flow =
NOI − Annual Mortgage Payments
```

### Ending property value

```text
Ending Property Value =
Beginning Property Value × (1 + Appreciation Rate)
```

### Ending equity

```text
Ending Equity =
Ending Property Value − Ending Mortgage Balance
```

### Selling costs

```text
Selling Costs =
Projected Sale Price × Selling Cost Rate
```

### Net sale proceeds

```text
Net Sale Proceeds =
Projected Sale Price
− Selling Costs
− Remaining Mortgage
```

### Cumulative cash flow

```text
Cumulative Cash Flow =
Sum of Annual Cash Flow During the Holding Period
```

### Total profit

```text
Total Profit =
Cumulative Cash Flow
+ Net Sale Proceeds
− Initial Cash Investment
```

### Total return

```text
Total Return =
Total Profit / Initial Cash Investment
```

### Simplified annualized return

```text
Simplified Annualized Return =
(1 + Total Return)^(1 / Holding Period) − 1
```

This metric is not the same as internal rate of return. It annualizes the total holding-period return but does not account for the timing of individual annual cash flows.

## Default-scenario interpretation

Under the default assumptions, Property A generally benefits from:

* A smaller mortgage
* Lower mortgage payments
* Lower property taxes
* Lower insurance
* Lower maintenance costs
* Stronger annual cash flow

Property B benefits from:

* A higher starting property value
* A larger dollar gain from the same appreciation rate
* Greater potential sale proceeds

Property B must generate enough additional rent or appreciation to offset its higher financing and operating costs.

After reducing Property B’s default purchase price from `$550,000` to `$520,000`, its mortgage decreases from `$300,000` to `$270,000`. This improves its cash flow and lowers the appreciation rate required to match Property A.

Under the current default assumptions, the estimated appreciation break-even rate is approximately `4.69%` per year. This result will change whenever the user modifies rent, expenses, financing, buying costs, selling costs, or the holding period.

## Interpretation of “B Minus A”

Several tables and visualizations report:

```text
B Minus A =
Property B Total Profit − Property A Total Profit
```

Interpretation:

| B Minus A | Meaning                                       |
| --------: | --------------------------------------------- |
|  Positive | Property B produces more total profit         |
|      Zero | The two properties produce equal total profit |
|  Negative | Property A produces more total profit         |

## Model validation

The notebook includes reasonableness and reconciliation checks for key outputs such as:

* Mortgage payment
* Year-one cash flow
* Cumulative cash flow
* Projected sale price
* Remaining mortgage
* Total profit

After changing a default assumption, the validation benchmarks must also be updated. Otherwise, assertions tied to the previous scenario may fail even when the model is calculating correctly.

The notebook should be restarted and executed from top to bottom after every material assumption change.

## Current limitations

This model is an investment-planning tool rather than a guarantee of future performance.

Important limitations include:

* Appreciation is modeled as a constant annual rate.
* Rent growth is modeled as a constant annual rate.
* Vacancy is modeled as a constant percentage.
* Maintenance is currently a fixed annual amount.
* Property tax is estimated using the projected property value rather than an independently modeled assessed value.
* The model does not currently distinguish land value from building value.
* The model does not include federal income taxes.
* The model does not include capital-gains taxes.
* The model does not include depreciation recapture.
* The model does not calculate a complete after-tax return.
* The model does not include irregular capital expenditures unless entered through the available assumptions.
* The model does not explicitly model leasing commissions, tenant-placement fees, utilities, legal costs, or eviction costs.
* Insurance estimates are assumptions rather than binding quotes.
* Monthly rent estimates should be validated using current comparable leases.
* Selling costs are estimated as a percentage of the projected sale price.
* The simplified annualized return is not a cash-flow-timed IRR.
* Market conditions, financing terms, taxes, insurance, and rental demand may differ materially from the assumptions.

## Recommended due diligence

Before making an investment decision, replace the default assumptions with property-specific information:

1. Obtain a professional homeowners’ or landlord-insurance quote.
2. Confirm the applicable property-tax rate and likely assessed value.
3. Review comparable long-term rental listings.
4. Confirm HOA dues, restrictions, and special assessments.
5. Obtain a current mortgage estimate.
6. Estimate inspection, repair, renovation, and closing costs.
7. Review expected property-management fees.
8. Evaluate major capital expenditures such as roofing, HVAC, plumbing, and appliances.
9. Confirm likely selling costs.
10. Consult qualified real-estate, tax, legal, and financial professionals.

## Possible future improvements

Potential extensions include:

* Internal rate of return
* Net present value
* Cash-on-cash return
* Debt-service coverage ratio
* Capital-expenditure schedules
* Property-specific tax assessments
* After-tax cash flow
* Depreciation and depreciation recapture
* Capital-gains taxation
* Monte Carlo simulation
* Rent and expense probability distributions
* Refinance scenarios
* Alternative holding periods
* Exportable PDF or CSV reports
* Saved user scenarios
* Additional property comparisons
* Market-data integration

## Technology

* Python
* Streamlit
* pandas
* NumPy
* NumPy Financial
* SciPy
* Matplotlib
* Jupyter Notebook

## Disclaimer

This project is for educational and analytical purposes only. It does not constitute investment, tax, legal, accounting, mortgage, or real-estate advice.

All results depend on user-supplied assumptions and simplified projections. Actual investment results may vary significantly. Users should independently verify all property information and consult qualified professionals before making a purchase or financing decision.

## Author

Prepared by Nina Huang.