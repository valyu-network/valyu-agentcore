"""
Paper Search Example

Search academic research papers, scholarly articles, and textbooks
across all disciplines from arXiv, PubMed, and other sources.
"""

from valyu_agentcore import paperSearch
from strands import Agent
from strands.models import BedrockModel


def main():
    # Create agent with paper search tool
    agent = Agent(
        model=BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            streaming=True,
        ),
        tools=[paperSearch()],
        system_prompt="""You are a research assistant with access to academic papers.
Use paper search to find scholarly articles and research papers.
Summarize findings and always cite papers with their titles and sources.""",
    )

    # Example queries
    queries = [
        "Recent papers on transformer architecture improvements",
        "Research on CRISPR gene editing efficiency",
        "Studies on quantum computing error correction",
    ]

    print("=" * 60)
    print("Paper Search Example")
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
