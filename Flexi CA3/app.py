import gradio as gr
from agent import FinancialRiskAgent

# Initialize Financial Risk Assessment Agent
agent = FinancialRiskAgent()

CUSTOM_CSS = """
/* ============================================================
   FINRISK AI — PRIVATE ADVISORY THEME
   Inspired by investment-firm branding: deep navy + brass/gold,
   serif display headings, warm ivory page, hairline dividers.
   ============================================================ */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #f6f5f1;
    --surface: #ffffff;
    --border: #e5e2d8;
    --ink: #182236;
    --muted: #6b6f7c;

    --navy: #0d1a30;
    --navy-2: #16274a;
    --gold: #c8973f;
    --gold-soft: #f3e8d3;

    --risk-high: #9b2c2c;
    --risk-high-bg: #f6e8e7;
    --risk-medium: #b06a1c;
    --risk-medium-bg: #f8ecd9;
    --risk-low: #2f6b4f;
    --risk-low-bg: #e7f1ec;
}

body, .gradio-container {
    background-color: var(--bg) !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    color: var(--ink) !important;
    max-width: 1320px !important;
    margin: 0 auto !important;
    padding: 20px 22px 60px !important;
    line-height: 1.55 !important;
}

.gradio-container h1, .gradio-container h2, .gradio-container h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--ink) !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    margin: 0 0 12px !important;
}

/* Header — deep navy band, mirrors a private-advisory nav bar */
.app-header {
    background: var(--navy);
    border-radius: 12px;
    padding: 18px 24px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

.brand-row { display: flex; align-items: center; gap: 14px; }

.brand-accent-bar {
    width: 3px;
    align-self: stretch;
    min-height: 36px;
    background: var(--gold);
    border-radius: 2px;
    flex-shrink: 0;
}

.brand-title {
    font-family: 'Playfair Display', serif;
    font-size: 21px;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: 0.2px;
}

.brand-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--gold);
    margin-top: 3px;
}

.status-pill {
    border: 1px solid rgba(200, 151, 63, 0.5);
    color: var(--gold-soft);
    font-size: 12px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 7px 14px;
    border-radius: 20px;
}

.pulse-dot {
    width: 6px;
    height: 6px;
    background-color: var(--gold);
    border-radius: 50%;
}

/* Generic panel wrapper */
.panel-card {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 20px 22px !important;
    margin-bottom: 18px !important;
}

.panel-title {
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 4px;
}

.panel-rule {
    width: 34px;
    height: 2px;
    background: var(--gold);
    margin-bottom: 14px;
}

/* Input Section (left column) */
.input-section-card {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 20px !important;
}

.input-group-header {
    font-family: 'Playfair Display', serif;
    font-size: 13px;
    font-weight: 700;
    color: var(--navy-2);
    margin-top: 16px;
    margin-bottom: 8px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border);
}

.gradio-container input, .gradio-container textarea {
    background-color: #fdfcfa !important;
    border: 1px solid var(--border) !important;
    color: var(--ink) !important;
    border-radius: 6px !important;
    font-size: 13.5px !important;
    padding: 9px 11px !important;
}

.gradio-container input:focus, .gradio-container textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-soft) !important;
}

.gradio-container label span {
    color: var(--muted) !important;
    font-weight: 500 !important;
    font-size: 12px !important;
}

/* Primary Button — gold, matches the reference's CTA treatment */
.analyze-primary-btn {
    background: var(--gold) !important;
    color: var(--navy) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 13px !important;
    border-radius: 7px !important;
    border: none !important;
    margin-top: 18px !important;
    cursor: pointer !important;
    width: 100% !important;
    transition: background 0.15s ease !important;
}

.analyze-primary-btn:hover { background: #b3831f !important; }

/* Hero risk summary — the one bold, dark moment on the page */
.hero-risk-card {
    background: var(--navy);
    border-radius: 12px;
    padding: 26px 28px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 24px;
}

.risk-seal {
    flex-shrink: 0;
    width: 70px;
    height: 70px;
    border-radius: 50%;
    border: 2.5px solid currentColor;
    background: rgba(255,255,255,0.03);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Playfair Display', serif;
}

.risk-seal.risk-high { color: #e08585; }
.risk-seal.risk-medium { color: #e3ae66; }
.risk-seal.risk-low { color: #7ecba3; }

.seal-grade { font-size: 18px; font-weight: 700; line-height: 1; }
.seal-label { font-family: 'Inter', sans-serif; font-size: 7px; font-weight: 600; letter-spacing: 0.5px; margin-top: 3px; }

.hero-details { flex: 1; min-width: 140px; }
.hero-eyebrow { font-size: 11px; font-weight: 500; letter-spacing: 1.2px; text-transform: uppercase; color: var(--gold); }
.hero-company { font-family: 'Playfair Display', serif; font-size: 21px; font-weight: 700; color: #ffffff; margin-top: 4px; }

.hero-right-col { text-align: right; }
.score-num { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; color: #ffffff; }
.score-max { font-size: 14px; color: rgba(255,255,255,0.55); font-weight: 400; }
.engine-info { font-size: 11.5px; color: rgba(255,255,255,0.5); margin-top: 4px; }

/* Metrics — a single unified strip with hairline dividers, not repeated cards */
.metrics-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 8px;
    margin-bottom: 20px;
}

.metrics-eyebrow {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--gold);
    padding: 0 14px 14px;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
}

.metric-cell {
    padding: 8px 18px;
    border-left: 1px solid var(--border);
}

.metric-cell:nth-child(4n+1) { border-left: none; }
.metric-cell:nth-child(n+5) { border-top: 1px solid var(--border); padding-top: 16px; margin-top: 8px; }

.metric-name { font-size: 11.5px; color: var(--muted); font-weight: 500; }
.metric-val { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: var(--ink); margin: 4px 0 2px; }
.metric-sub { font-size: 10.5px; color: var(--muted); }

/* Categories */
.categories-grid { display: flex; flex-direction: column; gap: 8px; }

.category-card {
    background: #fdfcfa;
    border: 1px solid var(--border);
    border-radius: 7px;
    padding: 11px 14px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.cat-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.cat-dot.risk-high { background: var(--risk-high); }
.cat-dot.risk-medium { background: var(--risk-medium); }
.cat-dot.risk-low { background: var(--risk-low); }

.cat-header { display: flex; justify-content: space-between; align-items: center; gap: 10px; flex: 1; }
.cat-name { font-size: 13.5px; font-weight: 600; color: var(--ink); }

.badge-small { padding: 3px 10px; border-radius: 5px; font-size: 10.5px; font-weight: 700; display: inline-block; }
.badge-high { background: var(--risk-high-bg); color: var(--risk-high); }
.badge-medium { background: var(--risk-medium-bg); color: var(--risk-medium); }
.badge-low { background: var(--risk-low-bg); color: var(--risk-low); }

/* Risk factors */
.factor-title-high { font-size: 12px; font-weight: 700; color: var(--risk-high); margin-bottom: 6px; }
.factor-title-med { font-size: 12px; font-weight: 700; color: var(--risk-medium); margin-top: 12px; margin-bottom: 6px; }

.factor-list-item {
    font-size: 13px;
    color: var(--ink);
    padding: 7px 12px;
    background: #fdfcfa;
    border-radius: 6px;
    margin-bottom: 5px;
}

/* AI Analyst Insight — full-width panel, tables need the room */
.insight-markdown { overflow-x: auto; }

.insight-markdown table {
    width: 100%;
    border-collapse: collapse;
    table-layout: auto;
    font-size: 13px;
    margin: 10px 0 16px;
}

.insight-markdown th, .insight-markdown td {
    border: 1px solid var(--border);
    padding: 9px 12px;
    text-align: left;
    vertical-align: top;
    white-space: normal;
}

.insight-markdown th {
    background: #fbfaf7;
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    color: var(--ink);
    white-space: nowrap;
}

.insight-markdown code {
    background: var(--gold-soft);
    color: #8a6420;
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 12px;
}

.insight-markdown h1, .insight-markdown h2, .insight-markdown h3 {
    font-size: 15px !important;
    margin-top: 16px !important;
}

/* Agent activity timeline */
.timeline-step { display: flex; align-items: center; gap: 12px; padding: 8px 0; border-bottom: 1px solid var(--border); }
.timeline-step:last-child { border-bottom: none; }

.step-code {
    font-family: 'Playfair Display', serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--navy);
    background: var(--gold-soft);
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.step-text { font-size: 13px; color: var(--ink); }

/* Disclaimer footer — echoes the navy footer band */
.disclaimer-banner {
    background: var(--navy);
    border-radius: 10px;
    padding: 16px 22px;
    margin-top: 22px;
    font-size: 11.5px;
    color: rgba(255,255,255,0.55);
    line-height: 1.6;
}

.error-banner {
    background: var(--risk-high-bg);
    border: 1px solid var(--risk-high);
    border-radius: 10px;
    padding: 18px 20px;
    color: var(--risk-high);
}
.error-title { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 15px; margin-bottom: 5px; }
.error-desc { font-size: 13px; }

.empty-state {
    background: var(--surface);
    border: 1px dashed var(--border);
    border-radius: 12px;
    padding: 34px 26px;
    text-align: center;
    color: var(--muted);
    font-size: 13.5px;
}

@media (max-width: 900px) {
    .metrics-grid { grid-template-columns: repeat(2, 1fr); }
    .metric-cell:nth-child(4n+1) { border-left: 1px solid var(--border); }
    .metric-cell:nth-child(2n+1) { border-left: none; }
    .metric-cell:nth-child(n+3) { border-top: 1px solid var(--border); padding-top: 16px; margin-top: 8px; }
    .hero-risk-card { flex-direction: column; align-items: flex-start; }
    .hero-right-col { text-align: left; }
}
"""


