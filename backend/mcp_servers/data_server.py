import sys
import json
import logging
from typing import Dict, Any

# Import modular tool handlers
from mcp_servers.data_server_modules import (
    crm_tools,
    payment_tools,
    journey_tools,
    team_tools,
    communication_tools
)

# Registry of all 29 tools
TOOLS = {
    # CRM group
    "get_customer": crm_tools.get_customer,
    "get_policy": crm_tools.get_policy,
    "get_propensity_score": crm_tools.get_propensity_score,
    "search_policies_due": crm_tools.search_policies_due,
    "get_customer_by_policy": crm_tools.get_customer_by_policy,
    
    # Journey group
    "get_journey_state": journey_tools.get_journey_state,
    "create_journey": journey_tools.create_journey,
    "update_journey_state": journey_tools.update_journey_state,
    "write_audit_entry": journey_tools.write_audit_entry,
    "get_audit_trail": journey_tools.get_audit_trail,
    "append_conversation_message": journey_tools.append_conversation_message,
    "get_conversation_history": journey_tools.get_conversation_history,
    
    # Payment group
    "generate_payment_link": payment_tools.generate_payment_link,
    "check_payment_status": payment_tools.check_payment_status,
    "mark_payment": payment_tools.mark_payment,
    "generate_emi_plan": payment_tools.generate_emi_plan,
    "generate_revival_quotation": payment_tools.generate_revival_quotation,
    
    # Team group
    "escalate_to_human": team_tools.escalate_to_human,
    "get_queue": team_tools.get_queue,
    "assign_case": team_tools.assign_case,
    "update_case_status": team_tools.update_case_status,
    "resolve_case": team_tools.resolve_case,
    "get_team_status": team_tools.get_team_status,
    
    # Communication group
    "send_email": communication_tools.send_email,
    "send_whatsapp": communication_tools.send_whatsapp,
    "initiate_voice_call": communication_tools.initiate_voice_call,
    "get_message_status": communication_tools.get_message_status,
    "get_channel_stats": communication_tools.get_channel_stats
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
