import asyncio
import json
import os
import sys

# Ensure backend directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_client.client import MCPClient

async def verify_mcp():
    client = MCPClient()
    print("Testing DATA server...")
    try:
        # Call a tool directly
        result = await client.call_tool("data", "get_customer", {"customer_id": "CUST-0001"})
        print(f"Data Result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Data Server Error: {e}")

    print("\nTesting SAFETY server...")
    try:
        result = await client.call_tool("safety", "detect_distress", {
            "content": "My husband passed away last month.",
            "language": "en"
        })
        print(f"Safety Result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Safety Server Error: {e}")

    await client.shutdown()

if __name__ == "__main__":
    asyncio.run(verify_mcp())
