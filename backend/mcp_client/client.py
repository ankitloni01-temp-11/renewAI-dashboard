"""Unified MCP Client for RenewAI agents."""
import asyncio
import json
import logging
import subprocess
import uuid
from typing import Dict, Any, Optional
from mcp_client.registry import SERVERS

logger = logging.getLogger("mcp_client")

class MCPClient:
    """A client that manages connections to multiple MCP servers over stdio."""
    
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.pending_requests: Dict[str, asyncio.Future] = {}
        self.lock = asyncio.Lock()

    async def connect(self, server_name: str):
        """Connect to an MCP server if not already connected."""
        if server_name in self.processes:
            return

        config = SERVERS.get(server_name)
        if not config:
            raise ValueError(f"Server '{server_name}' not found in registry.")

        logger.info(f"Connecting to MCP server: {server_name}")
        
        # Start server as a subprocess using stdio
        process = subprocess.Popen(
            [config["command"]] + config["args"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd="/home/labuser/VSCODE_training/renewai-demo/backend"
        )
        
        self.processes[server_name] = process
        
        # Start background reader for this server
        asyncio.create_task(self._read_loop(server_name))

    async def _read_loop(self, server_name: str):
        """Read JSON-RPC responses from the server's stdout."""
        process = self.processes[server_name]
        try:
            while True:
                line = await asyncio.to_thread(process.stdout.readline)
                if not line:
                    break
                
                try:
                    response = json.loads(line)
                    req_id = response.get("id")
                    if req_id in self.pending_requests:
                        self.pending_requests[req_id].set_result(response)
                except json.JSONDecodeError:
                    logger.error(f"Failed to decode MCP response from {server_name}: {line}")
        except Exception as e:
            logger.error(f"Error in MCP read loop for {server_name}: {e}")

    async def call_tool(self, server_name: str, tool_name: str, arguments: Optional[Dict] = None) -> Dict[str, Any]:
        """Call an MCP tool on a specific server."""
        await self.connect(server_name)
        
        req_id = str(uuid.uuid4())
        request = {
            "jsonrpc": "2.0",
            "method": "call_tool",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            },
            "id": req_id
        }
        
        future = asyncio.get_running_loop().create_future()
        self.pending_requests[req_id] = future
        
        process = self.processes[server_name]
        async with self.lock:
            process.stdin.write(json.dumps(request) + "\n")
            process.stdin.flush()
        
        try:
            # Wait for response with timeout
            config = SERVERS.get(server_name, {})
            timeout = config.get("timeout_seconds", 10)
            
            response = await asyncio.wait_for(future, timeout=timeout)
            
            if "error" in response:
                raise RuntimeError(f"MCP Tool Error ({server_name}/{tool_name}): {response['error']}")
            
            return response.get("result", {})
            
        finally:
            self.pending_requests.pop(req_id, None)

    async def shutdown(self):
        """Close all server connections."""
        for name, process in self.processes.items():
            logger.info(f"Shutting down MCP server: {name}")
            process.terminate()
        self.processes.clear()

# Singleton client instance
mcp = MCPClient()
