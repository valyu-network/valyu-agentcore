# IAM Policies for AgentCore Gateway

Ready-to-use IAM policies for different access levels.

## Policies

### agentcore-user-policy.json

Full access to create and manage AgentCore Gateways with Cognito authentication.

**Use for:** Developers and admins who need to create/configure gateways.

```bash
aws iam create-policy \
  --policy-name AgentCoreUserPolicy \
  --policy-document file://agentcore-user-policy.json
```

**Permissions included:**
- Create, update, delete gateways
- Manage gateway targets (add Valyu, etc.)
- Invoke gateway tools
- Create Cognito resources for auth
- Pass IAM roles to Bedrock

### agentcore-invoke-only-policy.json

Minimal permissions to invoke gateway tools only.

**Use for:** Applications and services that just need to call tools.

```bash
aws iam create-policy \
  --policy-name AgentCoreInvokeOnlyPolicy \
  --policy-document file://agentcore-invoke-only-policy.json
```

**Permissions included:**
- Invoke gateway (call MCP tools)
- List available tools

## Attaching Policies

### To IAM User

```bash
aws iam attach-user-policy \
  --user-name your-username \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT:policy/AgentCoreUserPolicy
```

### To IAM Role

```bash
aws iam attach-role-policy \
  --role-name your-role \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT:policy/AgentCoreInvokeOnlyPolicy
```

### To EC2 Instance Profile

```bash
aws iam add-role-to-instance-profile \
  --instance-profile-name your-profile \
  --role-name your-role
```

## Scoping Permissions

For production, scope to specific gateways:

```json
{
  "Resource": "arn:aws:bedrock-agentcore:us-east-1:123456789:gateway/your-gateway-id"
}
```

Or by tag:

```json
{
  "Condition": {
    "StringEquals": {
      "aws:ResourceTag/Environment": "production"
    }
  }
}
```

## Service Control Policies (SCPs)

For AWS Organizations, you can restrict AgentCore to specific regions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AgentCoreRegionRestriction",
      "Effect": "Deny",
      "Action": "bedrock-agentcore:*",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-west-2"]
        }
      }
    }
  ]
}
```
