"""
Financial Analyst Agent

A comprehensive financial research agent that combines SEC filings,
market data, and web search to provide deep financial analysis.

This example demonstrates combining multiple Valyu tools for a real-world
enterprise use case.

Usage:
    export VALYU_API_KEY=your-api-key
    python financial_analyst.py "Analyze NVIDIA's competitive position"
"""

import sys
from strands import Agent
from strands.models import BedrockModel
from valyu_agentcore import financeSearch, secSearch, webSearch


SYSTEM_PROMPT = """You are a senior financial analyst at a top investment firm.
Your role is to provide comprehensive, data-driven analysis for investment decisions.

When analyzing a company or financial topic:

1. **Gather Data First**
   - Use SEC filings (10-K, 10-Q) for official financial data
   - Use financial search for current market data and metrics
   - Use web search for recent news and developments

2. **Structure Your Analysis**
   - Executive Summary: Key findings in 2-3 sentences
   - Financial Health: Revenue, margins, cash flow, debt levels
   - Competitive Position: Market share, moat, key competitors
   - Risk Factors: From SEC filings and market conditions
   - Recent Developments: News, earnings, strategic moves

3. **Be Specific**
   - Cite specific numbers and sources
   - Compare metrics to industry averages when relevant
   - Note any data limitations or uncertainties

4. **Professional Tone**
   - Write for institutional investors
   - Avoid speculation without supporting data
   - Distinguish between facts and analysis
"""


def create_financial_analyst():
    """Create a financial analyst agent with all relevant tools."""
    return Agent(
        model=BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            temperature=0.3,  # Lower temperature for factual analysis
        ),
        system_prompt=SYSTEM_PROMPT,
        tools=[
            financeSearch(max_num_results=10),
            secSearch(max_num_results=5),
            webSearch(max_num_results=5),
        ],
    )


def analyze(query: str) -> str:
    """Run financial analysis on a query."""
    agent = create_financial_analyst()
    response = agent(query)
    return str(response)


# Example queries for different analysis types
EXAMPLE_QUERIES = {
    "company_deep_dive": "Provide a comprehensive analysis of NVIDIA including financials, competitive position, and risk factors",
    "earnings_analysis": "Analyze Apple's most recent quarterly earnings and compare to analyst expectations",
    "sector_comparison": "Compare the financial health of major cloud providers: AWS, Azure, and Google Cloud",
    "risk_assessment": "What are the key risk factors for Tesla from their latest 10-K?",
    "valuation": "Is Microsoft fairly valued based on current financials and growth prospects?",
}


def main():
    if len(sys.argv) < 2:
        print("Financial Analyst Agent")
        print("=" * 50)
        print("\nUsage: python financial_analyst.py <query>")
        print("\nExample queries:")
        for name, query in EXAMPLE_QUERIES.items():
            print(f"\n  {name}:")
            print(f"    python financial_analyst.py \"{query}\"")
        return

    query = " ".join(sys.argv[1:])

    print("=" * 60)
    print("Financial Analyst Agent")
    print("=" * 60)
    print(f"\nQuery: {query}")
    print("\nAnalyzing...\n")
    print("-" * 60)

    response = analyze(query)
    print(response)


if __name__ == "__main__":
    main()
