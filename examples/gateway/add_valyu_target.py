"""
Add Valyu to Existing AgentCore Gateway

Add Valyu search tools to your existing AWS Bedrock AgentCore Gateway.
This is the recommended approach for enterprises.

Usage:
    export VALYU_API_KEY=your-api-key

    # Add Valyu to your gateway
    python add_valyu_target.py --gateway-id your-gateway-id

    # List targets
    python add_valyu_target.py --gateway-id your-gateway-id --list

    # Remove target
    python add_valyu_target.py --gateway-id your-gateway-id --remove TARGET_ID
"""

import argparse
import sys
from valyu_agentcore.gateway import add_valyu_target


def list_targets(gateway_id: str, region: str = "us-east-1"):
    """List targets in the gateway."""
    import boto3

    client = boto3.client("bedrock-agentcore-control", region_name=region)
    targets = client.list_gateway_targets(gatewayIdentifier=gateway_id)

    print(f"\nTargets in gateway {gateway_id}:")
    for target in targets.get("items", []):
        print(f"  - {target['name']} ({target['targetId']}): {target['status']}")

    if not targets.get("items"):
        print("  (no targets)")


def remove_target(gateway_id: str, target_id: str, region: str = "us-east-1"):
    """Remove a target from the gateway."""
    import boto3

    client = boto3.client("bedrock-agentcore-control", region_name=region)
    print(f"Removing target {target_id}...")
    client.delete_gateway_target(gatewayIdentifier=gateway_id, targetId=target_id)
    print("Done!")


def main():
    parser = argparse.ArgumentParser(
        description="Add Valyu search tools to your AgentCore Gateway"
    )
    parser.add_argument(
        "--gateway-id",
        required=True,
        help="Your AgentCore Gateway ID",
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (default: us-east-1)",
    )
    parser.add_argument(
        "--target-name",
        default="valyu-search",
        help="Name for the Valyu target (default: valyu-search)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List current targets in the gateway",
    )
    parser.add_argument(
        "--remove",
        metavar="TARGET_ID",
        help="Remove a target",
    )

    args = parser.parse_args()

    if args.list:
        list_targets(args.gateway_id, args.region)
        return

    if args.remove:
        remove_target(args.gateway_id, args.remove, args.region)
        return

    # Add Valyu target
    print("=" * 60)
    print("Add Valyu to AgentCore Gateway")
    print("=" * 60)
    print()

    try:
        result = add_valyu_target(
            gateway_id=args.gateway_id,
            region=args.region,
            target_name=args.target_name,
        )

        print("\n" + "=" * 60)
        print("Success!")
        print("=" * 60)
        print(f"\nTarget ID: {result['target_id']}")
        print(f"Gateway ID: {result['gateway_id']}")
        print("""
Available tools (via your gateway):
  - valyu_search           : Web search
  - valyu_academic_search  : Academic papers
  - valyu_financial_search : Financial data
  - valyu_sec_search       : SEC filings
  - valyu_patents          : Patent search
  - valyu_contents         : URL extraction

Example usage with your existing agent:

    from strands import Agent
    from strands.models import BedrockModel
    from strands.tools.mcp.mcp_client import MCPClient
    from mcp.client.streamable_http import streamablehttp_client

    def create_transport():
        return streamablehttp_client(
            "YOUR_GATEWAY_URL/mcp",
            headers={"Authorization": f"Bearer {your_token}"}
        )

    with MCPClient(create_transport) as mcp:
        agent = Agent(
            model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
            tools=mcp.list_tools_sync(),
        )
        response = agent("Search for NVIDIA SEC filings")
""")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()