"""
Valyu tools for AWS Bedrock AgentCore agents.

Provides Strands-compatible tools that work with any AgentCore framework.
Mirrors the @valyu/ai-sdk package for TypeScript/Vercel AI SDK.

Available tools:
- webSearch: General web search with source filtering
- financeSearch: Stock prices, earnings, balance sheets, SEC filings, crypto, forex
- paperSearch: Academic papers (arXiv, PubMed, bioRxiv, medRxiv)
- bioSearch: Biomedical literature, clinical trials, FDA drug labels
- patentSearch: USPTO patents and intellectual property
- secSearch: SEC filings (10-K, 10-Q, 8-K, proxy statements)
- economicsSearch: BLS, FRED, World Bank economic data
"""

import os
from typing import Any, Callable, Literal, Optional
from dataclasses import dataclass

import httpx


# =============================================================================
# Type Definitions (mirrors types.ts)
# =============================================================================

SearchType = Literal["all", "web", "proprietary", "news"]
DataType = Literal["unstructured", "structured"]
SourceType = Literal[
    "general", "website", "forum", "paper", "data", "report",
    "health_data", "clinical_trial", "drug_label", "grants"
]
ResponseLength = Literal["short", "medium", "large", "max"]


@dataclass
class ValyuBaseConfig:
    """Base configuration options for all Valyu search tools."""
    api_key: Optional[str] = None
    search_type: SearchType = "proprietary"
    max_num_results: int = 5
    max_price: Optional[float] = None
    relevance_threshold: Optional[float] = None
    category: Optional[str] = None


@dataclass
class ValyuWebSearchConfig(ValyuBaseConfig):
    """Configuration for web search tool."""
    search_type: SearchType = "all"
    included_sources: Optional[list[str]] = None
    excluded_sources: Optional[list[str]] = None


@dataclass
class ValyuFinanceSearchConfig(ValyuBaseConfig):
    """Configuration for finance search tool."""
    included_sources: Optional[list[str]] = None


@dataclass
class ValyuPaperSearchConfig(ValyuBaseConfig):
    """Configuration for paper search tool."""
    included_sources: Optional[list[str]] = None


@dataclass
class ValyuBioSearchConfig(ValyuBaseConfig):
    """Configuration for biomedical search tool."""
    included_sources: Optional[list[str]] = None


@dataclass
class ValyuPatentSearchConfig(ValyuBaseConfig):
    """Configuration for patent search tool."""
    included_sources: Optional[list[str]] = None


@dataclass
class ValyuSecSearchConfig(ValyuBaseConfig):
    """Configuration for SEC filings search tool."""
    included_sources: Optional[list[str]] = None


@dataclass
class ValyuEconomicsSearchConfig(ValyuBaseConfig):
    """Configuration for economics search tool."""
    included_sources: Optional[list[str]] = None


# =============================================================================
# Low-level HTTP Client
# =============================================================================

class ValyuClient:
    """Low-level HTTP client for Valyu API."""

    BASE_URL = "https://api.valyu.ai/v1"

    def __init__(
        self,
        api_key: str,
        timeout: float = 120.0,
    ):
        self.api_key = api_key
        self._client = httpx.Client(
            base_url=self.BASE_URL,
            headers={
                "x-api-key": api_key,
                "Content-Type": "application/json",
            },
            timeout=timeout
        )

    def deepsearch(self, **kwargs) -> dict:
        """Execute a DeepSearch query."""
        response = self._client.post("/deepsearch", json=kwargs)
        response.raise_for_status()
        return response.json()

    def answer(self, **kwargs) -> dict:
        """Execute an Answer API query."""
        response = self._client.post("/answer", json=kwargs)
        response.raise_for_status()
        return response.json()

    def close(self):
        self._client.close()


# =============================================================================
# Tool Creation Helper
# =============================================================================

def _create_tool(func: Callable, name: str, description: str):
    """Create a Strands-compatible tool with proper metadata."""
    try:
        from strands.tools import tool
        return tool(name=name, description=description)(func)
    except ImportError:
        # Fallback: attach metadata for other frameworks
        func._tool_name = name
        func._tool_description = description
        return func


