# Use Case Examples

Real-world agent examples demonstrating Valyu tools for enterprise workflows.

## Financial Analyst

Investment research agent combining SEC filings, market data, and web search.

```bash
python financial_analyst.py "Analyze NVIDIA's competitive position"
```

**Tools used:** `financeSearch`, `secSearch`, `webSearch`

**Best for:**
- Equity research
- Investment memos
- Earnings analysis
- Sector comparisons

## Research Assistant

Academic and technical research agent for literature review and prior art search.

```bash
python research_assistant.py "transformer architecture improvements"
```

**Tools used:** `paperSearch`, `patentSearch`, `webSearch`

**Best for:**
- Literature reviews
- Prior art search
- Technical research
- State of the art surveys

## Due Diligence

Comprehensive due diligence agent for M&A, investment, or partnership evaluation.

```bash
python due_diligence.py "Stripe"
```

**Tools used:** `secSearch`, `financeSearch`, `webSearch`, `patentSearch`

**Best for:**
- M&A due diligence
- Investment evaluation
- Partnership assessment
- Competitive intelligence

## Running Examples

1. Set your API key:
   ```bash
   export VALYU_API_KEY=your-api-key
   ```

2. Install dependencies:
   ```bash
   pip install valyu-agentcore[strands]
   ```

3. Run any example:
   ```bash
   python financial_analyst.py "your query"
   ```

## Customizing for Your Use Case

These examples show patterns you can adapt:

1. **Tool Selection** - Choose tools relevant to your domain
2. **System Prompts** - Define the agent's persona and output format
3. **Temperature** - Lower for factual, higher for creative tasks
4. **Result Limits** - Adjust `max_num_results` based on depth needed

Example customization:

```python
from strands import Agent
from strands.models import BedrockModel
from valyu_agentcore import secSearch, financeSearch

agent = Agent(
    model=BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        temperature=0.2,  # Factual analysis
    ),
    system_prompt="You are a compliance analyst...",
    tools=[
        secSearch(max_num_results=20),  # More SEC results
        financeSearch(max_num_results=10),
    ],
)
```

## Gateway Deployment

These agents can also run through AgentCore Gateway. After deploying Valyu to your gateway, the same queries work with centralized auth and audit logging.

See [../gateway/](../gateway/) for gateway setup.
