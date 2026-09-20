import sys
import os

# Add root directory to path to ensure modules are importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

def run_financial_analysis(
    revenue: float,
    net_profit: float,
    total_debt: float,
    total_assets: float,
    current_assets: float,
    current_liabilities: float,
    inventory: float,
    prepaid_expenses: float,
    operating_cash_flow: float,
    ebit: float,
    interest_expense: float
) -> dict:
    """
    Deterministic Financial Analysis Tool.
    Calculates 9 financial ratios and evaluates 6 risk categories against defined project assessment criteria.
    Returns structured results including ratios, individual category risks, composite risk score, and overall risk.
    """
    # Step 1: Calculate Financial Ratios using deterministic formulas
    ratios = calculate_ratios(
        revenue=revenue,
        net_profit=net_profit,
        total_debt=total_debt,
        total_assets=total_assets,
        current_assets=current_assets,
        current_liabilities=current_liabilities,
        inventory=inventory,
        prepaid_expenses=prepaid_expenses,
        operating_cash_flow=operating_cash_flow,
        ebit=ebit,
        interest_expense=interest_expense
    )

    # Step 2: Assess Individual Risk Categories
    risk_categories = {
        "Profitability": assess_profitability(ratios["profit_margin"]),
        "Debt": assess_debt(ratios["debt_to_asset"]),
        "Liquidity": assess_liquidity(ratios["current_ratio"]),
        "Quick Liquidity": assess_quick_liquidity(ratios["quick_ratio"]),
        "Cash Flow": assess_cash_flow(ratios["ocf_ratio"]),
        "Interest Coverage": assess_interest_coverage(ratios["interest_coverage_ratio"])
    }

    # Step 3: Compute Overall Composite Risk Score
    score = calculate_risk_score(risk_categories)
    number_of_categories = len(risk_categories)
    maximum_score = number_of_categories * 3
    overall_risk = determine_overall_risk(score, number_of_categories)

    # Identify primary risk factors (categories with HIGH risk)
    high_risk_factors = [cat for cat, level in risk_categories.items() if level == "HIGH"]
    medium_risk_factors = [cat for cat, level in risk_categories.items() if level == "MEDIUM"]

    return {
        "ratios": ratios,
        "risk_categories": risk_categories,
        "risk_score": score,
        "maximum_score": maximum_score,
        "overall_risk": overall_risk,
        "high_risk_factors": high_risk_factors,
        "medium_risk_factors": medium_risk_factors
    }


# OpenAI tool schema definitions for LLM function calling
TOOL_CALCULATE_FINANCIAL_RISK = {
    "type": "function",
    "function": {
        "name": "run_financial_analysis",
        "description": "Calculates financial ratios and evaluates category risk levels & overall composite financial risk using deterministic rules.",
        "parameters": {
            "type": "object",
            "properties": {
                "revenue": {"type": "number", "description": "Total Company Revenue"},
                "net_profit": {"type": "number", "description": "Net Profit after taxes"},
                "total_debt": {"type": "number", "description": "Total Debt liabilities"},
                "total_assets": {"type": "number", "description": "Total Assets"},
                "current_assets": {"type": "number", "description": "Current Assets"},
                "current_liabilities": {"type": "number", "description": "Current Liabilities"},
                "inventory": {"type": "number", "description": "Inventory value"},
                "prepaid_expenses": {"type": "number", "description": "Prepaid expenses"},
                "operating_cash_flow": {"type": "number", "description": "Operating Cash Flow"},
                "ebit": {"type": "number", "description": "Earnings Before Interest and Taxes"},
                "interest_expense": {"type": "number", "description": "Interest expense on debt"}
            },
            "required": [
                "revenue", "net_profit", "total_debt", "total_assets",
                "current_assets", "current_liabilities", "inventory",
                "prepaid_expenses", "operating_cash_flow", "ebit", "interest_expense"
            ]
        }
    }
}