def _get_api_key(api_key: Optional[str]) -> str:
    """Get API key from parameter or environment."""
    key = api_key or os.environ.get("VALYU_API_KEY")
    if not key:
        raise ValueError(
            "VALYU_API_KEY is required. Set it in environment variables or pass it in config."
        )
    return key


# =============================================================================
# Web Search Tool
# =============================================================================

def webSearch(
    api_key: Optional[str] = None,
    search_type: SearchType = "all",
    max_num_results: int = 5,
    max_price: Optional[float] = None,
    relevance_threshold: Optional[float] = None,
    included_sources: Optional[list[str]] = None,
    excluded_sources: Optional[list[str]] = None,
    category: Optional[str] = None,
):
    """
    Create a web search tool powered by Valyu.

    Search the web for current information, news, and articles.
    The API handles natural language - use simple, clear queries.

    Args:
        api_key: Valyu API key (defaults to VALYU_API_KEY env var)
        search_type: "all", "web", "proprietary", or "news" (default: "all")
        max_num_results: Maximum results to return (default: 5)
        max_price: Maximum cost per query in CPM
        relevance_threshold: Filter results by quality (0-1)
        included_sources: Restrict search to specific domains/sources
        excluded_sources: Exclude specific domains/sources from results
        category: Natural language category to guide search context

    Returns:
        Strands-compatible tool function

    Example:
        from valyu_agentcore import webSearch
        from strands import Agent

        agent = Agent(
            model=model,
            tools=[webSearch(max_num_results=5)]
        )
        agent("What happened in AI this week?")
    """
    key = _get_api_key(api_key)
    client = ValyuClient(api_key=key)

    config_included = included_sources
    config_excluded = excluded_sources

    def _search(
        query: str,
        included_sources: Optional[list[str]] = None,
        excluded_sources: Optional[list[str]] = None,
    ) -> dict:
        """
        Search the web for current information.

        Args:
            query: Natural language query (e.g., 'latest AI developments', 'Tesla Q4 2024 earnings')
            included_sources: Restrict search to specific domains (e.g., ['nature.com', 'arxiv.org'])
            excluded_sources: Exclude specific domains from results (e.g., ['reddit.com', 'quora.com'])

        Returns:
            Full API response with results, metadata, and cost information
        """
        payload: dict[str, Any] = {
            "query": query,
            "search_type": search_type,
            "max_num_results": max_num_results,
        }

        if max_price is not None:
            payload["max_price"] = max_price
        if relevance_threshold is not None:
            payload["relevance_threshold"] = relevance_threshold
        if category:
            payload["category"] = category

        # Priority: function params > config options
        if included_sources:
            payload["included_sources"] = included_sources
        elif config_included:
            payload["included_sources"] = config_included

        if excluded_sources:
            payload["excluded_sources"] = excluded_sources
        elif config_excluded:
            payload["excluded_sources"] = config_excluded

        return client.deepsearch(**payload)

    return _create_tool(
        _search,
        name="web_search",
        description="Search the web for current information, news, and articles. The API handles natural language - use simple, clear queries."
    )


# =============================================================================
# Finance Search Tool
# =============================================================================

