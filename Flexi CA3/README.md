# Financial Risk Assessment Agent

> **AI-Powered Explainable Financial Risk Analysis System combining Deterministic Financial Ratios, Retrieval-Augmented Generation (RAG), Optional Tavily Web Research, and OpenAI-Compatible Groq LLM Reasoning.**

---

## 📌 Problem Statement & Motivation
Corporate financial analysis traditionally relies on manual financial ratio calculations and human expert interpretation. While software can compute financial metrics, interpreting multi-factor risk across liquidity, leverage, cash flow, and earning power requires domain knowledge and contextual awareness.

The **Financial Risk Assessment Agent** solves this by establishing a clear two-layer architecture:
1. **Deterministic Core**: Pure Python calculation engine that deterministically computes 9 financial ratios and evaluates 6 risk categories against defined project thresholds, ensuring mathematical accuracy and 0% LLM hallucination in numerical scoring.
2. **Agentic AI Layer**: An LLM agent powered by Groq (OpenAI tool-calling standard) that retrieves domain knowledge via RAG and optional web search via Tavily to deliver explainable, human-readable financial diagnoses and recommendations.

---

## 🏗️ System Architecture

```
                       ┌─────────────────────────┐
                       │       GRADIO GUI        │
                       └────────────┬────────────┘
                                    │
                       ┌────────────▼────────────┐
                       │  FINANCIAL RISK AGENT   │
                       └────────────┬────────────┘
                                    │
    ┌───────────────────────────────┼───────────────────────────────┐
    │                               │                               │
┌───▼──────────────────┐ ┌──────────▼──────────┐ ┌──────────────────▼───┐
│ Financial Calculator │ │ RAG Knowledge Base  │ │ Tavily Web Search  │
│  & Risk Engine (Py)  │ │ (Local Vector Search│ │ (Optional External │
│ (Deterministic Layer)│ │  & Text Retrieval)  │ │  Market Context)   │
└───────────┬──────────┘ └──────────┬──────────┘ └──────────┬────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    │
                       ┌────────────▼────────────┐
                       │   Groq LLM Reasoning    │
                       │ (Tool Interpretation)   │
                       └────────────┬────────────┘
                                    │
                       ┌────────────▼────────────┐
                       │ Explainable Dashboard   │
                       │ Ratios, Risk Badges,    │
                       │  AI Explanations & RAG  │
                       └─────────────────────────┘
```

---

## ⚡ Key Features

- **Deterministic Financial Engine**: Computes Profit Margin, Debt-to-Asset Ratio, Current Ratio, Quick Assets, Quick Ratio, Debt-to-Equity Ratio, Operating Cash Flow Ratio, and Interest Coverage Ratio.
- **Categorical Risk Classification**: Categorizes Profitability, Debt, Liquidity, Quick Liquidity, Cash Flow, and Interest Coverage into LOW (1 pt), MEDIUM (2 pts), or HIGH (3 pts) risk.
- **Composite Risk Scoring**: Calculates overall risk level (LOW <= 50%, MEDIUM <= 75%, HIGH > 75% of max 18 points).
- **Retrieval-Augmented Generation (RAG)**: Integrates a local TF-IDF / vector knowledge engine containing structured financial concept explanations.
- **Tavily Web Search Integration**: Optional tool to fetch current company news, market context, and industry trends.
- **Groq LLM Integration**: Uses OpenAI-compatible endpoints (`https://api.groq.com/openai/v1`) for fast, explainable AI diagnoses.
- **Offline / API Fallback Safety**: If API keys are missing or services fail, the system falls back to a rule-based explanation engine so numerical assessments are never lost.
- **Interactive Gradio GUI**: Clean tabbed web interface with pre-filled test data, summary risk badges, dataframes, AI explanations, and source citations.

---

## 📊 How the Risk Score Works

Each of the 6 core financial categories is assigned a risk level based on project assessment criteria:

| Category | Low Risk (1 pt) | Medium Risk (2 pts) | High Risk (3 pts) |
| :--- | :--- | :--- | :--- |
| **Profitability (Profit Margin)** | > 15% | 5% – 15% | < 5% |
| **Debt & Solvency (Debt-to-Asset)** | < 40% | 40% – 60% | > 60% |
| **Liquidity (Current Ratio)** | >= 1.5 | 1.0 – 1.49 | < 1.0 |
| **Quick Liquidity (Quick Ratio)** | >= 1.0 | 0.5 – 0.99 | < 0.5 |
| **Cash Flow (OCF Ratio)** | >= 0.5 | 0.2 – 0.49 | < 0.2 |
| **Interest Coverage (EBIT/Interest)** | >= 5.0 | 2.0 – 4.99 | < 2.0 |

- **Maximum Composite Score**: 6 categories × 3 points = **18 points**
- **Overall Risk Thresholds**:
  - Score <= 9 (<= 50%): **LOW Risk**
  - Score 10 – 13 (<= 75%): **MEDIUM Risk**
  - Score 14 – 18 (> 75%): **HIGH Risk**

*Note: Debt-to-Equity is calculated and displayed as an informational metric but excluded from the composite risk score to prevent double-counting leverage already evaluated in the Debt-to-Asset ratio.*

---

## 🛠️ Technology Stack

- **GUI Framework**: Gradio
- **Language**: Python 3.10+
- **LLM Interface**: OpenAI Python SDK connecting to Groq (`https://api.groq.com/openai/v1`)
- **RAG Engine**: Scikit-Learn (TF-IDF & Cosine Similarity vector matching) + Markdown Knowledge Base
- **Web Search**: Tavily API (`tavily-python`)
- **Testing**: PyTest & Unittest

---

## 🚀 Quick Start & Installation

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/your-username/financial-risk-assessment-agent.git
cd financial-risk-assessment-agent
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables (`.env`)
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
TAVILY_API_KEY=tvly_your_tavily_api_key_here  # Optional
```

### 3. Run Automated Unit Tests
```bash
python -m unittest discover tests
```

### 4. Launch Gradio Web Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:7860`.

---

## ⚠️ Important Educational Disclaimer

This project is built strictly for **educational and academic demonstration purposes**. It does not constitute professional financial, investment, accounting, or lending advice. Assessment thresholds represent project evaluation criteria rather than universal financial regulations.
