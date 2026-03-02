import sys
import json
import re
from typing import Dict, Any, List

# PII patterns
AADHAAR_PATTERN = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')
PAN_PATTERN = re.compile(r'\b[A-Z]{5}\d{4}[A-Z]{1}\b')
PHONE_PATTERN = re.compile(r'(\+91[\-\s]?)?[6-9]\d{9}')
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

# Banned phrases
GUARANTEED_RETURNS = ["guaranteed return", "guaranteed profit", "assured return"]
PRESSURE_LANGUAGE = ["must pay today or lose everything", "last chance or policy cancelled"]

# Simplified distress check (Knowledge server will handle the full DB eventually)
DISTRESS_KEYWORDS = ["died", "passed away", "expired", "hospital", "accident", "emergency"]

def scan_pii(arguments: Dict) -> Dict:
    text = arguments.get("text", "")
    findings = []
    masked_text = text
    
    # Aadhaar
    aadhaar_matches = AADHAAR_PATTERN.findall(text)
    if aadhaar_matches:
        findings.append({"type": "aadhaar", "count": len(aadhaar_matches)})
        masked_text = AADHAAR_PATTERN.sub("XXXX-XXXX-XXXX", masked_text)

    # Phone
    phone_matches = PHONE_PATTERN.findall(text)
    if phone_matches:
        findings.append({"type": "phone", "count": len(phone_matches)})
        masked_text = PHONE_PATTERN.sub("+91-XXXXXXXXXX", masked_text)

    return {"pii_detected": len(findings) > 0, "findings": findings, "masked_text": masked_text}

def detect_distress(arguments: Dict) -> Dict:
    content = arguments.get("content", "").lower()
    detected = [kw for kw in DISTRESS_KEYWORDS if kw in content]
    return {
        "distress_detected": len(detected) > 0,
        "distress_keywords": detected,
        "action": "escalate" if detected else "none"
    }

def check_compliance(arguments: Dict) -> Dict:
    text = arguments.get("text", "").lower()
    issues = []
    
    # AI self-id
    #ai_phrases = ["ai", "bot", "assistant", "automated"]
    #if not any(p in text for p in ai_phrases):
    #    issues.append("Missing AI self-identification")
        
    for p in PRESSURE_LANGUAGE:
        if p in text:
            issues.append(f"Pressure language detected: {p}")
            
    return {"compliant": len(issues) == 0, "issues": issues}

def check_misselling(arguments: Dict) -> Dict:
    text = arguments.get("text", "").lower()
    issues = [p for p in GUARANTEED_RETURNS if p in text]
    return {"misselling_detected": len(issues) > 0, "issues": issues}

def full_safety_check(arguments: Dict) -> Dict:
    content = arguments.get("content", "")
    pii = scan_pii({"text": content})
    distress = detect_distress({"content": content})
    compliance = check_compliance({"text": content})
    misselling = check_misselling({"text": content})
    
    approved = not (distress["distress_detected"] or misselling["misselling_detected"] or not compliance["compliant"])
    
    return {
        "approved": approved,
        "pii": pii,
        "distress": distress,
        "compliance": compliance,
        "misselling": misselling,
        "final_content": pii["masked_text"]
    }

TOOLS = {
    "scan_pii": scan_pii,
    "detect_distress": detect_distress,
    "check_compliance": check_compliance,
    "check_misselling": check_misselling,
    "full_safety_check": full_safety_check
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