def risk_color_class(level):
    """Return CSS risk class."""
    lvl = str(level).upper()
    if lvl == "HIGH":
        return "risk-high"
    elif lvl == "MEDIUM":
        return "risk-medium"
    return "risk-low"


def risk_grade(level):
    """Map a risk level to a ratings-agency-style grade letter."""
    lvl = str(level).upper()
    if lvl == "HIGH":
        return "CCC"
    elif lvl == "MEDIUM":
        return "BB"
    return "A"


def risk_badge_large(level):
    """Generate the hero rating seal."""
    lvl = str(level).upper()
    cls = risk_color_class(level)
    grade = risk_grade(level)
    return f"""
    <div class="risk-seal {cls}">
        <span class="seal-grade">{grade}</span>
        <span class="seal-label">{lvl}</span>
    </div>
    """


def risk_badge_small(level):
    """Generate small HTML risk badge."""
    lvl = str(level).upper()
    if lvl == "HIGH":
        return '<span class="badge-small badge-high">HIGH</span>'
    elif lvl == "MEDIUM":
        return '<span class="badge-small badge-medium">MEDIUM</span>'
    return '<span class="badge-small badge-low">LOW</span>'


def metric_cell_html(title, value, subtitle):
    """Generate one cell of the metrics strip."""
    return f"""
    <div class="metric-cell">
        <div class="metric-name">{title}</div>
        <div class="metric-val">{value}</div>
        <div class="metric-sub">{subtitle}</div>
    </div>
    """


