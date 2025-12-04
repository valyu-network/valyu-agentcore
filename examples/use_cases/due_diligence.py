"""
Due Diligence Agent

A comprehensive due diligence agent for M&A, investment, or partnership
evaluation. Combines SEC filings, news, financial data, and patents
for thorough assessment.

This example demonstrates enterprise-grade due diligence workflows
using multiple Valyu tools.

Usage:
    export VALYU_API_KEY=your-api-key
    python due_diligence.py "Anthropic"
"""

import sys
from strands import Agent
from strands.models import BedrockModel
from valyu_agentcore import (
    secSearch,
    financeSearch,
    webSearch,
    patentSearch,
)


SYSTEM_PROMPT = """You are a due diligence analyst preparing a comprehensive report
for a potential investment, acquisition, or partnership evaluation.

Your due diligence report should cover:

1. **Company Overview**
   - Business model and revenue streams
   - Founding history and key milestones
   - Leadership team and board composition

2. **Financial Analysis**
   - Revenue and growth trajectory
   - Profitability and margins
   - Cash position and burn rate (if applicable)
   - Debt and capital structure

3. **Market Position**
   - Market size and share
   - Key competitors
   - Competitive advantages and moats
   - Customer concentration

4. **Risk Assessment**
   - Regulatory risks
   - Legal issues or litigation
   - Key person dependencies
   - Technology risks
   - Market risks

5. **Intellectual Property**
   - Patent portfolio
   - Key technologies
   - Trade secrets or proprietary data

6. **Recent Developments**
   - Recent news and press coverage
   - Strategic moves and partnerships
   - Any red flags or concerns

Structure your report with clear sections and cite all sources.
Flag any information gaps that would need further investigation.
"""


def create_due_diligence_agent():
    """Create a due diligence agent with comprehensive tools."""
    return Agent(
        model=BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            temperature=0.2,
        ),
        system_prompt=SYSTEM_PROMPT,
        tools=[
            secSearch(max_num_results=10),
            financeSearch(max_num_results=10),
            webSearch(max_num_results=10),
            patentSearch(max_num_results=5),
        ],
    )


def run_due_diligence(company: str) -> str:
    """Run due diligence on a company."""
    agent = create_due_diligence_agent()
    query = f"""Conduct comprehensive due diligence on {company}.

    Cover all standard due diligence areas:
    - Company overview and business model
    - Financial health and metrics
    - Market position and competition
    - Risk factors
    - Intellectual property
    - Recent news and developments

    Flag any concerns or areas needing further investigation."""

    response = agent(query)
    return str(response)


EXAMPLE_COMPANIES = [
    "Stripe",
    "OpenAI",
    "Databricks",
    "Snowflake",
    "Palantir",
]


def main():
    if len(sys.argv) < 2:
        print("Due Diligence Agent")
        print("=" * 50)
        print("\nUsage: python due_diligence.py <company_name>")
        print("\nExample companies:")
        for company in EXAMPLE_COMPANIES:
            print(f"    python due_diligence.py \"{company}\"")
        return

    company = " ".join(sys.argv[1:])

    print("=" * 60)
    print("Due Diligence Report")
    print("=" * 60)
    print(f"\nTarget: {company}")
    print("\nConducting due diligence...\n")
    print("-" * 60)

    response = run_due_diligence(company)
    print(response)


if __name__ == "__main__":
    main()
