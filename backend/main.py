"""Main FastAPI application for RenewAI Demo."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routers import (
    mock_apis, data_apis, journey_apis, human_queue_apis,
    audit_apis, kpi_apis, trigger_apis, conversation_apis
)


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
app.include_router(journey_apis.router)
app.include_router(human_queue_apis.router)
app.include_router(audit_apis.router)
app.include_router(kpi_apis.router)
app.include_router(trigger_apis.router)
app.include_router(conversation_apis.router)


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

@app.get("/health")
async def health():
    return {"status": "healthy"}