def category_card_html(title, level):
    """Generate HTML category row."""
    cls = risk_color_class(level)
    badge = risk_badge_small(level)
    return f"""
    <div class="category-card">
        <span class="cat-dot {cls}"></span>
        <div class="cat-header">
            <span class="cat-name">{title}</span>
            {badge}
        </div>
    </div>
    """


def process_assessment(
    company_name,
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
    interest_expense,
    web_search_query
):
    """
    Handler function for Gradio interface.
    Validates inputs, passes financial parameters to Agent, and formats output components.
    """
    # 1. Input Validation
    try:
        revenue = float(revenue)
        net_profit = float(net_profit)
        total_debt = float(total_debt)
        total_assets = float(total_assets)
        current_assets = float(current_assets)
        current_liabilities = float(current_liabilities)
        inventory = float(inventory)
        prepaid_expenses = float(prepaid_expenses)
        operating_cash_flow = float(operating_cash_flow)
        ebit = float(ebit)
        interest_expense = float(interest_expense)
    except (ValueError, TypeError):
        error_html = """
        <div class="error-banner">
            <div class="error-title">Input Validation Error</div>
            <div class="error-desc">Please enter valid numerical values for all financial fields.</div>
        </div>
        """
        return error_html, "", "", [], "", "Input validation failed. Please fix inputs above.", "", "", ""

    financial_data = {
        "revenue": revenue,
        "net_profit": net_profit,
        "total_debt": total_debt,
        "total_assets": total_assets,
        "current_assets": current_assets,
        "current_liabilities": current_liabilities,
        "inventory": inventory,
        "prepaid_expenses": prepaid_expenses,
        "operating_cash_flow": operating_cash_flow,
        "ebit": ebit,
        "interest_expense": interest_expense
    }

    # 2. Execute Existing Agent Analysis
    result = agent.analyze(
        company_name=company_name,
        financial_data=financial_data,
        web_search_query=web_search_query
    )

    if not result["success"]:
        error_html = f"""
        <div class="error-banner">
            <div class="error-title">Assessment Error</div>
            <div class="error-desc">{result.get('error', 'Error occurred during risk assessment.')}</div>
        </div>
        """
        return error_html, "", "", [], "", "Assessment failed.", "", "", ""

    calc = result["calc_results"]
    ratios = calc["ratios"]
    categories = calc["risk_categories"]
    overall_risk = calc["overall_risk"]
    risk_score = calc["risk_score"]
    maximum_score = calc["maximum_score"]

    # 3. Overall Risk Hero Card
    seal = risk_badge_large(overall_risk)

    summary_html = f"""
    <div class="hero-risk-card">
        {seal}
        <div class="hero-details">
            <div class="hero-eyebrow">Risk Assessment</div>
            <div class="hero-company">{result['company_name']}</div>
        </div>
        <div class="hero-right-col">
            <div class="score-num">{risk_score} <span class="score-max">/ {maximum_score}</span></div>
            <div class="engine-info">Model: {result['used_model']}</div>
        </div>
    </div>
    """

    # 4. Key Financial Metrics — single strip with hairline dividers
    profit_margin = ratios["profit_margin"]
    current_ratio = ratios["current_ratio"]
    quick_ratio = ratios["quick_ratio"]
    debt_to_asset = ratios["debt_to_asset"]
    ocf_ratio = ratios["ocf_ratio"]
    interest_coverage = ratios["interest_coverage_ratio"]
    quick_assets = ratios["quick_assets"]
    debt_to_equity = ratios["debt_to_equity"]

    interest_display = f"{interest_coverage:.2f}×" if interest_coverage is not None else "N/A"
    dte_display = f"{debt_to_equity:.2f}" if debt_to_equity is not None else "N/A"

    metrics_html = f"""
    <div class="metrics-eyebrow">Key Financial Metrics</div>
    <div class="metrics-grid">
        {metric_cell_html("Profit Margin", f"{profit_margin:.2f}%", "Net Profit / Revenue")}
        {metric_cell_html("Current Ratio", f"{current_ratio:.2f}", "Current Assets / Liabilities")}
        {metric_cell_html("Quick Ratio", f"{quick_ratio:.2f}", "Quick Assets / Liabilities")}
        {metric_cell_html("Debt-to-Asset", f"{debt_to_asset:.2f}%", "Total Debt / Total Assets")}
        {metric_cell_html("Debt-to-Equity", dte_display, "Total Debt / Equity")}
        {metric_cell_html("OCF Ratio", f"{ocf_ratio:.2f}", "Op. Cash Flow / Liabilities")}
        {metric_cell_html("Interest Coverage", interest_display, "EBIT / Interest Expense")}
        {metric_cell_html("Quick Assets", f"{quick_assets:.2f}", "Liquid Asset Buffer")}
    </div>
    """

    # 5. Category Risk Breakdown
    category_html = f"""
    <div class="categories-grid">
        {category_card_html("Profitability", categories["Profitability"])}
        {category_card_html("Debt & Solvency", categories["Debt"])}
        {category_card_html("Liquidity", categories["Liquidity"])}
        {category_card_html("Quick Liquidity", categories["Quick Liquidity"])}
        {category_card_html("Cash Flow", categories["Cash Flow"])}
        {category_card_html("Interest Coverage", categories["Interest Coverage"])}
    </div>
    """

    # 6. Risk Category Criteria table (the ratios table has been removed as redundant)
    categories_data = [
        ["Profitability", categories["Profitability"], ">15% Low | 5-15% Medium | <5% High"],
        ["Debt & Solvency", categories["Debt"], "<40% Low | 40-60% Medium | >60% High"],
        ["Liquidity (Current)", categories["Liquidity"], ">=1.5 Low | 1.0-1.49 Medium | <1.0 High"],
        ["Quick Liquidity", categories["Quick Liquidity"], ">=1.0 Low | 0.5-0.99 Medium | <0.5 High"],
        ["Cash Flow", categories["Cash Flow"], ">=0.5 Low | 0.2-0.49 Medium | <0.2 High"],
        ["Interest Coverage", categories["Interest Coverage"], ">=5.0 Low | 2.0-4.99 Medium | <2.0 High"]
    ]

    # 7. Risk Factors Section
    high_factors = calc.get("high_risk_factors", [])
    med_factors = calc.get("medium_risk_factors", [])

    factors_html = ""
    if high_factors:
        factors_html += '<div class="factor-title-high">High-Risk Factors</div>'
        for f in high_factors:
            factors_html += f'<div class="factor-list-item">{f}</div>'

    if med_factors:
        factors_html += '<div class="factor-title-med">Medium-Risk Factors</div>'
        for f in med_factors:
            factors_html += f'<div class="factor-list-item">{f}</div>'

    if not high_factors and not med_factors:
        factors_html += '<div class="factor-list-item">All financial categories assessed as low risk under project criteria.</div>'

    # 8. AI Explanation Markdown
    ai_explanation = result.get("ai_explanation", "No AI interpretation available.")

    # 9. Agent Activity Log (Timeline style)
    agent_steps = result.get("agent_steps", [])
    activity_html = ""
    if agent_steps:
        for idx, step in enumerate(agent_steps, 1):
            activity_html += f"""
            <div class="timeline-step">
                <span class="step-code">{idx:02d}</span>
                <span class="step-text">{step}</span>
            </div>
            """
    else:
        activity_html += '<div class="timeline-step"><span class="step-code">01</span><span class="step-text">Assessment completed by Financial Risk Agent.</span></div>'

    # 10. RAG and Web Sources
    rag_sources = result.get("rag_sources", "No RAG knowledge retrieved.")
    web_sources = result.get("web_sources", "No web research requested.")

    return (
        summary_html,
        metrics_html,
        category_html,
        categories_data,
        factors_html,
        ai_explanation,
        activity_html,
        rag_sources,
        web_sources
    )