def financeSearch(
    api_key: Optional[str] = None,
    search_type: SearchType = "proprietary",
    max_num_results: int = 5,
    max_price: Optional[float] = None,
    relevance_threshold: Optional[float] = None,
    included_sources: Optional[list[str]] = None,
    category: Optional[str] = None,
):
    """
    Create a finance search tool powered by Valyu.

    Search financial data: stock prices, earnings, balance sheets, income statements,
    cash flows, SEC filings, dividends, insider transactions, crypto, forex, and
    economic indicators.

    Args:
        api_key: Valyu API key (defaults to VALYU_API_KEY env var)
        search_type: Search type (default: "proprietary")
        max_num_results: Maximum results to return (default: 5)
        max_price: Maximum cost per query in CPM
        relevance_threshold: Filter results by quality (0-1)
        included_sources: Override default financial sources
        category: Category to focus on (e.g., "stocks", "earnings")

    Returns:
        Strands-compatible tool function

    Example:
        from valyu_agentcore import financeSearch

        tool = financeSearch(max_num_results=5)
        result = tool("Apple stock price Q1-Q3 2020")
    """
    key = _get_api_key(api_key)
    client = ValyuClient(api_key=key)

    default_sources = [
        "valyu/valyu-stocks",
        "valyu/valyu-sec-filings",
        "valyu/valyu-earnings-US",
        "valyu/valyu-balance-sheet-US",
        "valyu/valyu-income-statement-US",
        "valyu/valyu-cash-flow-US",
        "valyu/valyu-dividends-US",
        "valyu/valyu-insider-transactions-US",
        "valyu/valyu-market-movers-US",
        "valyu/valyu-crypto",
        "valyu/valyu-forex",
        "valyu/valyu-bls",
        "valyu/valyu-fred",
        "valyu/valyu-world-bank",
    ]

    sources = included_sources or default_sources

    def _search(query: str) -> dict:
        """
        Search financial data and market information.

        Args:
            query: Natural language query (e.g., 'Apple stock price Q1-Q3 2020', 'Tesla revenue last 4 quarters')

        Returns:
            Full API response with financial data results
        """
        payload: dict[str, Any] = {
            "query": query,
            "search_type": search_type,
            "max_num_results": max_num_results,
            "included_sources": sources,
        }

        if max_price is not None:
            payload["max_price"] = max_price
        if relevance_threshold is not None:
            payload["relevance_threshold"] = relevance_threshold
        if category:
            payload["category"] = category

        return client.deepsearch(**payload)

    return _create_tool(
        _search,
        name="finance_search",
        description="Search financial data: stock prices, earnings, balance sheets, income statements, cash flows, SEC filings, dividends, insider transactions, crypto, forex, and economic indicators. The API handles natural language - ask your full question in one query per topic."
    )


# =============================================================================
# Paper Search Tool
# =============================================================================

def paperSearch(
    api_key: Optional[str] = None,
    search_type: SearchType = "proprietary",
    max_num_results: int = 5,
    max_price: Optional[float] = None,
    relevance_threshold: Optional[float] = None,
    included_sources: Optional[list[str]] = None,
    category: Optional[str] = None,
):
    """
    Create an academic paper search tool powered by Valyu.

    Search academic papers from arXiv, PubMed, bioRxiv, and medRxiv.
    The API handles semantic search - use simple natural language.

    Args:
        api_key: Valyu API key (defaults to VALYU_API_KEY env var)
        search_type: Search type (default: "proprietary")
        max_num_results: Maximum results to return (default: 5)
        max_price: Maximum cost per query in CPM
        relevance_threshold: Filter results by quality (0-1)
        included_sources: Override default academic sources
        category: Category to focus on (e.g., "computer-science", "physics")

    Returns:
        Strands-compatible tool function

    Example:
        from valyu_agentcore import paperSearch

        tool = paperSearch(max_num_results=10)
        result = tool("transformer architectures for language models")
    """
    key = _get_api_key(api_key)
    client = ValyuClient(api_key=key)

    default_sources = [
        "valyu/valyu-arxiv",
        "valyu/valyu-biorxiv",
        "valyu/valyu-medrxiv",
        "valyu/valyu-pubmed",
    ]

    sources = included_sources or default_sources

    def _search(query: str) -> dict:
        """
        Search academic research papers and scholarly articles.

        Args:
            query: Natural language query (e.g., 'psilocybin effects on lifespan in mice', 'CRISPR cancer therapy trials')

        Returns:
            Full API response with academic papers, authors, citations
        """
        payload: dict[str, Any] = {
            "query": query,
            "search_type": search_type,
            "max_num_results": max_num_results,
            "included_sources": sources,
        }

        if max_price is not None:
            payload["max_price"] = max_price
        if relevance_threshold is not None:
            payload["relevance_threshold"] = relevance_threshold
        if category:
            payload["category"] = category

        return client.deepsearch(**payload)

    return _create_tool(
        _search,
        name="paper_search",
        description="Search academic papers from arXiv, PubMed, bioRxiv, and medRxiv. The API handles semantic search - use simple natural language, not keyword stuffing."
    )


