import sys
import json
import os
from typing import Dict, Any, List
from rag.vector_store import search_objections as local_search_objections, search_policy_docs

# For demo purposes, we load these from seed files instead of store
SEED_DIR = "/home/labuser/VSCODE_training/renewai-demo/backend/seed_data"

def search_objections(arguments: Dict) -> Dict:
    query = arguments.get("query", "")
    n = arguments.get("n", 5)
    
    # Load from seed data for isolation
    path = os.path.join(SEED_DIR, "objection_library.json")
    items = []
    try:
        with open(path) as f:
            items = json.load(f)
    except:
        pass
        
    results = local_search_objections(query, items, n)
    return {"results": results}

def search_policy_documents(arguments: Dict) -> Dict:
    query = arguments.get("query", "")
    product_type = arguments.get("product_type")
    n = arguments.get("n", 3)
    results = search_policy_docs(query, product_type, n)
    return {"results": results}

def get_compliance_rules(arguments: Dict) -> Dict:
    path = os.path.join(SEED_DIR, "compliance_rules.json")
    try:
        with open(path) as f:
            data = json.load(f)
        return {"rules": data}
    except:
        return {"rules": []}

def get_distress_keywords(arguments: Dict) -> Dict:
    path = os.path.join(SEED_DIR, "distress_keywords.json")
    try:
        with open(path) as f:
            data = json.load(f)
        return {"keywords": data}
    except:
        return {"keywords": {}}

TOOLS = {
    "search_objections": search_objections,
    "search_policy_documents": search_policy_documents,
    "get_compliance_rules": get_compliance_rules,
    "get_distress_keywords": get_distress_keywords
}

def main():
    """Main loop for JSON-RPC over stdio."""
    for line in sys.stdin:
        try:
            request = json.loads(line)
            req_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "call_tool":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name in TOOLS:
                    result = TOOLS[tool_name](arguments)
                    response = {"jsonrpc": "2.0", "result": result, "id": req_id}
                else:
                    response = {"jsonrpc": "2.0", "error": f"Tool '{tool_name}' not found", "id": req_id}
            else:
                response = {"jsonrpc": "2.0", "error": f"Method '{method}' not implemented", "id": req_id}
            
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        except Exception as e:
            sys.stderr.write(f"Error: {str(e)}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()
