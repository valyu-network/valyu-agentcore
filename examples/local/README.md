# Local Examples

Simple examples using Valyu tools directly with Strands Agents (no Gateway/Runtime).

## Setup

```bash
pip install valyu-agentcore[strands]
export VALYU_API_KEY=your-api-key
```

Get your API key at [platform.valyu.ai](https://platform.valyu.ai).

## Run Examples

```bash
# Web search
python web_search.py

# Financial data
python finance_search.py

# SEC filings
python sec_search.py

# Academic papers
python paper_search.py

# Patents
python patent_search.py

# Biomedical
python bio_search.py

# Economic data
python economics_search.py
```

## Available Tools

| Example | Tool | What it does |
|---------|------|--------------|
| `web_search.py` | `webSearch` | Search the web, get full page content |
| `finance_search.py` | `financeSearch` | Stock prices, earnings, market data |
| `sec_search.py` | `secSearch` | SEC filings (10-K, 10-Q, 8-K) |
| `paper_search.py` | `paperSearch` | Academic papers from arXiv, PubMed |
| `patent_search.py` | `patentSearch` | USPTO patents |
| `bio_search.py` | `bioSearch` | Clinical trials, FDA data |
| `economics_search.py` | `economicsSearch` | BLS, FRED, World Bank data |

## Use in Your Code

```python
from valyu_agentcore import webSearch, financeSearch
from strands import Agent
from strands.models import BedrockModel

agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    tools=[webSearch(), financeSearch()],
)

response = agent("What's the latest news about Tesla and its stock price?")
print(response)
```