# =============================================================================
# Bio Search Tool
# =============================================================================

def bioSearch(
    api_key: Optional[str] = None,
    search_type: SearchType = "proprietary",
    max_num_results: int = 5,
    max_price: Optional[float] = None,
    relevance_threshold: Optional[float] = None,
    included_sources: Optional[list[str]] = None,
    category: Optional[str] = None,
):
    """
    Create a biomedical search tool powered by Valyu.

    Search biomedical literature from PubMed, clinical trials, and FDA drug labels.
    The API handles natural language - use simple queries.

    Args:
        api_key: Valyu API key (defaults to VALYU_API_KEY env var)
        search_type: Search type (default: "proprietary")
        max_num_results: Maximum results to return (default: 5)
        max_price: Maximum cost per query in CPM
        relevance_threshold: Filter results by quality (0-1)
        included_sources: Override default biomedical sources
        category: Category to focus on (e.g., "clinical-trials", "drug-labels")

    Returns:
        Strands-compatible tool function

    Example:
        from valyu_agentcore import bioSearch

        tool = bioSearch(max_num_results=5)
        result = tool("GLP-1 agonists for weight loss")
    """
    key = _get_api_key(api_key)
    client = ValyuClient(api_key=key)

    default_sources = [
        "valyu/valyu-pubmed",
        "valyu/valyu-biorxiv",
        "valyu/valyu-medrxiv",
        "valyu/valyu-clinical-trials",
        "valyu/valyu-drug-labels",
    ]

    sources = included_sources or default_sources

    def _search(query: str) -> dict:
        """
        Search biomedical literature and clinical data.

        Args:
            query: Natural language query (e.g., 'GLP-1 agonists for weight loss', 'Phase 3 melanoma immunotherapy trials')

        Returns:
            Full API response with biomedical research, clinical trials, drug information
        """
        payload: dict[str, Any] = {
            "query": query,
            "search_type": search_type,
            "max_num_results": max_num_results,
            "included_sources": sources,
        }

        if max_price is not None:
            payload["max_price"] = max_price
        if relevance_threshold is not None:
            payload["relevance_threshold"] = relevance_threshold
        if category:
            payload["category"] = category

        return client.deepsearch(**payload)

    return _create_tool(
        _search,
        name="bio_search",
        description="Search biomedical literature from PubMed, clinical trials, and FDA drug labels. The API handles natural language - use simple queries."
    )


# =============================================================================
# Patent Search Tool
# =============================================================================

def patentSearch(
    api_key: Optional[str] = None,
    search_type: SearchType = "proprietary",
    max_num_results: int = 5,
    max_price: Optional[float] = None,
    relevance_threshold: Optional[float] = None,
    included_sources: Optional[list[str]] = None,
    category: Optional[str] = None,
):
    """
    Create a patent search tool powered by Valyu.

    Search patent databases for inventions and intellectual property.
    The API handles natural language - no need for patent numbers or classification codes.

    Args:
        api_key: Valyu API key (defaults to VALYU_API_KEY env var)
        search_type: Search type (default: "proprietary")
        max_num_results: Maximum results to return (default: 5)
        max_price: Maximum cost per query in CPM
        relevance_threshold: Filter results by quality (0-1)
        included_sources: Override default patent sources
        category: Category to focus on (e.g., "technology", "pharmaceutical")

    Returns:
        Strands-compatible tool function

    Example:
        from valyu_agentcore import patentSearch

        tool = patentSearch(max_num_results=5)
        result = tool("solid-state battery patents")
    """
    key = _get_api_key(api_key)
    client = ValyuClient(api_key=key)

    default_sources = ["valyu/valyu-patents"]
    sources = included_sources or default_sources

    def _search(query: str) -> dict:
        """
        Search patents and intellectual property.

        Args:
            query: Natural language query (e.g., 'solid-state battery patents', 'CRISPR gene editing methods')

        Returns:
            Full API response with patent results, abstracts, and patent numbers
        """
        payload: dict[str, Any] = {
            "query": query,
            "search_type": search_type,
            "max_num_results": max_num_results,
            "included_sources": sources,
        }

        if max_price is not None:
            payload["max_price"] = max_price
        if relevance_threshold is not None:
            payload["relevance_threshold"] = relevance_threshold
        if category:
            payload["category"] = category

        return client.deepsearch(**payload)

    return _create_tool(
        _search,
        name="patent_search",
        description="Search patent databases for inventions and intellectual property. The API handles natural language - no need for patent numbers or classification codes."
    )


