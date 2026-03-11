import asyncio
import json
from mcp_client.client import mcp

async def main():
    policy_id = "SLI-2298741"
    logs = await mcp.call_tool("data", "get_audit", {"policy_id": policy_id})
    print(json.dumps(logs, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
