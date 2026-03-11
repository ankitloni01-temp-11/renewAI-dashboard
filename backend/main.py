import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routers import (
    mock_apis, data_apis, conversation_apis,
    test_mcp_apis, elevenlabs_apis, dashboard_apis
)

START_TIME = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """MCP client lifecycle management."""
    print("[RenewAI] Starting up...")
    
    # Generate seed data if not exists (Data Server will load it)
    seed_dir = os.path.join(os.path.dirname(__file__), 'seed_data')
    customers_path = os.path.join(seed_dir, 'customers.json')
    
    if not os.path.exists(customers_path):
        print("[RenewAI] Generating seed data...")
        from scripts.generate_seed_data import main as generate
        generate()
    
    # Pre-connect to servers for faster first-load
    from mcp_client.client import mcp
    try:
        await mcp.connect("data")
        print("[RenewAI] Connected to Data Server.")
    except Exception as e:
        print(f"[RenewAI] Failed to connect to Data Server: {e}")

    yield
    
    print("[RenewAI] Shutting down...")
    from mcp_client.client import mcp
    await mcp.shutdown()


app = FastAPI(
    title="RenewAI Demo API",
    description="Suraksha Life Insurance AI-powered renewal system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(mock_apis.router)
app.include_router(data_apis.router)
app.include_router(conversation_apis.router)
app.include_router(test_mcp_apis.router)
app.include_router(elevenlabs_apis.router)
app.include_router(dashboard_apis.router)


@app.get("/")
async def root():
    from mcp_client.client import mcp
    stats = await mcp.call_tool("data", "get_channel_stats", {})
    return {
        "name": "RenewAI Demo API",
        "company": "Suraksha Life Insurance",
        "version": "1.0.0",
        "status": "running",
        "mcp_connected": True,
        "channel_stats": stats
    }

@app.get("/api/health")
@app.get("/health")
async def health():
    from mcp_client.client import mcp
    from config import GOOGLE_API_KEY
    
    uptime = int(time.time() - START_TIME)
    
    # Tool counts based on server source code analysis
    # In a real system, these would be fetched dynamically via mcp.list_tools()
    mcp_status = {
        "data": {"status": "ok", "uptime_seconds": uptime, "tool_count": 29},
        "knowledge": {"status": "ok", "uptime_seconds": uptime, "tool_count": 4},
        "safety": {"status": "ok", "uptime_seconds": uptime, "tool_count": 5}
    }
    
    # Check if servers are actually connected in MCP client
    connected_servers = mcp.processes.keys()
    for srv in mcp_status:
        if srv not in connected_servers:
            # Try to connect to verify status
            try:
                await mcp.connect(srv)
            except:
                mcp_status[srv]["status"] = "unavailable"

    return {
        "status": "ok",
        "mcp_servers": mcp_status,
        "gemini_api": "configured" if GOOGLE_API_KEY else "not_configured",
        "chromadb": "loaded"  # Knowledge server manages this
    }
