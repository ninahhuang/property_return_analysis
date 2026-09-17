import pytest

from calculations import calculate_mortgage_balance, project_property


def test_paid_off_mortgage_cannot_be_negative():
    balance = calculate_mortgage_balance(
        mortgage_amount=300_000,
        annual_mortgage_rate=0.06,
        mortgage_term_years=30,
        payments_made=360,
    )

    assert balance == pytest.approx(0.0, abs=1.0)


def test_mortgage_balance_declines_over_time():
    early_balance = calculate_mortgage_balance(
        mortgage_amount=300_000,
        annual_mortgage_rate=0.06,
        mortgage_term_years=30,
        payments_made=12,
    )

    later_balance = calculate_mortgage_balance(
        mortgage_amount=300_000,
        annual_mortgage_rate=0.06,
        mortgage_term_years=30,
        payments_made=120,
    )

    assert later_balance < early_balance