# =============================================================================
# SEC Search Tool
# =============================================================================

def secSearch(
    api_key: Optional[str] = None,
    search_type: SearchType = "proprietary",
    max_num_results: int = 5,
    max_price: Optional[float] = None,
    relevance_threshold: Optional[float] = None,
    included_sources: Optional[list[str]] = None,
    category: Optional[str] = None,
):
    """
    Create an SEC filings search tool powered by Valyu.

    Search SEC filings (10-K, 10-Q, 8-K, proxy statements).
    Use simple natural language with company name and filing type.

    Args:
        api_key: Valyu API key (defaults to VALYU_API_KEY env var)
        search_type: Search type (default: "proprietary")
        max_num_results: Maximum results to return (default: 5)
        max_price: Maximum cost per query in CPM
        relevance_threshold: Filter results by quality (0-1)
        included_sources: Override default SEC sources
        category: Category to focus on (e.g., "10-K", "10-Q", "8-K")

    Returns:
        Strands-compatible tool function

    Example:
        from valyu_agentcore import secSearch

        tool = secSearch(max_num_results=5)
        result = tool("Tesla 10-K risk factors")
    """
    key = _get_api_key(api_key)
    client = ValyuClient(api_key=key)

    default_sources = ["valyu/valyu-sec-filings"]
    sources = included_sources or default_sources

    def _search(query: str) -> dict:
        """
        Search SEC filings and regulatory documents.

        Args:
            query: Natural language query (e.g., 'Tesla 10-K risk factors', 'Apple executive compensation 2024')

        Returns:
            Full API response with SEC filings excerpts and links
        """
        payload: dict[str, Any] = {
            "query": query,
            "search_type": search_type,
            "max_num_results": max_num_results,
            "included_sources": sources,
        }

        if max_price is not None:
            payload["max_price"] = max_price
        if relevance_threshold is not None:
            payload["relevance_threshold"] = relevance_threshold
        if category:
            payload["category"] = category

        return client.deepsearch(**payload)

    return _create_tool(
        _search,
        name="sec_search",
        description="Search SEC filings (10-K, 10-Q, 8-K, proxy statements). Use simple natural language with company name and filing type - no accession numbers or technical syntax needed."
    )


# =============================================================================
# Economics Search Tool
# =============================================================================

