import asyncio
import logging
from mcp_client.client import mcp

logging.basicConfig(level=logging.INFO)

async def test_all():
    try:
        print("\n--- Testing Data Server ---")
        customer = await mcp.call_tool("data", "get_customer", {"customer_id": "CUST-00001"})
        print(f"Customer CUST-00001: {customer.get('name', 'Not Found')}")
        
        journey = await mcp.call_tool("data", "create_journey", {"policy_id": "POL-001"})
        print(f"Created Journey: {journey.get('journey_id')}")

        print("\n--- Testing Knowledge Server ---")
        objections = await mcp.call_tool("knowledge", "search_objections", {"query": "premium too high"})
        print(f"Objections found: {len(objections.get('results', []))}")

        print("\n--- Testing Safety Server ---")
        safety = await mcp.call_tool("safety", "full_safety_check", {"content": "Your Aadhaar is 1234 5678 9012. You must pay today or lose everything!"})
        print(f"Approved: {safety.get('approved')}")
        print(f"Masked Text: {safety.get('final_content')}")
        print(f"Compliance issues: {safety.get('compliance', {}).get('issues')}")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        await mcp.shutdown()

if __name__ == "__main__":
    asyncio.run(test_all())
