import unittest
import sys
import os

# Add root directory to python path
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
from tools.financial_tools import run_financial_analysis
from tools.web_search import search_external_web
from rag.rag_engine import FinancialRAGEngine
from agent import FinancialRiskAgent


class TestFinancialEngine(unittest.TestCase):

    def test_high_risk_company(self):
        """Test exact test company parameters specified in project requirements."""
        data = {
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

        res = run_financial_analysis(**data)
        ratios = res["ratios"]
        risk_cats = res["risk_categories"]

        self.assertAlmostEqual(ratios["profit_margin"], 8.0)
        self.assertAlmostEqual(ratios["debt_to_asset"], 50.0)
        self.assertAlmostEqual(ratios["current_ratio"], 0.90)
        self.assertAlmostEqual(ratios["quick_assets"], 30.0)
        self.assertAlmostEqual(ratios["quick_ratio"], 0.60)
        self.assertAlmostEqual(ratios["debt_to_equity"], 1.00)
        self.assertAlmostEqual(ratios["ocf_ratio"], 0.10)
        self.assertAlmostEqual(ratios["interest_coverage_ratio"], 3.00)

        self.assertEqual(risk_cats["Profitability"], "MEDIUM")
        self.assertEqual(risk_cats["Debt"], "MEDIUM")
        self.assertEqual(risk_cats["Liquidity"], "HIGH")
        self.assertEqual(risk_cats["Quick Liquidity"], "MEDIUM")
        self.assertEqual(risk_cats["Cash Flow"], "HIGH")
        self.assertEqual(risk_cats["Interest Coverage"], "MEDIUM")

        self.assertEqual(res["risk_score"], 14)
        self.assertEqual(res["overall_risk"], "HIGH")

    def test_low_risk_company(self):
        """Test a financially robust company that should be rated LOW risk."""
        data = {
            "revenue": 200,
            "net_profit": 40,      # Profit Margin = 20% (>15% -> LOW)
            "total_debt": 30,
            "total_assets": 150,    # Debt-to-Asset = 20% (<40% -> LOW)
            "current_assets": 100,
            "current_liabilities": 50, # Current Ratio = 2.0 (>=1.5 -> LOW)
            "inventory": 10,
            "prepaid_expenses": 5,  # Quick Assets = 85 -> Quick Ratio = 1.7 (>=1.0 -> LOW)
            "operating_cash_flow": 30, # OCF Ratio = 0.6 (>=0.5 -> LOW)
            "ebit": 50,
            "interest_expense": 5   # Interest Coverage = 10 (>=5 -> LOW)
        }

        res = run_financial_analysis(**data)
        self.assertEqual(res["risk_score"], 6)  # 6 * 1 = 6 points
        self.assertEqual(res["overall_risk"], "LOW")

    def test_medium_risk_company(self):
        """Test a moderately leveraged company that should be rated MEDIUM risk."""
        data = {
            "revenue": 100,
            "net_profit": 10,       # Profit Margin = 10% (MEDIUM)
            "total_debt": 50,
            "total_assets": 100,    # Debt-to-Asset = 50% (MEDIUM)
            "current_assets": 60,
            "current_liabilities": 50, # Current Ratio = 1.2 (MEDIUM)
            "inventory": 15,
            "prepaid_expenses": 5,  # Quick Ratio = 40/50 = 0.8 (MEDIUM)
            "operating_cash_flow": 15, # OCF Ratio = 0.3 (MEDIUM)
            "ebit": 15,
            "interest_expense": 5   # Interest Coverage = 3.0 (MEDIUM)
        }

        res = run_financial_analysis(**data)
        self.assertEqual(res["risk_score"], 12)  # 6 * 2 = 12 points
        self.assertEqual(res["overall_risk"], "MEDIUM")

    def test_invalid_inputs(self):
        """Test validation error triggers on non-positive or invalid inputs."""
        base_data = {
            "revenue": 100, "net_profit": 8, "total_debt": 60, "total_assets": 120,
            "current_assets": 45, "current_liabilities": 50, "inventory": 10,
            "prepaid_expenses": 5, "operating_cash_flow": 5, "ebit": 15, "interest_expense": 5
        }

        # Case 1: Revenue <= 0
        bad_data = base_data.copy()
        bad_data["revenue"] = 0
        with self.assertRaises(ValueError):
            calculate_ratios(**bad_data)

        # Case 2: Total Assets <= 0
        bad_data = base_data.copy()
        bad_data["total_assets"] = -10
        with self.assertRaises(ValueError):
            calculate_ratios(**bad_data)

        # Case 3: Current Liabilities <= 0
        bad_data = base_data.copy()
        bad_data["current_liabilities"] = 0
        with self.assertRaises(ValueError):
            calculate_ratios(**bad_data)

    def test_zero_interest_expense(self):
        """Test zero interest expense handling."""
        data = {
            "revenue": 100, "net_profit": 20, "total_debt": 10, "total_assets": 100,
            "current_assets": 50, "current_liabilities": 25, "inventory": 5,
            "prepaid_expenses": 0, "operating_cash_flow": 20, "ebit": 25, "interest_expense": 0
        }
        res = run_financial_analysis(**data)
        self.assertIsNone(res["ratios"]["interest_coverage_ratio"])
        self.assertEqual(res["risk_categories"]["Interest Coverage"], "LOW")

    def test_rag_engine(self):
        """Test RAG engine retrieval functionality."""
        rag = FinancialRAGEngine()
        snippets = rag.retrieve_relevant_knowledge("Quick ratio inventory liquidity", top_k=2)
        self.assertTrue(len(snippets) > 0)
        self.assertIn("Quick", snippets[0])

    def test_web_search_fallback(self):
        """Test Tavily web search fallback when key is missing or invalid."""
        # Unset key if set
        old_key = os.environ.get("TAVILY_API_KEY")
        if "TAVILY_API_KEY" in os.environ:
            del os.environ["TAVILY_API_KEY"]
            
        res = search_external_web("Test query")
        self.assertIn("Tavily API key", res)
        
        if old_key:
            os.environ["TAVILY_API_KEY"] = old_key

    def test_agent_fallback_mode(self):
        """Test FinancialRiskAgent fallback when Groq key is absent or invalid."""
        agent = FinancialRiskAgent()
        agent.api_key = None # Force fallback mode
        
        data = {
            "revenue": 100, "net_profit": 8, "total_debt": 60, "total_assets": 120,
            "current_assets": 45, "current_liabilities": 50, "inventory": 10,
            "prepaid_expenses": 5, "operating_cash_flow": 5, "ebit": 15, "interest_expense": 5
        }

        res = agent.analyze("Fallback Test Co", data)
        self.assertTrue(res["success"])
        self.assertIn("Deterministic Rule-Based Engine", res["used_model"])
        self.assertIn("HIGH", res["ai_explanation"])


if __name__ == "__main__":
    unittest.main()
