# valyu-agentcore

Add web and domain-specific search capabilities to [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html) and [Strands Agents](https://strandsagents.com).

Includes web search, SEC filings, financial data, academic papers, patents, biomedical data, and company research.

Valyu is the [leading search API for AI agents](https://www.valyu.ai/blogs/benchmarking-search-apis-for-ai-agents).

## Installation

```bash
pip install valyu-agentcore
```

For AgentCore Gateway support:
```bash
pip install valyu-agentcore[agentcore]
```

## Quick Start

### Add to AgentCore Gateway (Enterprise)

Add Valyu search tools to your existing gateway with one line:

```python
from valyu_agentcore.gateway import add_valyu_target

add_valyu_target(gateway_id="your-gateway-id")
```

That's it. All Valyu tools are now available to any agent connected to your gateway.

**Why use AgentCore Gateway?**
- **Centralized secrets** - API keys stored in AWS, not in application code
- **Audit logging** - All tool calls logged to CloudTrail
- **Unified access** - Single MCP gateway for multiple tool providers
- **Enterprise auth** - OAuth via Cognito or your existing identity provider

### Direct with Strands Agents

For development or simpler deployments, use tools directly:

```python
from valyu_agentcore import webSearch, financeSearch, secSearch
from strands import Agent
from strands.models import BedrockModel

agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    tools=[webSearch(), financeSearch(), secSearch()],
)

response = agent("Summarize Tesla's latest 10-K risk factors")
```

Get your API key at [platform.valyu.ai](https://platform.valyu.ai). For enterprise requirements, [contact us](https://valyu.ai/enterprise).

See [examples/gateway/](examples/gateway/) for full gateway documentation.

## Available Tools

| Tool | Description | Best For |
|------|-------------|----------|
| `webSearch` | Web search with full page content | News, current events, general info |
| `financeSearch` | Stock prices, earnings, market data | Financial analysis, market research |
| `paperSearch` | Academic papers (arXiv, PubMed, journals) | Literature review, research |
| `bioSearch` | Clinical trials, FDA labels, biomedical | Medical research, drug info |
| `patentSearch` | USPTO patents and IP | Prior art, IP research |
| `secSearch` | SEC filings (10-K, 10-Q, 8-K) | Company analysis, due diligence |
| `economicsSearch` | BLS, FRED, World Bank data | Economic indicators, policy research |

## Use Case Examples

Real-world agent examples in [examples/use_cases/](examples/use_cases/):

| Example | Description | Tools Used |
|---------|-------------|------------|
| [Financial Analyst](examples/use_cases/financial_analyst.py) | Investment research and analysis | SEC, finance, company, web |
| [Research Assistant](examples/use_cases/research_assistant.py) | Academic literature review | papers, patents, web |
| [Due Diligence](examples/use_cases/due_diligence.py) | M&A and investment evaluation | All tools |

```bash
# Run financial analyst
python examples/use_cases/financial_analyst.py "Analyze NVIDIA's competitive position"

# Run research assistant
python examples/use_cases/research_assistant.py "transformer architecture improvements"

# Run due diligence
python examples/use_cases/due_diligence.py "Stripe"
```

## Tool Examples

### webSearch

```python
from valyu_agentcore import webSearch

agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    tools=[webSearch()],
)
response = agent("Latest news on quantum computing breakthroughs")
```

### financeSearch

```python
from valyu_agentcore import financeSearch

agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    tools=[financeSearch()],
)
response = agent("What is NVIDIA's current stock price and P/E ratio?")
```

### secSearch

```python
from valyu_agentcore import secSearch

agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    tools=[secSearch()],
)
response = agent("Summarize the risk factors from Apple's latest 10-K")
```


## Use All Tools

```python
from valyu_agentcore import ValyuTools

tools = ValyuTools(max_num_results=5)

agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    tools=tools.all(),  # All 8 tools
)

# Or use tool groups:
# tools.search_tools()     - All search tools
# tools.financial_tools()  - finance, SEC, economics, company research
# tools.research_tools()   - papers, bio, patents
```

## Configuration

All tools accept these options:

```python
from valyu_agentcore import webSearch

tool = webSearch(
    api_key="your-key",           # Or use VALYU_API_KEY env var
    max_num_results=10,           # Number of results (default: 5)
    max_price=0.50,               # Max cost per query in dollars
    relevance_threshold=0.7,      # Filter by quality (0-1)
    excluded_sources=["reddit.com"],  # Exclude specific domains
)
```

## AgentCore Gateway

### Add to Existing Gateway

If you already have an AgentCore Gateway:

```python
from valyu_agentcore.gateway import add_valyu_target

# Add Valyu tools to your gateway
result = add_valyu_target(
    gateway_id="your-gateway-id",
    region="us-east-1",  # optional
)
print(f"Added target: {result['target_id']}")
```

Your existing agents will now have access to all Valyu tools through the gateway.

### Create New Gateway

For testing or new deployments:

```python
from valyu_agentcore.gateway import setup_valyu_gateway, GatewayAgent

# Create gateway with Cognito auth (one-time)
config = setup_valyu_gateway()

# Use the agent
with GatewayAgent.from_config() as agent:
    response = agent("Search for NVIDIA SEC filings")
    print(response)
```

### CloudFormation Deployment

Deploy authentication infrastructure via CloudFormation:

```bash
aws cloudformation create-stack \
  --stack-name valyu-gateway \
  --template-body file://cloudformation/valyu-gateway.yaml \
  --parameters ParameterKey=ValyuApiKey,ParameterValue=YOUR_KEY \
  --capabilities CAPABILITY_NAMED_IAM
```

This creates Cognito, IAM, and logging infrastructure. Then create your gateway and add Valyu as a target. See [cloudformation/](cloudformation/) for full instructions.

### IAM Policies

Ready-to-use IAM policies in [iam-policies/](iam-policies/):

- **agentcore-user-policy.json** - Full gateway management access
- **agentcore-invoke-only-policy.json** - Minimal invoke-only access

### Manual Console Setup

You can also add Valyu via AWS Console:

1. Go to **Amazon Bedrock** > **AgentCore** > **Gateways**
2. Select your gateway > **Add target**
3. Configure:
   - Name: `valyu-search`
   - Type: MCP server
   - Endpoint: `https://mcp.valyu.ai/mcp?valyuApiKey=YOUR_KEY`

### Gateway Tools

Tools available through the gateway:

| Gateway Tool | Description |
|--------------|-------------|
| `valyu_search` | Web search |
| `valyu_academic_search` | Academic papers |
| `valyu_financial_search` | Financial data |
| `valyu_sec_search` | SEC filings |
| `valyu_patents` | Patent search |
| `valyu_contents` | URL content extraction |

See [examples/gateway/README.md](examples/gateway/README.md) for complete documentation.

## Project Structure

```
valyu-agentcore/
├── valyu_agentcore/         # Core package
│   ├── tools.py             # Strands Agent tools
│   └── gateway.py           # AgentCore Gateway integration
├── examples/
│   ├── notebooks/           # Jupyter notebooks
│   │   └── getting_started.ipynb
│   ├── web_search.py        # Basic tool examples
│   ├── finance_search.py
│   ├── sec_search.py
│   ├── paper_search.py
│   ├── use_cases/           # Real-world agent examples
│   │   ├── financial_analyst.py
│   │   ├── research_assistant.py
│   │   └── due_diligence.py
│   └── gateway/             # Gateway examples
│       ├── add_valyu_target.py
│       ├── setup_gateway.py
│       └── use_gateway.py
├── cloudformation/          # AWS CloudFormation templates
│   └── valyu-gateway.yaml
└── iam-policies/            # IAM policy templates
    ├── agentcore-user-policy.json
    └── agentcore-invoke-only-policy.json
```

## Create Custom Tools

Build your own tool using the Valyu API:

```python
import os
import httpx
from strands.tools import tool

@tool
def my_custom_search(query: str) -> dict:
    """Search for specific content."""
    response = httpx.post(
        "https://api.valyu.ai/v1/deepsearch",
        headers={"x-api-key": os.environ["VALYU_API_KEY"]},
        json={
            "query": query,
            "search_type": "all",
            "included_sources": ["your-sources"],
        },
    )
    return response.json()
```

## Links

- [Valyu Platform](https://platform.valyu.ai) - Get API keys ($10 free credits)
- [Valyu Documentation](https://docs.valyu.ai) - API docs
- [Strands Agents](https://strandsagents.com) - Agent framework
- [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html) - AWS docs

## License

MIT
