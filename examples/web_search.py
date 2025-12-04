"""
Web Search Example

Search the web for current information, news, articles, and general content.
"""

from valyu_agentcore import webSearch
from strands import Agent
from strands.models import BedrockModel


def main():
    # Create agent with web search tool
    agent = Agent(
        model=BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            streaming=True,
        ),
        tools=[webSearch()],
        system_prompt="""You are a research assistant with access to web search.
Use web search to find current information, news, and articles.
Always cite your sources using markdown links.""",
    )

    # Example queries
    queries = [
        "Latest developments in AI inference chips",
        "Recent news about SpaceX Starship",
        "Current trends in renewable energy",
    ]

    print("=" * 60)
    print("Web Search Example")
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
