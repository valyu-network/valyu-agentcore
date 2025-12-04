"""
Patent Search Example

Search patent databases for inventions, innovations, and intellectual property
from USPTO and other patent offices.
"""

from valyu_agentcore import patentSearch
from strands import Agent
from strands.models import BedrockModel


def main():
    # Create agent with patent search tool
    agent = Agent(
        model=BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            streaming=True,
        ),
        tools=[patentSearch(max_num_results=5)],
        system_prompt="""You are a patent research specialist.
Use patent search to find patents and intellectual property.
Summarize key claims and cite patent numbers.""",
    )

    # Example queries
    queries = [
        "Patents for solid-state battery technology",
        "Recent AI chip architecture patents",
        "Autonomous vehicle sensor fusion patents",
    ]

    print("=" * 60)
    print("Patent Search Example")
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
