# AgentCore Gateway Integration

Add Valyu search tools to your AWS Bedrock AgentCore Gateway.

## Why Use Gateway?

- **Centralized API Keys** - Store Valyu API key in gateway config, not in application code
- **Audit Logging** - Track all tool calls through AWS CloudTrail
- **Unified Access** - Single gateway endpoint for multiple MCP tool providers
- **Enterprise Auth** - Use your existing Cognito/OAuth infrastructure

## Quick Start

### Add to Existing Gateway (Recommended)

If you already have an AgentCore Gateway:

```python
from valyu_agentcore.gateway import add_valyu_target

add_valyu_target(gateway_id="your-gateway-id")
```

Done. Valyu tools are now available to any agent connected to your gateway.

### Create New Gateway

For testing or new deployments:

```python
from valyu_agentcore.gateway import setup_valyu_gateway, GatewayAgent

# One-time setup (creates gateway + Cognito auth)
setup_valyu_gateway()

# Use the agent
with GatewayAgent.from_config() as agent:
    response = agent("Search for NVIDIA SEC filings")
    print(response)
```

## Installation

```bash
pip install valyu-agentcore[agentcore]
```

Set your Valyu API key:
```bash
export VALYU_API_KEY=your-api-key
```

Get your key at [platform.valyu.ai](https://platform.valyu.ai).

## Available Functions

### add_valyu_target

Add Valyu to an existing gateway:

```python
from valyu_agentcore.gateway import add_valyu_target

result = add_valyu_target(
    gateway_id="your-gateway-id",
    valyu_api_key="your-key",  # or uses VALYU_API_KEY env var
    region="us-east-1",
    target_name="valyu-search",
)

print(f"Target ID: {result['target_id']}")
```

### setup_valyu_gateway

Create a new gateway with Cognito authentication:

```python
from valyu_agentcore.gateway import setup_valyu_gateway

config = setup_valyu_gateway(
    valyu_api_key="your-key",  # or uses VALYU_API_KEY env var
    gateway_name="my-gateway",
    region="us-east-1",
)

print(f"Gateway URL: {config.gateway_url}")
# Config saved to valyu_gateway_config.json
```

### GatewayAgent

Use after `setup_valyu_gateway()`:

```python
from valyu_agentcore.gateway import GatewayAgent

with GatewayAgent.from_config() as agent:
    # List available tools
    tools = agent.list_tools()
    print(f"Available: {len(tools)} tools")

    # Run a query
    response = agent("Research Tesla's financial performance")
    print(response)
```

### cleanup_valyu_gateway

Remove gateway resources:

```python
from valyu_agentcore.gateway import cleanup_valyu_gateway

cleanup_valyu_gateway()  # Uses valyu_gateway_config.json
```

## Available Tools

Once Valyu is added to your gateway, these tools become available:

| Tool | Description |
|------|-------------|
| `valyu_search` | Web search returning full page content |
| `valyu_academic_search` | Academic papers from arXiv, PubMed, journals |
| `valyu_financial_search` | Stock prices, earnings, market data |
| `valyu_sec_search` | SEC filings (10-K, 10-Q, 8-K) with section search |
| `valyu_patents` | Patent search and analysis |
| `valyu_contents` | Extract content from any URL |

Tools appear with a prefix based on your target name:
```
valyu-search___valyu_search
valyu-search___valyu_sec_search
valyu-search___valyu_financial_search
```

## Manual Setup via AWS Console

If you prefer the AWS Console:

1. Go to **Amazon Bedrock → AgentCore → Gateways**
2. Select your gateway (or create one)
3. Click **Add target**
4. Configure:
   - **Name**: `valyu-search`
   - **Type**: MCP server
   - **Endpoint**: `https://mcp.valyu.ai/mcp?valyuApiKey=YOUR_VALYU_API_KEY`
5. Wait for status to show "Ready"

## Using with Your Own Agent

After adding Valyu to your gateway, use the tools from your existing agent code:

```python
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client

# Connect to your gateway
def create_transport():
    return streamablehttp_client(
        "https://your-gateway.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp",
        headers={"Authorization": f"Bearer {your_access_token}"}
    )

with MCPClient(create_transport) as mcp:
    tools = mcp.list_tools_sync()

    agent = Agent(
        model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
        tools=tools,
    )

    response = agent("Find NVIDIA's latest 10-K and summarize risk factors")
    print(response)
```

## Example Scripts

| Script | Description |
|--------|-------------|
| `add_valyu_target.py` | CLI to add Valyu to existing gateway |
| `setup_gateway.py` | Create new gateway with Cognito auth |
| `use_gateway.py` | Demo using GatewayAgent |

### add_valyu_target.py

```bash
# Add to existing gateway
python add_valyu_target.py --gateway-id your-gateway-id

# List targets
python add_valyu_target.py --gateway-id your-gateway-id --list

# Remove target
python add_valyu_target.py --gateway-id your-gateway-id --remove TARGET_ID
```

### setup_gateway.py

```bash
# Create new gateway
python setup_gateway.py

# Cleanup
python setup_gateway.py cleanup
```

### use_gateway.py

```bash
# Run demo
python use_gateway.py

# Interactive mode
python use_gateway.py -i
```

## Troubleshooting

### "Target synchronization failed"

- Verify your Valyu API key is valid at [platform.valyu.ai](https://platform.valyu.ai)
- Check network connectivity from AWS to `mcp.valyu.ai`

### "Access denied" errors

- Ensure your IAM role has `bedrock-agentcore:*` permissions
- Check that your OAuth token is valid and not expired

### "Cognito credentials not found"

- Run `setup_valyu_gateway()` first to create the gateway
- Check that `valyu_gateway_config.json` exists

### Tools not appearing

- Wait 1-2 minutes for target sync
- Check target status in AWS Console or via `--list` flag

## Links

- [Get Valyu API Key](https://platform.valyu.ai)
- [Valyu Documentation](https://docs.valyu.ai)
- [AgentCore Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html)
