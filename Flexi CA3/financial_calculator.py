def calculate_ratios(
    revenue,
    net_profit,
    total_debt,
    total_assets,
    current_assets,
    current_liabilities,
    inventory,
    prepaid_expenses,
    operating_cash_flow,
    ebit,
    interest_expense
):
    """
    Calculate financial ratios used for risk assessment.
    """

    # Basic validation

    if revenue <= 0:
        raise ValueError("Revenue must be greater than 0.")

    if total_assets <= 0:
        raise ValueError("Total assets must be greater than 0.")

    if current_assets < 0:
        raise ValueError("Current assets cannot be negative.")

    if current_liabilities <= 0:
        raise ValueError(
            "Current liabilities must be greater than 0."
        )

    if inventory < 0:
        raise ValueError("Inventory cannot be negative.")

    if prepaid_expenses < 0:
        raise ValueError(
            "Prepaid expenses cannot be negative."
        )


    # 1. Profit Margin

    profit_margin = (
        net_profit / revenue
    ) * 100


    # 2. Debt-to-Asset Ratio

    debt_to_asset = (
        total_debt / total_assets
    ) * 100


    # 3. Current Ratio

    current_ratio = (
        current_assets /
        current_liabilities
    )


    # 4. Quick Assets

    quick_assets = (
        current_assets
        - inventory
        - prepaid_expenses
    )

    if quick_assets < 0:
        quick_assets = 0


    # 5. Quick Ratio

    quick_ratio = (
        quick_assets /
        current_liabilities
    )


    # 6. Shareholders' Equity

    equity = (
        total_assets -
        total_debt
    )


    # 7. Debt-to-Equity Ratio

    if equity > 0:
        debt_to_equity = (
            total_debt / equity
        )
    else:
        debt_to_equity = None


    # 8. Operating Cash Flow Ratio

    ocf_ratio = (
        operating_cash_flow /
        current_liabilities
    )


    # 9. Interest Coverage Ratio

    if interest_expense > 0:
        interest_coverage_ratio = (
            ebit / interest_expense
        )
    else:
        interest_coverage_ratio = None


    # Return results

    return {
        "profit_margin": profit_margin,
        "debt_to_asset": debt_to_asset,
        "current_ratio": current_ratio,
        "quick_assets": quick_assets,
        "quick_ratio": quick_ratio,
        "equity": equity,
        "debt_to_equity": debt_to_equity,
        "ocf_ratio": ocf_ratio,
        "interest_coverage_ratio":
            interest_coverage_ratio
    }