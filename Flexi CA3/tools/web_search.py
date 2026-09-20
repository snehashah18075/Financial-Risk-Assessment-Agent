import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def search_external_web(query: str) -> str:
    """
    Optional Tavily Web Search Tool.
    Searches recent news, company background, or market trends when requested by the agent or user.
    If Tavily API key is missing or call fails, gracefully returns a clear status message.
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key or tavily_api_key.strip() == "":
        return "Web search status: Tavily API key (TAVILY_API_KEY) is not configured in .env. Skipping external web research."

    # Attempt to search using tavily-python package or direct HTTP API call
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=tavily_api_key.strip())
        response = client.search(query=query, search_depth="basic", max_results=3)
        
        results = []
        if isinstance(response, dict) and "results" in response:
            for item in response["results"]:
                title = item.get("title", "No Title")
                content = item.get("content", "")
                url = item.get("url", "")
                results.append(f"• **{title}**\n  {content}\n  Source: {url}")
        
        if results:
            return "External Web Research Results:\n\n" + "\n\n".join(results)
        else:
            return "Web search completed, but no relevant external information was found."
            
    except Exception as e:
        return f"Web search status: Attempted web search for '{query}' but encountered an issue ({str(e)}). External web search unavailable."


# OpenAI tool schema definition for web search
TOOL_WEB_SEARCH = {
    "type": "function",
    "function": {
        "name": "search_external_web",
        "description": "Searches recent company financial news, industry background, or market context using Tavily.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for company news, industry metrics, or financial updates."
                }
            },
            "required": ["query"]
        }
    }
}
