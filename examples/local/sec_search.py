"""
SEC Search Example

Search SEC filings including 10-K, 10-Q, 8-K, and other regulatory documents.
"""

from valyu_agentcore import secSearch
from strands import Agent
from strands.models import BedrockModel


def main():
    # Create agent with SEC search tool
    agent = Agent(
        model=BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            streaming=True,
        ),
        tools=[secSearch()],
        system_prompt="""You are a financial analyst specializing in SEC filings.
Use SEC search to find regulatory filings and disclosures.
Extract key information and cite filing types and dates.""",
    )

    # Example queries
    queries = [
        "Summarize Tesla's latest 10-K risk factors",
        "Recent 8-K filings from major tech companies",
        "Apple's executive compensation from proxy statement",
    ]

    print("=" * 60)
    print("SEC Search Example")
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
