import os
import json
from dotenv import load_dotenv
from datetime import date

from tools.financial_tools import run_financial_analysis, TOOL_CALCULATE_FINANCIAL_RISK
from tools.web_search import search_external_web, TOOL_WEB_SEARCH
from rag.rag_engine import query_financial_knowledge, TOOL_RAG_SEARCH, get_rag_engine

load_dotenv()

# Supported Groq Models with Tool Calling Support
GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b"
]

MAX_TOOL_ROUNDS = 5


class FinancialRiskAgent:
    """
    Financial Risk Assessment Agent utilizing Groq LLM (OpenAI-compatible) and dynamic tool calling.
    Combines deterministic financial ratio calculations with RAG domain knowledge retrieval
    and optional Tavily web search, orchestrated dynamically by the LLM.
    """

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
        self.rag_engine = get_rag_engine()

    def analyze(self, company_name: str = "", financial_data: dict = None, web_search_query: str = "", user_prompt: str = "") -> dict:
        """
        Executes end-to-end Financial Risk Assessment using an agentic LLM tool-calling loop.
        
        Parameters:
        - company_name: Name of target company.
        - financial_data: Dict of 11 financial metrics.
        - web_search_query: Optional user request for web search.
        - user_prompt: Optional direct query string.
        """
        agent_steps = []
        target_company = company_name.strip() if company_name else "Target Company"
        agent_steps.append(f"Received financial assessment request for '{target_company}'")

        # Prepare initial prompt context
        initial_user_message = self._build_user_message(
            company_name=company_name,
            financial_data=financial_data,
            web_search_query=web_search_query,
            user_prompt=user_prompt
        )

        ai_explanation = None
        used_model = None
        calc_results = None
        rag_sources_list = []
        web_sources_list = []

        # Attempt LLM Agent Tool Calling via Groq if API key is present
        if self.api_key and self.api_key.strip():
            ai_explanation, used_model, calc_results, rag_sources_list, web_sources_list = self._call_groq_agent_loop(
                user_message=initial_user_message,
                financial_data=financial_data,
                agent_steps=agent_steps
            )

        # Fallback if Groq key is missing or API call failed
        if not ai_explanation:
            agent_steps.append("Groq API unavailable or failed. Utilizing deterministic rule-based fallback engine.")
            fallback_res = self._run_fallback(
                company_name=company_name,
                financial_data=financial_data,
                web_search_query=web_search_query
            )
            calc_results = fallback_res["calc_results"]
            ai_explanation = fallback_res["ai_explanation"]
            rag_sources_text = fallback_res["rag_sources"]
            web_sources_text = fallback_res["web_sources"]
            used_model = "Deterministic Rule-Based Engine (AI Offline/Fallback)"
        else:
            # Format RAG and Web sources from tool execution lists
            rag_sources_text = (
                "**RAG Domain Knowledge Retrieved:**\n\n" + "\n\n---\n\n".join(rag_sources_list)
                if rag_sources_list else "RAG Tool was not called for this assessment."
            )
            web_sources_text = (
                "\n\n---\n\n".join(web_sources_list)
                if web_sources_list else "Tavily Web Search Tool was not called for this assessment."
            )

        return {
            "success": True,
            "company_name": target_company,
            "calc_results": calc_results,
            "ai_explanation": ai_explanation,
            "rag_sources": rag_sources_text,
            "web_sources": web_sources_text,
            "used_model": used_model,
            "agent_steps": agent_steps
        }

    def _build_user_message(self, company_name: str, financial_data: dict, web_search_query: str, user_prompt: str) -> str:
        parts = []
        if user_prompt and user_prompt.strip():
            parts.append(f"User Request: {user_prompt.strip()}")
        else:
            parts.append(f"Target Company Name: {company_name or 'Target Company'}")
            parts.append("Task: Conduct a comprehensive financial risk assessment for this company.")

        if financial_data:
            parts.append("Supplied Financial Data:")
            for k, v in financial_data.items():
                parts.append(f"  - {k}: {v}")
            parts.append("Use the run_financial_analysis tool with these numerical inputs to compute exact ratios and risk scores.")

        if web_search_query and web_search_query.strip():
            parts.append(f"User requested external web search context: '{web_search_query.strip()}'")

        return "\n".join(parts)

    def _call_groq_agent_loop(self, user_message: str, financial_data: dict, agent_steps: list):
        """Invoke Groq LLM using OpenAI-compatible function tool calling loop."""
        try:
            from openai import OpenAI
            client = OpenAI(base_url=self.base_url, api_key=self.api_key.strip())

            tools = [
                TOOL_CALCULATE_FINANCIAL_RISK,
                TOOL_RAG_SEARCH,
                TOOL_WEB_SEARCH
            ]
            current_date = date.today().isoformat()
            current_year = date.today().year
            
            system_prompt = f"""You are an expert Financial Risk Assessment Agent.

Current date: {current_date}
Current year: {current_year}
Available Tools:
1. `run_financial_analysis`: The AUTHORITATIVE ground truth tool for calculating financial ratios, category risk levels, composite risk scores, and overall risk.
   - NEVER recalculate or invent financial ratios yourself. Always call this tool when company numerical inputs are provided.
2. `query_financial_knowledge`: RAG retrieval tool for searching local financial domain knowledge.
   - Use this tool to retrieve explanations for financial metrics, risk thresholds, liquidity concepts, and financial distress mechanics.
3. `search_external_web`: Tavily web search tool for searching recent financial news, company updates, or market background.
   - Use this tool ONLY when external/current information is useful or explicitly requested.
   - When searching for "recent", "latest", or "current" information, use the current year ({current_year}) where a year is useful. Do not assume an outdated year.

Authoritative Financial Definitions:
- Operating Cash Flow (OCF) Ratio = Operating Cash Flow / Current Liabilities.
- NEVER describe the project's OCF Ratio as Operating Cash Flow / Revenue.
- All ratios, scores, and risk classifications returned by `run_financial_analysis` are authoritative. Do not recalculate, reinterpret, or replace their formulas.

Guidelines:
- You are free to call multiple tools as needed. Deciding which tools to call is your responsibility as an agent.
- Once you have gathered sufficient information from tools, synthesize an objective, structured, and educational financial risk assessment.
- Clearly distinguish calculated financial figures (from run_financial_analysis) from general domain concepts (RAG) and recent news (web search).
"""

            for model_name in GROQ_MODELS:
                try:
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ]

                    calc_results = None
                    rag_sources = []
                    web_sources = []
                    rounds = 0

                    while rounds < MAX_TOOL_ROUNDS:
                        rounds += 1
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=messages,
                            tools=tools,
                            tool_choice="auto",
                            temperature=0.2,
                            max_tokens=1200
                        )

                        choice = response.choices[0]
                        message = choice.message

                        # Check if model requested tool calls
                        if message.tool_calls:
                            # Append assistant's response message containing tool_calls to conversation
                            messages.append(message)

                            for tool_call in message.tool_calls:
                                function_name = tool_call.function.name
                                tool_call_id = tool_call.id
                                
                                try:
                                    arguments = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                                except Exception as json_err:
                                    arguments = {}

                                # Tool Dispatcher
                                if function_name == "run_financial_analysis":
                                    agent_steps.append("Calling financial risk analysis tool")
                                    try:
                                        # Supply any missing arguments from financial_data if available
                                        if financial_data:
                                            for key, val in financial_data.items():
                                                if key not in arguments:
                                                    arguments[key] = val

                                        tool_result = run_financial_analysis(**arguments)
                                        calc_results = tool_result
                                        agent_steps.append("Financial analysis tool completed")
                                        content_str = json.dumps(tool_result)
                                    except Exception as err:
                                        agent_steps.append(f"Financial analysis tool error: {str(err)}")
                                        content_str = json.dumps({"error": str(err)})

                                elif function_name == "query_financial_knowledge":
                                    query_str = arguments.get("query", "financial ratio risk evaluation")
                                    agent_steps.append(f"Calling financial knowledge RAG tool (query: '{query_str}')")
                                    try:
                                        tool_result = query_financial_knowledge(query_str)
                                        rag_sources.append(tool_result)
                                        agent_steps.append("RAG retrieval completed")
                                        content_str = tool_result
                                    except Exception as err:
                                        agent_steps.append(f"RAG tool error: {str(err)}")
                                        content_str = f"RAG search error: {str(err)}"

                                elif function_name == "search_external_web":
                                    query_str = arguments.get("query", "")
                                    agent_steps.append(f"Calling Tavily web search tool (query: '{query_str}')")
                                    try:
                                        tool_result = search_external_web(query_str)
                                        web_sources.append(tool_result)
                                        agent_steps.append("Web search completed")
                                        content_str = tool_result
                                    except Exception as err:
                                        agent_steps.append(f"Web search tool error: {str(err)}")
                                        content_str = f"Web search error: {str(err)}"

                                else:
                                    agent_steps.append(f"Unknown tool requested: {function_name}")
                                    content_str = json.dumps({"error": f"Unknown tool name: {function_name}"})

                                # Append tool result back to messages
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call_id,
                                    "name": function_name,
                                    "content": content_str
                                })
                        else:
                            # Final response text generated by assistant
                            final_text = message.content
                            if final_text and final_text.strip():
                                agent_steps.append("Generating final assessment")
                                return final_text, model_name, calc_results, rag_sources, web_sources
                            else:
                                break

                    # If max rounds reached and last message has content
                    if messages:
                        last_msg = messages[-1]
                        last_content = getattr(last_msg, "content", None) if not isinstance(last_msg, dict) else last_msg.get("content")
                        if last_content:
                            agent_steps.append("Generating final assessment")
                            return last_content, model_name, calc_results, rag_sources, web_sources

                except Exception as model_err:
                    print(f"Model {model_name} tool calling failed: {model_err}")
                    continue

        except Exception as e:
            print(f"Groq Agent API Exception: {e}")

        return None, None, None, [], []

    def _run_fallback(self, company_name: str, financial_data: dict, web_search_query: str) -> dict:
        """Deterministic rule-based fallback when Groq LLM API is unavailable."""
        calc_results = None
        rag_sources_text = ""
        web_sources_text = ""

        if financial_data:
            try:
                calc_results = run_financial_analysis(**financial_data)
            except Exception as e:
                calc_results = None

        if calc_results:
            rag_snippets = self.rag_engine.get_knowledge_summary_for_ratios(calc_results["risk_categories"])
            rag_sources_text = f"**RAG Domain Knowledge Retrieved:**\n\n{rag_snippets}"
            ai_explanation = self._generate_fallback_explanation(company_name, calc_results, rag_snippets)
        else:
            rag_sources_text = "RAG retrieval unavailable."
            ai_explanation = "Financial calculation and AI assessment unavailable due to missing or invalid inputs."

        if web_search_query and web_search_query.strip():
            web_sources_text = search_external_web(web_search_query.strip())
        else:
            web_sources_text = "No web search query provided or Tavily key unavailable."

        return {
            "calc_results": calc_results,
            "ai_explanation": ai_explanation,
            "rag_sources": rag_sources_text,
            "web_sources": web_sources_text
        }

    def _generate_fallback_explanation(self, company_name: str, calc_results: dict, rag_snippets: str) -> str:
        """Deterministic rule-based explanation generator used when LLM API is unavailable."""
        high_risks = calc_results["high_risk_factors"]
        med_risks = calc_results["medium_risk_factors"]
        ratios = calc_results["ratios"]

        lines = [
            "### Executive Summary",
            f"**{company_name or 'Target Company'}** has been evaluated with an **Overall Risk Level of {calc_results['overall_risk']}** based on a composite risk score of **{calc_results['risk_score']} out of {calc_results['maximum_score']} points** under project assessment criteria.\n",
            "### Primary Risk Drivers",
        ]

        if high_risks:
            lines.append(f"The primary areas of severe concern (HIGH Risk) include: **{', '.join(high_risks)}**.")
        else:
            lines.append("No individual category was flagged as HIGH risk.")

        if med_risks:
            lines.append(f"Categories flagged with moderate concern (MEDIUM Risk) include: **{', '.join(med_risks)}**.")

        lines.append("\n### Detailed Ratio Analysis & Financial Mechanisms")

        if "Liquidity" in high_risks or "Liquidity" in med_risks:
            lines.append(f"- **Liquidity (Current Ratio = {ratios['current_ratio']:.2f})**: A ratio below 1.5 indicates that short-term liabilities may exceed short-term liquid assets under project thresholds, creating potential working capital stress.")

        if "Quick Liquidity" in high_risks or "Quick Liquidity" in med_risks:
            lines.append(f"- **Quick Liquidity (Quick Ratio = {ratios['quick_ratio']:.2f})**: Excludes inventory and prepaid expenses. A ratio below 1.0 indicates dependency on inventory liquidation to cover immediate debts.")

        if "Cash Flow" in high_risks or "Cash Flow" in med_risks:
            lines.append(f"- **Operating Cash Flow (OCF Ratio = {ratios['ocf_ratio']:.2f})**: An OCF ratio below 0.5 indicates weak operational cash generation relative to short-term liabilities.")

        if "Profitability" in high_risks or "Profitability" in med_risks:
            lines.append(f"- **Profitability (Profit Margin = {ratios['profit_margin']:.2f}%)**: Profit margin below 15% indicates limited margin protection against operational cost inflation or demand drop.")

        if "Debt" in high_risks or "Debt" in med_risks:
            lines.append(f"- **Leverage (Debt-to-Asset = {ratios['debt_to_asset']:.2f}%)**: High debt proportion increases fixed obligations and financial vulnerability.")

        if "Interest Coverage" in high_risks or "Interest Coverage" in med_risks:
            cov = f"{ratios['interest_coverage_ratio']:.2f}" if ratios['interest_coverage_ratio'] is not None else 'N/A'
            lines.append(f"- **Interest Coverage ({cov})**: Low coverage indicates thin safety margins between operating earnings (EBIT) and mandatory interest obligations.")

        lines.append("\n### Actionable Risk Mitigation Recommendations")
        lines.append("1. **Strengthen Short-term Working Capital**: Restructure short-term liabilities or accelerate receivables collection to elevate current and quick ratios.")
        lines.append("2. **Enhance Operational Cash Generation**: Focus on core operational cash flows and inventory turnover optimization.")
        lines.append("3. **De-leverage Capital Structure**: Limit additional debt issuance until interest coverage and debt-to-asset ratios improve.")

        lines.append("\n> *Note: This explanation was generated using the deterministic fallback engine as the external Groq LLM service was not reached.*")

        return "\n".join(lines)

