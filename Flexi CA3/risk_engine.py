def assess_profitability(profit_margin):
    if profit_margin > 15:
        return "LOW"
    elif profit_margin >= 5:
        return "MEDIUM"
    else:
        return "HIGH"


def assess_debt(debt_to_asset):
    if debt_to_asset < 40:
        return "LOW"
    elif debt_to_asset <= 60:
        return "MEDIUM"
    else:
        return "HIGH"


def assess_liquidity(current_ratio):
    if current_ratio >= 1.5:
        return "LOW"
    elif current_ratio >= 1.0:
        return "MEDIUM"
    else:
        return "HIGH"


def assess_quick_liquidity(quick_ratio):
    if quick_ratio >= 1.0:
        return "LOW"
    elif quick_ratio >= 0.5:
        return "MEDIUM"
    else:
        return "HIGH"


def assess_cash_flow(ocf_ratio):
    if ocf_ratio >= 0.5:
        return "LOW"
    elif ocf_ratio >= 0.2:
        return "MEDIUM"
    else:
        return "HIGH"


def assess_interest_coverage(interest_coverage_ratio):
    if interest_coverage_ratio is None:
        return "LOW"

    if interest_coverage_ratio >= 5:
        return "LOW"
    elif interest_coverage_ratio >= 2:
        return "MEDIUM"
    else:
        return "HIGH"


def calculate_risk_score(risk_categories):
    score_map = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3
    }

    score = sum(
        score_map[risk]
        for risk in risk_categories.values()
    )

    return score


def determine_overall_risk(score, number_of_categories):
    maximum_score = number_of_categories * 3

    if score <= maximum_score * 0.50:
        return "LOW"
    elif score <= maximum_score * 0.75:
        return "MEDIUM"
    else:
        return "HIGH"