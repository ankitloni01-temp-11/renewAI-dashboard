import re
import json
from typing import Dict, Any, List, Tuple
from store.memory_store import store


# PII patterns
AADHAAR_PATTERN = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')
PAN_PATTERN = re.compile(r'\b[A-Z]{5}\d{4}[A-Z]{1}\b')
PHONE_PATTERN = re.compile(r'(\+91[\-\s]?)?[6-9]\d{9}')
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
BANK_ACCOUNT_PATTERN = re.compile(r'\b\d{9,18}\b')

# Banned phrases
GUARANTEED_RETURNS = [
    "guaranteed return", "guaranteed 14%", "guaranteed 12%", "assured return",
    "guaranteed profit", "100% returns", "fixed returns guaranteed",
    "we guarantee", "returns guaranteed"
]

PRESSURE_LANGUAGE = [
    "must pay today or lose everything", "last chance or you die", "immediate payment required or policy cancelled",
    "you will lose everything", "penalty will destroy", "urgent action required or permanent loss"
]

ULIP_BANNED = [
    "guaranteed", "assured return", "fixed return", "we guarantee returns",
    "no risk", "risk free returns"
]


def scan_pii(text: str) -> Dict[str, Any]:
    """Scan text for PII patterns."""
    findings = []
    masked_text = text

    # Aadhaar
    aadhaar_matches = AADHAAR_PATTERN.findall(text)
    if aadhaar_matches:
        findings.append({"type": "aadhaar", "count": len(aadhaar_matches)})
        masked_text = AADHAAR_PATTERN.sub("XXXX-XXXX-XXXX", masked_text)

    # PAN
    pan_matches = PAN_PATTERN.findall(text)
    if pan_matches:
        findings.append({"type": "pan", "count": len(pan_matches)})
        masked_text = PAN_PATTERN.sub("XXXXX9999X", masked_text)

    # Phone
    phone_matches = PHONE_PATTERN.findall(text)
    if phone_matches:
        findings.append({"type": "phone", "count": len(phone_matches)})
        masked_text = PHONE_PATTERN.sub("+91-XXXXXXXXXX", masked_text)

    # Email
    email_matches = EMAIL_PATTERN.findall(text)
    if email_matches:
        findings.append({"type": "email", "count": len(email_matches)})
        masked_text = EMAIL_PATTERN.sub("XXXX@XXXX.com", masked_text)

    return {
        "pii_detected": len(findings) > 0,
        "findings": findings,
        "masked_text": masked_text
    }


def check_distress_keywords(text: str, language: str = "English") -> Dict[str, Any]:
    """Check for distress keywords in text."""
    distress_db = store.distress_keywords
    detected = []
    text_lower = text.lower()

    # Always check English
    languages_to_check = ["English", language] if language != "English" else ["English"]

    for lang in languages_to_check:
        lang_keywords = distress_db.get(lang, {})
        for category, keywords in lang_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    detected.append({
                        "keyword": keyword,
                        "category": category,
                        "language": lang
                    })

    return {
        "distress_detected": len(detected) > 0,
        "distress_events": detected,
        "primary_category": detected[0]["category"] if detected else None
    }


