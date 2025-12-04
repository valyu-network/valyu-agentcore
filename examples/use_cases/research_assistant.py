"""
Research Assistant Agent

An academic and technical research agent that searches papers,
patents, and web sources to provide comprehensive research summaries.

This example demonstrates combining Valyu's research-focused tools
for literature review and technical research use cases.

Usage:
    export VALYU_API_KEY=your-api-key
    python research_assistant.py "transformer architecture improvements"
"""

import sys
from strands import Agent
from strands.models import BedrockModel
from valyu_agentcore import paperSearch, patentSearch, webSearch


SYSTEM_PROMPT = """You are a research assistant helping with academic and technical research.
Your role is to find, synthesize, and summarize research across multiple sources.

When researching a topic:

1. **Search Strategy**
   - Use paper search for peer-reviewed academic work
   - Use patent search for technical innovations and prior art
   - Use web search for recent developments and applications

2. **Organize Findings**
   - Key Papers: Most cited/relevant academic papers with summaries
   - Recent Advances: Work from the last 1-2 years
   - Patents: Relevant patents and their claims
   - Practical Applications: Real-world implementations

3. **Synthesis**
   - Identify common themes and consensus
   - Note disagreements or competing approaches
   - Highlight open questions and research gaps

4. **Citations**
   - Always cite sources with authors and dates
   - Link to papers when available
   - Note if sources are preprints vs published
"""


def create_research_assistant():
    """Create a research assistant agent."""
    return Agent(
        model=BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            temperature=0.2,
        ),
        system_prompt=SYSTEM_PROMPT,
        tools=[
            paperSearch(max_num_results=10),
            patentSearch(max_num_results=5),
            webSearch(max_num_results=5),
        ],
    )


def research(query: str) -> str:
    """Run research on a topic."""
    agent = create_research_assistant()
    response = agent(query)
    return str(response)


EXAMPLE_QUERIES = {
    "literature_review": "Survey recent advances in large language model efficiency and optimization",
    "prior_art": "Search for patents related to retrieval augmented generation (RAG)",
    "state_of_the_art": "What is the current state of the art in protein structure prediction?",
    "technical_comparison": "Compare different approaches to vector database indexing",
}


def main():
    if len(sys.argv) < 2:
        print("Research Assistant Agent")
        print("=" * 50)
        print("\nUsage: python research_assistant.py <topic>")
        print("\nExample queries:")
        for name, query in EXAMPLE_QUERIES.items():
            print(f"\n  {name}:")
            print(f"    python research_assistant.py \"{query}\"")
        return

    query = " ".join(sys.argv[1:])

    print("=" * 60)
    print("Research Assistant Agent")
    print("=" * 60)
    print(f"\nTopic: {query}")
    print("\nResearching...\n")
    print("-" * 60)

    response = research(query)
    print(response)


if __name__ == "__main__":
    main()
