"""
Valyu AgentCore - Search tools for AWS Bedrock AgentCore

Drop-in search tools for AI agents. Works with Strands Agents, AWS Bedrock
AgentCore Gateway, and any MCP-compatible framework.

## Quick Start (Direct)

```python
from valyu_agentcore import webSearch, financeSearch, secSearch
from strands import Agent
from strands.models import BedrockModel

agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    tools=[webSearch(), financeSearch(), secSearch()]
)

response = agent("What are Tesla's latest SEC filings?")
```

## Via AgentCore Gateway (Enterprise)

```python
from valyu_agentcore.gateway import setup_valyu_gateway, GatewayAgent

# One-time setup
setup_valyu_gateway()

# Use the agent
with GatewayAgent.from_config() as agent:
    response = agent("Research NVIDIA financials")
```

## Available Tools

- webSearch: General web search
- financeSearch: Stock prices, earnings, market data
- paperSearch: Academic papers (arXiv, PubMed)
- bioSearch: Clinical trials, FDA drug labels
- patentSearch: USPTO patents
- secSearch: SEC filings (10-K, 10-Q, 8-K)
- economicsSearch: BLS, FRED, World Bank data

Get your API key at https://platform.valyu.ai
"""

from .tools import (
    # Main classes
    ValyuTools,
    ValyuClient,
    # Individual tool factories (camelCase to match @valyu/ai-sdk)
    webSearch,
    financeSearch,
    paperSearch,
    bioSearch,
    patentSearch,
    secSearch,
    economicsSearch,
    # Type definitions
    SearchType,
    DataType,
    SourceType,
    ResponseLength,
    ValyuBaseConfig,
    ValyuWebSearchConfig,
    ValyuFinanceSearchConfig,
    ValyuPaperSearchConfig,
    ValyuBioSearchConfig,
    ValyuPatentSearchConfig,
    ValyuSecSearchConfig,
    ValyuEconomicsSearchConfig
)
from .version import __version__

__all__ = [
    # Main classes
    "ValyuTools",
    "ValyuClient",
    # Individual tools (camelCase to match @valyu/ai-sdk)
    "webSearch",
    "financeSearch",
    "paperSearch",
    "bioSearch",
    "patentSearch",
    "secSearch",
    "economicsSearch",
    # Type definitions
    "SearchType",
    "DataType",
    "SourceType",
    "ResponseLength",
    "ValyuBaseConfig",
    "ValyuWebSearchConfig",
    "ValyuFinanceSearchConfig",
    "ValyuPaperSearchConfig",
    "ValyuBioSearchConfig",
    "ValyuPatentSearchConfig",
    "ValyuSecSearchConfig",
    "ValyuEconomicsSearchConfig",
    # Version
    "__version__",
]

# Gateway imports available via: from valyu_agentcore.gateway import GatewayAgent
