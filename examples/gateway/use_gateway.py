"""
Use Valyu Tools via AgentCore Gateway

Test Valyu search tools through your AgentCore Gateway.

Works with either setup method:
  1. After setup_gateway.py (uses saved config)
  2. After add_valyu_target.py (provide gateway URL and token)

Usage:
    # If you ran setup_gateway.py (config file exists)
    python use_gateway.py

    # If you ran add_valyu_target.py (provide your gateway details)
    python use_gateway.py --gateway-url https://your-gateway.../mcp --token YOUR_TOKEN

    # Interactive mode
    python use_gateway.py -i
"""

import argparse
import os


def get_agent_from_config():
    """Create agent from saved config (setup_gateway.py flow)."""
    from valyu_agentcore.gateway import GatewayAgent
    return GatewayAgent.from_config()


def get_agent_from_args(gateway_url: str, token: str):
    """Create agent from provided URL and token (add_valyu_target flow)."""
    from valyu_agentcore.gateway import GatewayAgent
    return GatewayAgent(
        gateway_url=gateway_url,
        access_token=token,
    )


def run_demo(agent):
    """Run demo queries."""
    # List available tools
    tools = agent.list_tools()
    print(f"\nAvailable tools ({len(tools)}):")
    for tool in tools:
        tool_name = getattr(tool, 'name', None) or getattr(tool, 'tool_name', str(tool))
        print(f"  - {tool_name}")

    print("\n" + "-" * 60)

    # Run a query
    query = "Search for recent news about AI chip development"
    print(f"\nQuery: {query}")
    print("-" * 40)

    response = agent(query)
    print(response)


def run_interactive(agent):
    """Interactive mode."""
    print("\nType 'exit' to quit.\n")

    while True:
        try:
            query = input("Query: ").strip()
            if query.lower() in ["exit", "quit"]:
                break
            if not query:
                continue

            print("\nSearching...\n")
            response = agent(query)
            print(response)
            print()

        except KeyboardInterrupt:
            break

    print("\nGoodbye!")


def main():
    parser = argparse.ArgumentParser(
        description="Test Valyu tools via AgentCore Gateway"
    )
    parser.add_argument(
        "--gateway-url",
        help="Gateway MCP endpoint URL (required if no config file)",
    )
    parser.add_argument(
        "--token",
        help="OAuth access token (required if no config file)",
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Interactive mode",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Valyu + AgentCore Gateway Agent")
    print("=" * 60)

    # Determine which flow to use
    config_exists = os.path.exists("valyu_gateway_config.json")

    if args.gateway_url and args.token:
        # User provided gateway details (add_valyu_target flow)
        print("\nUsing provided gateway URL and token...")
        agent_ctx = get_agent_from_args(args.gateway_url, args.token)
    elif config_exists:
        # Use saved config (setup_gateway flow)
        print("\nUsing saved config (valyu_gateway_config.json)...")
        agent_ctx = get_agent_from_config()
    else:
        print("\nNo config found. Please either:")
        print("  1. Run setup_gateway.py first, OR")
        print("  2. Provide --gateway-url and --token")
        print("\nExample:")
        print("  python use_gateway.py --gateway-url https://your-gateway.../mcp --token YOUR_TOKEN")
        return

    print("Connecting to gateway...")

    with agent_ctx as agent:
        if args.interactive:
            run_interactive(agent)
        else:
            run_demo(agent)


if __name__ == "__main__":
    main()
