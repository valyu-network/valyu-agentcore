"""
Economics Search Example

Search economic data including labor statistics, Federal Reserve data,
World Bank indicators, and US federal spending.
"""

from valyu_agentcore import economicsSearch
from strands import Agent
from strands.models import BedrockModel


def main():
    # Create agent with economics search tool
    agent = Agent(
        model=BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            streaming=True,
        ),
        tools=[economicsSearch()],
        system_prompt="""You are an economist with access to economic data.
Use economics search to find labor statistics, FRED data, and economic indicators.
Present data with specific numbers and trends.""",
    )

    # Example queries
    queries = [
        "US unemployment rate trend since 2020",
        "Current CPI inflation data",
        "Federal Reserve interest rate decisions in 2024",
    ]

    print("=" * 60)
    print("Economics Search Example")
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
