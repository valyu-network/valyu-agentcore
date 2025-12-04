"""
Bio Search Example

Search biomedical literature including PubMed articles, clinical trials,
and FDA drug information.
"""

from valyu_agentcore import bioSearch
from strands import Agent
from strands.models import BedrockModel


def main():
    # Create agent with bio search tool
    agent = Agent(
        model=BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            streaming=True,
        ),
        tools=[bioSearch()],
        system_prompt="""You are a biomedical research assistant.
Use bio search to find clinical trials, FDA drug labels, and medical research.
Present findings clearly and cite all sources.""",
    )

    # Example queries
    queries = [
        "Phase 3 clinical trials for melanoma immunotherapy",
        "FDA approved treatments for type 2 diabetes in 2024",
        "Research on mRNA vaccine technology",
    ]

    print("=" * 60)
    print("Bio Search Example")
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
