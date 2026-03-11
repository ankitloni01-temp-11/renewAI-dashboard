import pytest

@pytest.mark.asyncio
async def test_get_rajesh(mcp):
    result = await mcp.call_tool("data", "get_customer", {"customer_id": "CUST-00001"})
    assert result["success"] is True if "success" in result else True
    # If the tool returns data directly
    data = result.get("data", result)
    assert "Rajesh" in data["name"]
    assert data["preferred_channel"] == "whatsapp"

@pytest.mark.asyncio
async def test_get_rajesh_policy(mcp):
    result = await mcp.call_tool("data", "get_policy", {"policy_id": "SLI-2298741"})
    data = result.get("data", result)
    assert data["product_name"] == "Suraksha Term Shield"
    assert data["premium_amount"] == 24000
    assert data["sum_assured"] == 10000000

@pytest.mark.asyncio
async def test_customer_not_found(mcp):
    result = await mcp.call_tool("data", "get_customer", {"customer_id": "CUST-9999"})
    # Data server tools seem to return error dicts based on main.py health check logic
    assert "error" in result

@pytest.mark.asyncio
async def test_propensity_score_structure(mcp):
    result = await mcp.call_tool("data", "get_propensity_score", {"policy_id": "SLI-2298741"})
    data = result.get("data", result)
    assert 0 <= data["propensity_score"] <= 100
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    assert isinstance(data["top_risk_factors"], list)

@pytest.mark.asyncio
async def test_objection_affordability(mcp):
    result = await mcp.call_tool("knowledge", "search_objections", {
        "query": "I cannot afford the premium right now", 
        "language": "en", 
        "top_k": 3
    })
    # Knowledge tools return a list of results
    assert isinstance(result, list)
    assert len(result) > 0
    assert any("financial" in r.get("category", "").lower() or "afford" in r.get("response", "").lower() for r in result)

@pytest.mark.asyncio
async def test_distress_bereavement_en(mcp):
    result = await mcp.call_tool("safety", "detect_distress", {
        "content": "My husband passed away last month. I do not know what to do with this policy.",
        "language": "en"
    })
    assert result["distress_detected"] is True
    assert result["category"] == "bereavement"
    assert result["recommended_action"] == "HALT_AND_ESCALATE"

@pytest.mark.asyncio
async def test_pii_detection(mcp):
    result = await mcp.call_tool("safety", "scan_pii", {
        "content": "My Aadhaar number is 1234 5678 9012. Call me on 9876543210."
    })
    assert result["pii_found"] is True
    assert "[REDACTED]" in result["masked_content"]

@pytest.mark.asyncio
async def test_policy_doc_grace_period(mcp):
    result = await mcp.call_tool("knowledge", "search_policy_documents", {
        "query": "grace period",
        "product_type": "term"
    })
    results = result.get("results", [])
    assert isinstance(results, list)
    assert len(results) > 0
    assert any("grace" in r.get("content", "").lower() for r in results)
