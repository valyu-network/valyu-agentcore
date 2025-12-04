"""
Finance Search Example

Search financial data including stock prices, market data, earnings reports,
and financial metrics.
"""

from valyu_agentcore import financeSearch
from strands import Agent
from strands.models import BedrockModel


def main():
    # Create agent with finance search tool
    agent = Agent(
        model=BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            streaming=True,
        ),
        tools=[financeSearch()],
        system_prompt="""You are a financial analyst with access to market data.
Use finance search to find stock prices, earnings, and financial metrics.
Present data clearly with specific numbers and cite sources.""",
    )

    # Example queries
    queries = [
        "What is Apple's current stock price and recent performance?",
        "NVIDIA's latest quarterly revenue and earnings",
        "Compare Tesla and Rivian market caps",
    ]

    print("=" * 60)
    print("Finance Search Example")
    print("=" * 60)

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 40)
        response = agent(query)
        print(response)
        print()

        # Only run first query in demo
        break


if __name__ == "__main__":
    main()