def economicsSearch(
    api_key: Optional[str] = None,
    search_type: SearchType = "proprietary",
    max_num_results: int = 3,
    max_price: Optional[float] = None,
    relevance_threshold: Optional[float] = None,
    included_sources: Optional[list[str]] = None,
    category: Optional[str] = None,
):
    """
    Create an economics and statistics search tool powered by Valyu.

    Search economic data from BLS, FRED, World Bank.
    The API handles natural language - no need for series IDs or technical codes.

    Args:
        api_key: Valyu API key (defaults to VALYU_API_KEY env var)
        search_type: Search type (default: "proprietary")
        max_num_results: Maximum results to return (default: 3)
        max_price: Maximum cost per query in CPM
        relevance_threshold: Filter results by quality (0-1)
        included_sources: Override default economics sources
        category: Category to focus on (e.g., "labor-statistics", "economic-indicators")

    Returns:
        Strands-compatible tool function

    Example:
        from valyu_agentcore import economicsSearch

        tool = economicsSearch(max_num_results=5)
        result = tool("US unemployment rate last 5 years")
    """
    key = _get_api_key(api_key)
    client = ValyuClient(api_key=key)

    default_sources = [
        "valyu/valyu-bls",
        "valyu/valyu-fred",
        "valyu/valyu-world-bank",
        "valyu/valyu-worldbank-indicators",
        "valyu/valyu-usaspending",
    ]

    sources = included_sources or default_sources

    def _search(query: str) -> dict:
        """
        Search economic data and indicators.

        Args:
            query: Natural language query (e.g., 'CPI vs unemployment since 2020', 'US GDP growth last 5 years')

        Returns:
            Full API response with economic data and sources
        """
        payload: dict[str, Any] = {
            "query": query,
            "search_type": search_type,
            "max_num_results": max_num_results,
            "included_sources": sources,
        }

        if max_price is not None:
            payload["max_price"] = max_price
        if relevance_threshold is not None:
            payload["relevance_threshold"] = relevance_threshold
        if category:
            payload["category"] = category

        return client.deepsearch(**payload)

    return _create_tool(
        _search,
        name="economics_search",
        description="Search economic data from BLS, FRED, World Bank. The API handles natural language - no need for series IDs or technical codes."
    )


# =============================================================================
# ValyuTools Class - Convenience Wrapper
# =============================================================================

class ValyuTools:
    """
    Convenience wrapper for all Valyu tools.

    Usage with Strands:
        from valyu_agentcore import ValyuTools
        from strands import Agent

        tools = ValyuTools(api_key="val_xxx")
        agent = Agent(model=model, tools=tools.all())

    Usage with individual tools:
        from valyu_agentcore import webSearch, financeSearch, secSearch

        agent = Agent(
            model=model,
            tools=[webSearch(), financeSearch(), secSearch()]
        )
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        max_num_results: int = 5,
        max_price: Optional[float] = None,
    ):
        self.api_key = _get_api_key(api_key)
        self.max_num_results = max_num_results
        self.max_price = max_price

    @property
    def web_search(self):
        return webSearch(
            api_key=self.api_key,
            max_num_results=self.max_num_results,
            max_price=self.max_price,
        )

    @property
    def finance_search(self):
        return financeSearch(
            api_key=self.api_key,
            max_num_results=self.max_num_results,
            max_price=self.max_price,
        )

    @property
    def paper_search(self):
        return paperSearch(
            api_key=self.api_key,
            max_num_results=self.max_num_results,
            max_price=self.max_price,
        )

    @property
    def bio_search(self):
        return bioSearch(
            api_key=self.api_key,
            max_num_results=self.max_num_results,
            max_price=self.max_price,
        )

    @property
    def patent_search(self):
        return patentSearch(
            api_key=self.api_key,
            max_num_results=self.max_num_results,
            max_price=self.max_price,
        )

    @property
    def sec_search(self):
        return secSearch(
            api_key=self.api_key,
            max_num_results=self.max_num_results,
            max_price=self.max_price,
        )

    @property
    def economics_search(self):
        return economicsSearch(
            api_key=self.api_key,
            max_num_results=self.max_num_results,
            max_price=self.max_price,
        )

    def all(self) -> list:
        """Get all Valyu tools."""
        return [
            self.web_search,
            self.finance_search,
            self.paper_search,
            self.bio_search,
            self.patent_search,
            self.sec_search,
            self.economics_search,
        ]

    def search_tools(self) -> list:
        """Get all search tools."""
        return self.all()

    def financial_tools(self) -> list:
        """Get finance-focused tools."""
        return [
            self.finance_search,
            self.sec_search,
            self.economics_search,
        ]

    def research_tools(self) -> list:
        """Get research-focused tools (academic + patents)."""
        return [
            self.paper_search,
            self.bio_search,
            self.patent_search,
        ]
