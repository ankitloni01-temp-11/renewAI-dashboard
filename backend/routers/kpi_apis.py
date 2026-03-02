"""KPI computation and serving using MCP."""
from fastapi import APIRouter
from mcp_client.client import mcp

router = APIRouter(prefix="/api/kpis", tags=["kpis"])

@router.get("")
async def get_kpis():
    # In a real app, the Data Server would have a compute_kpis tool.
    # For demo, we'll return the static/compute logic based on MCP data.
    return {
        "persistency_rat_13m": 88.5,
        "collection_efficiency": 94.2,
        "avg_handling_time_reduction_pct": 65,
        "cost_per_renewal_rs": 45,
        "nps_score": 72,
        "compliance_adherence_pct": 99.8,
        "distress_detection_accuracy": 96.5,
        "agent_utilization_pct": 22,
        "annual_saving_crores": 12.9,
        "revenue_uplift_pct": 38.9
    }

@router.get("/channel-performance")
async def channel_performance():
    stats = await mcp.call_tool("data", "get_channel_stats", {})
    return {
        "email": {"sent": stats.get("email", 0), "open_rate": 44.1, "conversion_rate": 35.2},
        "whatsapp": {"sent": stats.get("whatsapp", 0), "response_rate": 54.3, "conversion_rate": 41.8},
        "voice": {"calls": stats.get("voice", 0), "answer_rate": 62.1, "conversion_rate": 29.1},
        "total_paid": 0 # Would need to check journeys
    }

@router.get("/financial")
async def financial_kpis():
    return {
        "annual_cost_current": 18.6,
        "annual_cost_projected": 5.7,
        "annual_saving": 12.9,
        "revenue_uplift": 38.9,
        "investment": 3.78,
        "net_year1": 48.0,
        "npv_3yr": 89.0,
        "payback_months": 7.8,
        "monthly_data": [
            {"month": "Jan 2026", "cost_saving": 1.075, "revenue_uplift": 3.24},
            {"month": "Feb 2026", "cost_saving": 1.075, "revenue_uplift": 3.24},
            {"month": "Mar 2026", "cost_saving": 1.075, "revenue_uplift": 3.24}
        ]
    }

@router.get("/team-performance")
async def team_performance():
    team = await mcp.call_tool("data", "get_team_status", {})
    return {"team": [
        {**t, "retained_premium": t.get("cases_this_week", 0) * 22400}
        for t in team if t.get("cases_this_week", 0) > 0
    ]}
