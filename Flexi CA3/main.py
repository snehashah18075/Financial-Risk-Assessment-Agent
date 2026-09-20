from financial_calculator import calculate_ratios

from risk_engine import (
    assess_profitability,
    assess_debt,
    assess_liquidity,
    assess_quick_liquidity,
    assess_cash_flow,
    assess_interest_coverage,
    calculate_risk_score,
    determine_overall_risk
)


# ==================================================
# Company Financial Data
# ==================================================

financial_data = {
    "revenue": 100,
    "net_profit": 8,
    "total_debt": 60,
    "total_assets": 120,

    "current_assets": 45,
    "current_liabilities": 50,

    "inventory": 10,
    "prepaid_expenses": 5,

    "operating_cash_flow": 5,

    "ebit": 15,
    "interest_expense": 5
}


# ==================================================
# Step 1: Calculate Financial Ratios
# ==================================================

ratios = calculate_ratios(**financial_data)


# ==================================================
# Step 2: Assess Individual Risk Categories
# ==================================================

risk_categories = {

    "Profitability": assess_profitability(
        ratios["profit_margin"]
    ),

    "Debt": assess_debt(
        ratios["debt_to_asset"]
    ),

    "Liquidity": assess_liquidity(
        ratios["current_ratio"]
    ),

    "Quick Liquidity": assess_quick_liquidity(
        ratios["quick_ratio"]
    ),

    "Cash Flow": assess_cash_flow(
        ratios["ocf_ratio"]
    ),

    "Interest Coverage": assess_interest_coverage(
        ratios["interest_coverage_ratio"]
    )
}


# ==================================================
# Step 3: Calculate Overall Risk
# ==================================================

score = calculate_risk_score(
    risk_categories
)

number_of_categories = len(
    risk_categories
)

overall_risk = determine_overall_risk(
    score,
    number_of_categories
)


# ==================================================
# Step 4: Create Structured Result
# ==================================================

result = {

    "ratios": ratios,

    "risk_categories": risk_categories,

    "risk_score": score,

    "maximum_score": number_of_categories * 3,

    "overall_risk": overall_risk
}


# ==================================================
# Step 5: Display Results
# ==================================================

print("\n==========================================")
print("       FINANCIAL RISK ASSESSMENT")
print("==========================================\n")


print("FINANCIAL RATIOS")
print("------------------------------------------")

print(
    f"Profit Margin: "
    f"{ratios['profit_margin']:.2f}%"
)

print(
    f"Debt-to-Asset Ratio: "
    f"{ratios['debt_to_asset']:.2f}%"
)

print(
    f"Current Ratio: "
    f"{ratios['current_ratio']:.2f}"
)

print(
    f"Quick Assets: "
    f"{ratios['quick_assets']:.2f}"
)

print(
    f"Quick Ratio: "
    f"{ratios['quick_ratio']:.2f}"
)

if ratios["debt_to_equity"] is not None:

    print(
        f"Debt-to-Equity Ratio: "
        f"{ratios['debt_to_equity']:.2f}"
    )

else:

    print(
        "Debt-to-Equity Ratio: "
        "Not Available"
    )


print(
    f"Operating Cash Flow Ratio: "
    f"{ratios['ocf_ratio']:.2f}"
)


if ratios["interest_coverage_ratio"] is not None:

    print(
        f"Interest Coverage Ratio: "
        f"{ratios['interest_coverage_ratio']:.2f}"
    )

else:

    print(
        "Interest Coverage Ratio: "
        "Not Available"
    )


print("\nRISK ASSESSMENT")
print("------------------------------------------")

for category, risk in risk_categories.items():

    print(
        f"{category}: {risk}"
    )


print("\nOVERALL ASSESSMENT")
print("------------------------------------------")

print(
    f"Risk Score: "
    f"{result['risk_score']}/"
    f"{result['maximum_score']}"
)

print(
    f"Overall Risk: "
    f"{result['overall_risk']}"
)


print("\n==========================================")