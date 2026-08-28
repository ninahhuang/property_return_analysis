# 10-Year Property Return Analysis

An interactive rental-property investment dashboard comparing the 10-year performance of two properties in Celina, Texas.

The model combines:

- Rental income and operating expenses
- Mortgage amortization
- Property appreciation
- Sale proceeds and transaction costs
- Total profit and return

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py