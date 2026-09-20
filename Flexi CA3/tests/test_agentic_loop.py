import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add root directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent import FinancialRiskAgent


class TestAgenticLoop(unittest.TestCase):

    def setUp(self):
        self.agent = FinancialRiskAgent()
        self.sample_financial_data = {
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

    def test_agent_steps_logging_fallback(self):
        """Test agent step logging in fallback mode (when Groq API key is absent)."""
        agent = FinancialRiskAgent()
        agent.api_key = None  # Ensure fallback mode

        res = agent.analyze(
            company_name="Test Alpha",
            financial_data=self.sample_financial_data
        )
        self.assertTrue(res["success"])
        self.assertIn("agent_steps", res)
        self.assertIsInstance(res["agent_steps"], list)
        self.assertTrue(len(res["agent_steps"]) > 0)
        print("\n--- FALLBACK AGENT STEPS LOGGING TEST ---")
        for idx, step in enumerate(res["agent_steps"], 1):
            print(f"{idx}. {step}")

    @patch("openai.OpenAI")
    def test_mock_groq_tool_calling_sequence_a(self, mock_openai_cls):
        """Mock Test A: LLM calls run_financial_analysis -> query_financial_knowledge -> final answer."""
        agent = FinancialRiskAgent()
        agent.api_key = "mock_groq_key"

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        # Round 1 response: LLM calls run_financial_analysis
        resp1 = MagicMock()
        tc1 = MagicMock()
        tc1.id = "call_calc_001"
        tc1.function.name = "run_financial_analysis"
        tc1.function.arguments = json.dumps(self.sample_financial_data)
        resp1.choices = [MagicMock(message=MagicMock(tool_calls=[tc1], content=None))]

        # Round 2 response: LLM calls query_financial_knowledge
        resp2 = MagicMock()
        tc2 = MagicMock()
        tc2.id = "call_rag_002"
        tc2.function.name = "query_financial_knowledge"
        tc2.function.arguments = json.dumps({"query": "liquidity ratio current ratio high risk"})
        resp2.choices = [MagicMock(message=MagicMock(tool_calls=[tc2], content=None))]

        # Round 3 response: LLM gives final text answer
        resp3 = MagicMock()
        resp3.choices = [MagicMock(message=MagicMock(tool_calls=None, content="### Executive Summary\nOverall Risk Level: HIGH"))]

        mock_client.chat.completions.create.side_effect = [resp1, resp2, resp3]

        print("\n==========================================")
        print("AGENT TEST A (Mock Tool Calling Sequence):")
        print("==========================================")

        res = agent.analyze(
            company_name="Test Corp A",
            financial_data=self.sample_financial_data
        )

        self.assertTrue(res["success"])
        self.assertIsNotNone(res["calc_results"])
        self.assertEqual(res["calc_results"]["risk_score"], 14)
        self.assertEqual(res["calc_results"]["overall_risk"], "HIGH")

        print("Agent activity log:")
        for idx, step in enumerate(res["agent_steps"], 1):
            print(f"{idx}. {step}")

        steps_str = " ".join(res["agent_steps"]).lower()
        self.assertIn("financial risk analysis tool", steps_str)
        self.assertIn("rag", steps_str)
        self.assertNotIn("tavily", steps_str)
        self.assertNotIn("web search tool", steps_str)

    @patch("openai.OpenAI")
    def test_mock_groq_tool_calling_sequence_b(self, mock_openai_cls):
        """Mock Test B: LLM calls run_financial_analysis -> query_financial_knowledge -> search_external_web -> final answer."""
        agent = FinancialRiskAgent()
        agent.api_key = "mock_groq_key"

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        # Round 1: run_financial_analysis
        resp1 = MagicMock()
        tc1 = MagicMock()
        tc1.id = "call_calc_001"
        tc1.function.name = "run_financial_analysis"
        tc1.function.arguments = json.dumps(self.sample_financial_data)
        resp1.choices = [MagicMock(message=MagicMock(tool_calls=[tc1], content=None))]

        # Round 2: query_financial_knowledge
        resp2 = MagicMock()
        tc2 = MagicMock()
        tc2.id = "call_rag_002"
        tc2.function.name = "query_financial_knowledge"
        tc2.function.arguments = json.dumps({"query": "cash flow ratio"})
        resp2.choices = [MagicMock(message=MagicMock(tool_calls=[tc2], content=None))]

        # Round 3: search_external_web
        resp3 = MagicMock()
        tc3 = MagicMock()
        tc3.id = "call_web_003"
        tc3.function.name = "search_external_web"
        tc3.function.arguments = json.dumps({"query": "Test Corp B debt news"})
        resp3.choices = [MagicMock(message=MagicMock(tool_calls=[tc3], content=None))]

        # Round 4: final answer
        resp4 = MagicMock()
        resp4.choices = [MagicMock(message=MagicMock(tool_calls=None, content="### Assessment with Web Context\nHigh risk level."))]

        mock_client.chat.completions.create.side_effect = [resp1, resp2, resp3, resp4]

        print("\n==========================================")
        print("AGENT TEST B (Mock Tool Calling Sequence):")
        print("==========================================")

        res = agent.analyze(
            company_name="Test Corp B",
            financial_data=self.sample_financial_data,
            web_search_query="Test Corp B debt news"
        )

        self.assertTrue(res["success"])
        print("Agent activity log:")
        for idx, step in enumerate(res["agent_steps"], 1):
            print(f"{idx}. {step}")

        steps_str = " ".join(res["agent_steps"]).lower()
        self.assertIn("financial risk analysis tool", steps_str)
        self.assertIn("rag", steps_str)
        self.assertIn("tavily", steps_str)

    @patch("openai.OpenAI")
    def test_mock_groq_tool_calling_sequence_c(self, mock_openai_cls):
        """Mock Test C: Concept explanation request -> query_financial_knowledge -> final answer."""
        agent = FinancialRiskAgent()
        agent.api_key = "mock_groq_key"

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        # Round 1: query_financial_knowledge
        resp1 = MagicMock()
        tc1 = MagicMock()
        tc1.id = "call_rag_001"
        tc1.function.name = "query_financial_knowledge"
        tc1.function.arguments = json.dumps({"query": "quick ratio below 1 liquidity pressure"})
        resp1.choices = [MagicMock(message=MagicMock(tool_calls=[tc1], content=None))]

        # Round 2: final answer
        resp2 = MagicMock()
        resp2.choices = [MagicMock(message=MagicMock(tool_calls=None, content="A quick ratio below 1 means liquid assets are less than short-term liabilities."))]

        mock_client.chat.completions.create.side_effect = [resp1, resp2]

        print("\n==========================================")
        print("AGENT TEST C (Mock Concept Explanation):")
        print("==========================================")

        res = agent.analyze(
            user_prompt="Explain why a quick ratio below 1 can indicate liquidity pressure."
        )

        self.assertTrue(res["success"])
        print("Agent activity log:")
        for idx, step in enumerate(res["agent_steps"], 1):
            print(f"{idx}. {step}")

        steps_str = " ".join(res["agent_steps"]).lower()
        self.assertIn("rag", steps_str)
        self.assertNotIn("financial risk analysis tool", steps_str)

    def test_live_groq_tool_calling_if_key_available(self):
        """Live integration test executed if GROQ_API_KEY is configured in environment."""
        if not self.agent.api_key:
            self.skipTest("GROQ_API_KEY not set in environment.")

        print("\n==========================================")
        print("LIVE GROQ AGENT INTEGRATION TEST")
        print("==========================================")
        res = self.agent.analyze(
            company_name="Live Test Corp",
            financial_data=self.sample_financial_data
        )

        self.assertTrue(res["success"])
        print(f"Used Model: {res['used_model']}")
        print("\nLive Agent activity log:")
        for idx, step in enumerate(res["agent_steps"], 1):
            print(f"{idx}. {step}")


if __name__ == "__main__":
    unittest.main()
