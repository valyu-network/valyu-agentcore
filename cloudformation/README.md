# CloudFormation Templates

Deploy supporting infrastructure for Valyu + AgentCore Gateway.

## What This Creates

The `valyu-gateway.yaml` template creates **authentication and supporting infrastructure**:

- **Cognito User Pool** - OAuth authentication for gateway access
- **Cognito App Client** - Client credentials for machine-to-machine auth
- **IAM Role** - Permissions for gateway to invoke tools
- **Secrets Manager** - Secure storage for Valyu API key
- **CloudWatch Log Group** - Audit logging

**Note:** This template creates the supporting infrastructure. You still need to create the AgentCore Gateway itself using either the Python SDK or AWS Console (see below).

## Quick Start

### Option 1: Python SDK (Recommended)

The simplest approach - creates everything including the gateway:

```python
from valyu_agentcore.gateway import setup_valyu_gateway, GatewayAgent

# Creates gateway + Cognito auth + Valyu target
setup_valyu_gateway()

# Use it
with GatewayAgent.from_config() as agent:
    response = agent("Search for NVIDIA SEC filings")
    print(response)
```

### Option 2: CloudFormation + Python SDK

Use CloudFormation for auth infrastructure, then add Valyu to your gateway:

```bash
# 1. Deploy auth infrastructure
aws cloudformation create-stack \
  --stack-name valyu-gateway \
  --template-body file://valyu-gateway.yaml \
  --parameters ParameterKey=ValyuApiKey,ParameterValue=YOUR_VALYU_API_KEY \
  --capabilities CAPABILITY_NAMED_IAM

# 2. Create gateway in AWS Console, then add Valyu target:
python -c "
from valyu_agentcore.gateway import add_valyu_target
add_valyu_target(gateway_id='your-gateway-id')
"
```

### Option 3: CloudFormation + AWS Console

1. Deploy the CloudFormation stack (see below)
2. Go to **Amazon Bedrock** > **AgentCore** > **Gateways**
3. Click **Create gateway**
4. Click **Add target** and use the `ValyuMcpEndpoint` from stack outputs

## Deploy via Console

1. Go to **CloudFormation** in AWS Console
2. Click **Create stack** > **With new resources**
3. Upload `valyu-gateway.yaml`
4. Enter parameters:
   - `ValyuApiKey`: Your key from [platform.valyu.ai](https://platform.valyu.ai)
   - `GatewayName`: Name for your gateway (default: `valyu-gateway`)
5. Click **Create stack**

## Deploy via CLI

```bash
aws cloudformation create-stack \
  --stack-name valyu-gateway \
  --template-body file://valyu-gateway.yaml \
  --parameters \
    ParameterKey=ValyuApiKey,ParameterValue=YOUR_VALYU_API_KEY \
  --capabilities CAPABILITY_NAMED_IAM
```

## Stack Outputs

| Output | Description |
|--------|-------------|
| `UserPoolId` | Cognito User Pool ID |
| `UserPoolClientId` | App client ID for authentication |
| `TokenEndpoint` | OAuth token endpoint URL |
| `GatewayRoleArn` | IAM role for the gateway |
| `ValyuMcpEndpoint` | Valyu MCP endpoint URL (use this when adding target) |

## Cleanup

```bash
aws cloudformation delete-stack --stack-name valyu-gateway
```

## IAM Permissions Required

To deploy this template, you need:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "cognito-idp:*",
        "iam:CreateRole",
        "iam:DeleteRole",
        "iam:PutRolePolicy",
        "iam:DeleteRolePolicy",
        "iam:PassRole",
        "secretsmanager:CreateSecret",
        "secretsmanager:DeleteSecret",
        "logs:CreateLogGroup",
        "logs:DeleteLogGroup"
      ],
      "Resource": "*"
    }
  ]
}
```