def create_ui():
    """Build and return the Gradio UI for FINRISK AI — navy/gold advisory-firm theme."""
    with gr.Blocks(title="FINRISK AI — Financial Risk Assessment Agent") as ui:

        # Header
        gr.HTML(
            """
            <div class="app-header">
                <div class="brand-row">
                    <div class="brand-accent-bar"></div>
                    <div>
                        <div class="brand-title">FinRisk AI</div>
                        <div class="brand-subtitle">Financial Risk Assessment Agent</div>
                    </div>
                </div>
                <div class="status-pill"><span class="pulse-dot"></span> Analyst ready</div>
            </div>
            """
        )

        with gr.Row():
            # Left column: compact input panel
            with gr.Column(scale=1, min_width=280):
                with gr.Group(elem_classes=["input-section-card"]):
                    gr.HTML('<div class="panel-title">New Assessment</div><div class="panel-rule"></div>')
                    company_name = gr.Textbox(
                        label="Company Name",
                        value="Test Company A",
                        placeholder="e.g. Acme Corporation"
                    )
                    web_search_query = gr.Textbox(
                        label="Optional Web Research Query",
                        placeholder="e.g. Recent debt restructuring news...",
                        value=""
                    )

                    gr.HTML('<div class="input-group-header">Profitability</div>')
                    with gr.Row():
                        revenue = gr.Number(label="Revenue ($)", value=100.0)
                        net_profit = gr.Number(label="Net Profit ($)", value=8.0)

                    gr.HTML('<div class="input-group-header">Solvency</div>')
                    with gr.Row():
                        total_debt = gr.Number(label="Total Debt ($)", value=60.0)
                        total_assets = gr.Number(label="Total Assets ($)", value=120.0)
                    with gr.Row():
                        ebit = gr.Number(label="EBIT ($)", value=15.0)
                        interest_expense = gr.Number(label="Interest Expense ($)", value=5.0)

                    gr.HTML('<div class="input-group-header">Liquidity</div>')
                    with gr.Row():
                        current_assets = gr.Number(label="Current Assets ($)", value=45.0)
                        current_liabilities = gr.Number(label="Current Liabilities ($)", value=50.0)
                    with gr.Row():
                        inventory = gr.Number(label="Inventory ($)", value=10.0)
                        prepaid_expenses = gr.Number(label="Prepaid Expenses ($)", value=5.0)

                    gr.HTML('<div class="input-group-header">Cash Flow</div>')
                    operating_cash_flow = gr.Number(label="Operating Cash Flow ($)", value=5.0)

                    assess_btn = gr.Button(
                        "Analyze Financial Risk",
                        variant="primary",
                        elem_classes=["analyze-primary-btn"]
                    )

            # Right column: balanced multi-panel dashboard
            with gr.Column(scale=2):
                summary_output = gr.HTML(
                    """
                    <div class="empty-state">
                        Enter financial data and select <strong>Analyze Financial Risk</strong> to begin.
                    </div>
                    """
                )

                with gr.Group(elem_classes=["metrics-panel"]):
                    metrics_output = gr.HTML()

                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Group(elem_classes=["panel-card"]):
                            gr.HTML('<div class="panel-title">Category Risk Breakdown</div><div class="panel-rule"></div>')
                            category_output = gr.HTML()
                    with gr.Column(scale=1):
                        with gr.Group(elem_classes=["panel-card"]):
                            gr.HTML('<div class="panel-title">Key Risk Factors</div><div class="panel-rule"></div>')
                            factors_output = gr.HTML()

                with gr.Group(elem_classes=["panel-card"]):
                    gr.HTML('<div class="panel-title">AI Analyst Insight</div><div class="panel-rule"></div>')
                    explanation_output = gr.Markdown(elem_classes=["insight-markdown"])

                with gr.Group(elem_classes=["panel-card"]):
                    gr.HTML('<div class="panel-title">Agent Activity</div><div class="panel-rule"></div>')
                    activity_output = gr.HTML()

                with gr.Group(elem_classes=["panel-card"]):
                    gr.HTML('<div class="panel-title">Risk Category Criteria</div><div class="panel-rule"></div>')
                    categories_table = gr.Dataframe(
                        headers=["Risk Category", "Risk Level", "Criteria Range"],
                        datatype=["str", "str", "str"],
                        interactive=False
                    )

                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Group(elem_classes=["panel-card"]):
                            gr.HTML('<div class="panel-title">Financial Knowledge (RAG)</div><div class="panel-rule"></div>')
                            rag_output = gr.Markdown()
                    with gr.Column(scale=1):
                        with gr.Group(elem_classes=["panel-card"]):
                            gr.HTML('<div class="panel-title">External Intelligence</div><div class="panel-rule"></div>')
                            web_output = gr.Markdown()

        # Disclaimer Footer
        gr.HTML(
            """
            <div class="disclaimer-banner">
                This application is intended for educational and analytical demonstration purposes only. It does not constitute professional financial, investment, lending, or accounting advice.
            </div>
            """
        )

        # Button Interaction
        assess_btn.click(
            fn=process_assessment,
            inputs=[
                company_name,
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
                interest_expense,
                web_search_query
            ],
            outputs=[
                summary_output,
                metrics_output,
                category_output,
                categories_table,
                factors_output,
                explanation_output,
                activity_output,
                rag_output,
                web_output
            ]
        )

    return ui


if __name__ == "__main__":
    demo = create_ui()
    import sys
    port = 7860
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    try:
        demo.launch(server_name="127.0.0.1", server_port=port, share=False, css=CUSTOM_CSS)
    except Exception as err:
        print(f"Port {port} in use ({err}), trying port {port+1}...")
        demo.launch(server_name="127.0.0.1", server_port=port+1, share=False, css=CUSTOM_CSS)