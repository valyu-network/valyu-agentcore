"""
Setup Valyu + AgentCore Gateway

This script creates an AgentCore Gateway with Valyu search tools.
Run once to set up, then use the agent in your applications.

Prerequisites:
    1. AWS credentials configured (aws configure)
    2. Valyu API key (https://platform.valyu.ai)
    3. Install dependencies: pip install valyu-agentcore[agentcore]

Usage:
    # Set your Valyu API key
    export VALYU_API_KEY=your-api-key

    # Run setup
    python setup_gateway.py

    # This creates valyu_gateway_config.json with your gateway details
"""

import os
from valyu_agentcore.gateway import setup_valyu_gateway, cleanup_valyu_gateway


def main():
    print("=" * 60)
    print("Valyu + AgentCore Gateway Setup")
    print("=" * 60)

    # Check for API key
    api_key = os.environ.get("VALYU_API_KEY")
    if not api_key:
        print("\nError: VALYU_API_KEY environment variable not set.")
        print("Get your API key at: https://platform.valyu.ai")
        print("\nSet it with: export VALYU_API_KEY=your-api-key")
        return

    print(f"\nUsing Valyu API key: {api_key[:8]}...")
    print("Region: us-east-1")
    print()

    try:
        # Set up the gateway
        config = setup_valyu_gateway(
            valyu_api_key=api_key,
            gateway_name="valyu-search-gateway",
            target_name="valyu-mcp",
            region="us-east-1",
        )

        print("\n" + "=" * 60)
        print("Setup Complete!")
        print("=" * 60)
        print(f"\nGateway URL: {config.gateway_url}")
        print(f"Config saved to: valyu_gateway_config.json")
        print("\nNext steps:")
        print("  1. Run: python use_gateway.py")
        print("  2. Or use GatewayAgent.from_config() in your code")

    except Exception as e:
        print(f"\nError during setup: {e}")
        raise


def cleanup():
    """Run this to delete all gateway resources."""
    print("Cleaning up gateway resources...")
    cleanup_valyu_gateway()
    print("Done!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        cleanup()
    else:
        main()
