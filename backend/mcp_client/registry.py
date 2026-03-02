"""Registry of MCP servers for the RenewAI project."""

SERVERS = {
    "data": {
        "command": "python",
        "args": ["-m", "mcp_servers.data_server"],
        "description": "Customer data, policy data, payments, journey state, audit trail, human queue, team management",
        "timeout_seconds": 10,
    },
    "knowledge": {
        "command": "python",
        "args": ["-m", "mcp_servers.knowledge_server"],
        "description": "RAG retrieval from ChromaDB for objection library and policy documents",
        "timeout_seconds": 15,
    },
    "safety": {
        "command": "python",
        "args": ["-m", "mcp_servers.safety_server"],
        "description": "PII scanning, IRDAI compliance checking, distress detection, mis-selling detection",
        "timeout_seconds": 5,
    },
}