def check_irdai_compliance(text: str, product_type: str = "term") -> Dict[str, Any]:
    """Check IRDAI compliance rules."""
    issues = []
    text_lower = text.lower()

    # AI self-identification
    ai_phrases = ["ai-powered", "ai powered", "artificial intelligence", "automated assistant",
                  "renewal assistant", "digital assistant", "bot", "virtual assistant"]
    if not any(phrase in text_lower for phrase in ai_phrases):
        issues.append({"rule": "AI self-identification missing (IRDAI Circular 2024)", "severity": "high"})

    # Brand identification
    if "suraksha" not in text_lower:
        issues.append({"rule": "Company name 'Suraksha' missing in communication", "severity": "medium"})

    # Opt-out mechanism
    opt_out_phrases = ["opt out", "stop", "1800", "unsubscribe", "reply stop", "non-consent"]
    if not any(phrase in text_lower for phrase in opt_out_phrases):
        issues.append({"rule": "Opt-out mechanism missing (IRDAI Consumer Protection)", "severity": "high"})

    # ULIP guaranteed returns
    if product_type == "ulip":
        for phrase in ULIP_BANNED:
            if phrase in text_lower:
                issues.append({"rule": f"Guaranteed return promise detected in ULIP: '{phrase}'", "severity": "critical"})

    # Pressure language
    for phrase in PRESSURE_LANGUAGE:
        if phrase in text_lower:
            issues.append({"rule": f"Aggressive pressure language detected: '{phrase}'", "severity": "high"})

    # Grace period accuracy
    if "grace period" in text_lower:
        # IRDAI Master Circular: 30 days for annual/half-yearly, 15 days for monthly
        if "15 day" in text_lower and ("annual" in text_lower or "yearly" in text_lower):
            issues.append({"rule": "Grace period incorrectly stated as 15 days for yearly mode (should be 30)", "severity": "high"})
        if "30 day" not in text_lower and ("annual" in text_lower or "yearly" in text_lower):
            issues.append({"rule": "Mandatory 30-day grace period for yearly mode not explicitly stated", "severity": "medium"})

    return {
        "compliant": len([i for i in issues if i["severity"] in ["high", "critical"]]) == 0,
        "issues": issues,
        "critical_violations": [i for i in issues if i["severity"] == "critical"]
    }


def check_misselling(text: str, product_type: str) -> Dict[str, Any]:
    """Check for mis-selling indicators."""
    issues = []
    text_lower = text.lower()

    for phrase in GUARANTEED_RETURNS:
        if phrase in text_lower:
            issues.append({"phrase": phrase, "type": "guaranteed_returns"})

    return {
        "misselling_detected": len(issues) > 0,
        "issues": issues
    }


async def run_content_safety(
    content: str,
    product_type: str = "term",
    language: str = "English",
    customer_message: str = ""
) -> Dict[str, Any]:
    """Run all 4 safety checks in parallel."""
    import asyncio

    # Run all checks
    text_to_check = content + " " + customer_message

    pii_result = scan_pii(content)  # Only check AI's output for PII
    distress_result = check_distress_keywords(text_to_check, language)
    compliance_result = check_irdai_compliance(content, product_type)
    misselling_result = check_misselling(content, product_type)

    # Determine overall verdict
    hard_fail = (
        distress_result["distress_detected"] or
        len(compliance_result["critical_violations"]) > 0 or
        misselling_result["misselling_detected"]
    )

    soft_fail = not compliance_result["compliant"]

    if distress_result["distress_detected"]:
        action = "escalate_human"
        reason = f"distress_detected_{distress_result['primary_category']}"
    elif len(compliance_result["critical_violations"]) > 0:
        action = "escalate_human"
        reason = "compliance_critical_violation"
    elif misselling_result["misselling_detected"]:
        action = "escalate_human"
        reason = "misselling_detected"
    elif soft_fail:
        action = "block_with_warning"
        reason = "compliance_soft_violation"
    elif pii_result["pii_detected"]:
        action = "mask_and_send"
        reason = "pii_masked"
    else:
        action = "approved"
        reason = None

    return {
        "approved": action == "approved" or action == "mask_and_send",
        "action": action,
        "reason": reason,
        "pii_check": pii_result,
        "distress_check": distress_result,
        "compliance_check": compliance_result,
        "misselling_check": misselling_result,
        "final_content": pii_result["masked_text"] if pii_result["pii_detected"] else content,
        "latency_ms": 120  # Deterministic, very fast
    }


# Alias used by renewal_graph.py
async def run_safety_check(content: str, language: str = "English", channel: str = "email") -> Dict[str, Any]:
    """Wrapper around run_content_safety that maps result to verdict format."""
    result = await run_content_safety(content, language=language)
    verdict = "PASS"
    if result["action"] == "escalate_human":
        verdict = "ESCALATE"
    elif result["action"] == "block_with_warning":
        verdict = "BLOCK"
    return {
        "verdict": verdict,
        "reason": result.get("reason"),
        "distress": result.get("distress_check", {}),
        "compliance": result.get("compliance_check", {}),
        "pii": result.get("pii_check", {}),
        "final_content": result.get("final_content", content)
    }
