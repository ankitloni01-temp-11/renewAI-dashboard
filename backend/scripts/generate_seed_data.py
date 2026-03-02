#!/usr/bin/env python3
"""Generate all seed data for RenewAI demo."""
import json
import random
import uuid
from datetime import datetime, timedelta
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "seed_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Indian name pool by region
NAMES_BY_STATE = {
    "Maharashtra": {
        "first": ["Rajesh", "Priya", "Suresh", "Anjali", "Vikram", "Sneha", "Anil", "Pooja", "Rahul", "Sunita", "Manoj", "Deepa", "Prakash", "Kavita", "Sachin"],
        "last": ["Sharma", "Patil", "Deshmukh", "Joshi", "Kulkarni", "Deshpande", "More", "Shinde", "Bhosale", "Pawar"],
        "language": "Marathi"
    },
    "Tamil Nadu": {
        "first": ["Meenakshi", "Karthik", "Lakshmi", "Ravi", "Anand", "Kavitha", "Murugan", "Preethi", "Selvam", "Geetha"],
        "last": ["Iyer", "Krishnamurthy", "Venkataraman", "Subramanian", "Sundaram", "Natarajan", "Pillai", "Rajan", "Muthusamy", "Thangavel"],
        "language": "Tamil"
    },
    "Karnataka": {
        "first": ["Suresh", "Anitha", "Ramesh", "Savitha", "Girish", "Mamatha", "Vinod", "Rekha", "Prasad", "Shwetha"],
        "last": ["Gowda", "Naik", "Hegde", "Shetty", "Rao", "Murthy", "Nair", "Reddy", "Kumar", "Patel"],
        "language": "Kannada"
    },
    "West Bengal": {
        "first": ["Sourav", "Priya", "Arnab", "Sudeshna", "Biswajit", "Rupa", "Debashis", "Moumita", "Ayan", "Sohini"],
        "last": ["Chatterjee", "Banerjee", "Mukherjee", "Ghosh", "Das", "Sen", "Bose", "Roy", "Dutta", "Chakraborty"],
        "language": "Bengali"
    },
    "Gujarat": {
        "first": ["Jigar", "Hetal", "Nilesh", "Komal", "Bhavesh", "Reena", "Chirag", "Nidhi", "Parth", "Foram"],
        "last": ["Shah", "Patel", "Mehta", "Desai", "Modi", "Joshi", "Trivedi", "Gandhi", "Bhatt", "Parikh"],
        "language": "Gujarati"
    },
    "Telangana": {
        "first": ["Venkatesh", "Padmaja", "Srinivas", "Madhavi", "Aravind", "Swathi", "Ramu", "Kavya", "Naresh", "Deepika"],
        "last": ["Reddy", "Rao", "Kumar", "Sharma", "Nair", "Naidu", "Yadav", "Murthy", "Prasad", "Babu"],
        "language": "Telugu"
    },
    "Kerala": {
        "first": ["Arun", "Divya", "Sreejith", "Anjitha", "Vishnu", "Nisha", "Rajesh", "Lekha", "Sujith", "Bindhu"],
        "last": ["Nair", "Menon", "Pillai", "Varma", "Thomas", "George", "Mathew", "Jose", "Kumar", "Krishnan"],
        "language": "Malayalam"
    },
    "Delhi": {
        "first": ["Amit", "Neha", "Sanjay", "Priyanka", "Ravi", "Shweta", "Deepak", "Pooja", "Vikas", "Ritika"],
        "last": ["Sharma", "Gupta", "Singh", "Verma", "Agarwal", "Khanna", "Malhotra", "Arora", "Bhatia", "Kapoor"],
        "language": "Hindi"
    },
    "Uttar Pradesh": {
        "first": ["Ram", "Sita", "Lakhan", "Geeta", "Vijay", "Savitri", "Sunil", "Rekha", "Ashok", "Meera"],
        "last": ["Singh", "Yadav", "Gupta", "Sharma", "Tiwari", "Tripathi", "Pandey", "Mishra", "Shukla", "Srivastava"],
        "language": "Hindi"
    }
}

STATES = list(NAMES_BY_STATE.keys())
PRODUCTS = [
    {"name": "Suraksha Term Shield", "type": "term", "premium_range": (12000, 48000), "sa_multiplier": (25, 50)},
    {"name": "Suraksha Endowment Plus", "type": "endowment", "premium_range": (15000, 36000), "sa_multiplier": (15, 30)},
    {"name": "Suraksha Wealth Builder ULIP", "type": "ulip", "premium_range": (50000, 500000), "sa_multiplier": (10, 20)},
    {"name": "Suraksha Pension Secure", "type": "pension", "premium_range": (24000, 60000), "sa_multiplier": (10, 20)},
    {"name": "Suraksha Child Future Plan", "type": "child", "premium_range": (10000, 30000), "sa_multiplier": (20, 40)},
]

SEGMENTS = ["wealth_builder", "budget_conscious", "loyal_long_term", "new_customer", "hni", "tech_savvy"]
CONTACT_TIMES = ["morning", "afternoon", "evening"]
CHANNELS = ["whatsapp", "email", "voice"]


def random_phone():
    return f"+91{random.randint(7000000000, 9999999999)}"


def random_email(name):
    domains = ["gmail.com", "yahoo.com", "outlook.com", "rediffmail.com"]
    clean = name.lower().replace(" ", ".").replace("'", "")
    return f"{clean}{random.randint(1, 999)}@{random.choice(domains)}"


def generate_payment_history(tenure, lapse_probability=0.1):
    history = []
    for year in range(1, tenure + 1):
        if random.random() < lapse_probability:
            status = random.choice(["late_7_days", "missed"])
        elif random.random() < 0.15:
            status = "late_3_days"
        else:
            status = "on_time"
        history.append({"year": year, "status": status})
    return history


def generate_customers(n=500):
    customers = []
    for i in range(n):
        state = random.choice(STATES)
        info = NAMES_BY_STATE[state]
        first = random.choice(info["first"])
        last = random.choice(info["last"])
        name = f"{first} {last}"
        lang = info["language"]
        # Some fallback to Hindi or English
        if random.random() < 0.2:
            lang = random.choice(["Hindi", "English"])

        channel = random.choices(CHANNELS, weights=[40, 35, 25])[0]
        contact_time = random.choices(CONTACT_TIMES, weights=[20, 30, 50])[0]
        tenure = random.randint(1, 20)
        segment = random.choice(SEGMENTS)

        c = {
            "customer_id": f"CUST-{str(i+1).zfill(5)}",
            "name": name,
            "age": random.randint(25, 65),
            "phone": random_phone(),
            "email": random_email(name),
            "preferred_language": lang,
            "preferred_channel": channel,
            "preferred_contact_time": contact_time,
            "segment": segment,
            "tenure_years": tenure,
            "complaint_count": random.choices([0, 1, 2], weights=[75, 20, 5])[0],
            "city": state,
            "state": state
        }
        customers.append(c)

    # Override first 3 for named customers
    customers[0] = {
        "customer_id": "CUST-00001",
        "name": "Rajesh Sharma",
        "age": 42,
        "phone": "+919876543210",
        "email": "rajesh.sharma42@gmail.com",
        "preferred_language": "Hindi",
        "preferred_channel": "whatsapp",
        "preferred_contact_time": "evening",
        "segment": "budget_conscious",
        "tenure_years": 5,
        "complaint_count": 0,
        "city": "Mumbai",
        "state": "Maharashtra"
    }
    customers[1] = {
        "customer_id": "CUST-00002",
        "name": "Meenakshi Iyer",
        "age": 58,
        "phone": "+919123456789",
        "email": "meenakshi.iyer@yahoo.com",
        "preferred_language": "Tamil",
        "preferred_channel": "whatsapp",
        "preferred_contact_time": "morning",
        "segment": "loyal_long_term",
        "tenure_years": 8,
        "complaint_count": 0,
        "city": "Chennai",
        "state": "Tamil Nadu"
    }
    customers[2] = {
        "customer_id": "CUST-00003",
        "name": "Vikram Malhotra",
        "age": 35,
        "phone": "+919988776655",
        "email": "vikram.malhotra@outlook.com",
        "preferred_language": "English",
        "preferred_channel": "email",
        "preferred_contact_time": "afternoon",
        "segment": "tech_savvy",
        "tenure_years": 3,
        "complaint_count": 0,
        "city": "Delhi",
        "state": "Delhi"
    }
    return customers


def generate_policies(customers):
    policies = []
    base_date = datetime(2026, 3, 1)

    for i, cust in enumerate(customers):
        product = random.choice(PRODUCTS)
        tenure = cust["tenure_years"]
        premium = round(random.randint(*product["premium_range"]) / 1000) * 1000
        sa_mult = random.uniform(*product["sa_multiplier"])
        sum_assured = round(premium * sa_mult / 1000) * 1000

        # Due dates scattered across March-April 2026
        days_offset = random.randint(0, 60)
        due_date = (base_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")

        policy = {
            "policy_id": f"SLI-{random.randint(100000, 999999)}",
            "customer_id": cust["customer_id"],
            "product_name": product["name"],
            "product_type": product["type"],
            "premium_amount": premium,
            "sum_assured": sum_assured,
            "due_date": due_date,
            "payment_history": generate_payment_history(tenure),
            "status": random.choices(["active", "lapsed"], weights=[95, 5])[0],
        }

        if product["type"] == "ulip":
            policy["fund_value"] = premium * tenure * random.uniform(1.05, 1.8)
            policy["nav_change_pct"] = round(random.uniform(5, 18), 1)
        if product["type"] in ["endowment", "child"]:
            maturity_years = random.randint(tenure + 1, tenure + 15)
            maturity = base_date + timedelta(days=maturity_years * 365)
            policy["maturity_date"] = maturity.strftime("%Y-%m-%d")
            policy["projected_maturity_value"] = round(premium * maturity_years * 1.6 / 1000) * 1000

        policies.append(policy)

    # Fixed policies for named customers
    policies[0] = {
        "policy_id": "SLI-2298741",
        "customer_id": "CUST-00001",
        "product_name": "Suraksha Term Shield",
        "product_type": "term",
        "premium_amount": 24000,
        "sum_assured": 10000000,
        "due_date": "2026-03-15",
        "payment_history": [{"year": i, "status": "on_time"} for i in range(1, 6)],
        "status": "active"
    }
    policies[1] = {
        "policy_id": "SLI-882341",
        "customer_id": "CUST-00002",
        "product_name": "Suraksha Endowment Plus",
        "product_type": "endowment",
        "premium_amount": 18000,
        "sum_assured": 500000,
        "due_date": "2026-03-25",
        "payment_history": [{"year": i, "status": "on_time"} for i in range(1, 9)],
        "status": "active",
        "maturity_date": "2036-03-25",
        "projected_maturity_value": 540000
    }
    policies[2] = {
        "policy_id": "SLI-445521",
        "customer_id": "CUST-00003",
        "product_name": "Suraksha Wealth Builder ULIP",
        "product_type": "ulip",
        "premium_amount": 120000,
        "sum_assured": 1500000,
        "due_date": "2026-03-10",
        "payment_history": [{"year": i, "status": "on_time"} for i in range(1, 4)],
        "status": "active",
        "fund_value": 458000,
        "nav_change_pct": 14.0
    }
    return policies


def generate_propensity(policies, customers_map):
    scores = []
    for policy in policies:
        cust = customers_map.get(policy["customer_id"], {})
        hist = policy.get("payment_history", [])
        missed = sum(1 for h in hist if h["status"] in ["missed", "late_7_days"])
        complaints = cust.get("complaint_count", 0)
        tenure = cust.get("tenure_years", 1)

        score = 30 + (missed * 12) + (complaints * 8) - (tenure * 1.5)
        score = max(5, min(95, int(score + random.randint(-10, 10))))

        risk = "LOW" if score < 40 else ("MEDIUM" if score < 65 else "HIGH")
        factors = []
        if missed > 0:
            factors.append(f"{missed} late/missed payments")
        if complaints > 0:
            factors.append(f"{complaints} prior complaints")
        if tenure < 3:
            factors.append("Short tenure")
        if score > 65:
            factors.append("High lapse risk profile")

        scores.append({
            "policy_id": policy["policy_id"],
            "propensity_score": score,
            "risk_level": risk,
            "factors": factors or ["No significant risk factors"]
        })
    return scores


def generate_objections():
    objections = [
        # Financial hardship
        {"id": f"OBJ-{i:03d}", "objection": text, "category": cat, "response": resp, "effectiveness_score": eff}
        for i, (text, cat, resp, eff) in enumerate([
            ("I can't afford the premium right now", "financial_hardship",
             "I completely understand. Suraksha offers a 30-day grace period at no extra charge. You can also opt for our ECS AutoPay which spreads the payment automatically. Shall I set that up for you?", 8.5),
            ("Paise nahi hain abhi", "financial_hardship",
             "Main samajh sakta hoon. Suraksha mein 30 din ki grace period hai bilkul free. Aap ECS AutoPay bhi setup kar sakte hain. Kya main aapke liye yeh arrange kar sakta hoon?", 8.7),
            ("Money is very tight this month", "financial_hardship",
             "I understand completely. We have a premium holiday option for up to 3 months for customers in financial difficulty. Your cover continues during this time. Would you like me to explore this for you?", 9.0),
            ("I lost my job recently", "financial_hardship",
             "I'm sorry to hear that. During difficult times, the last thing you want is to lose your life cover. Suraksha has a Premium Holiday scheme for up to 6 months where your policy stays active. Let me connect you with our specialist who can help.", 9.2),
            ("Bahut mehenga hai", "financial_hardship",
             "Main samajhta hoon. Kya aap jaante hain ki aap sirf ₹2,000 per maah mein apni ₹1 Crore ki protection jari rakh sakte hain? Aur agar kabhi zaroorat pade, hum 30 din ki grace period dete hain.", 8.3),
            ("Can't pay full amount at once", "payment_flexibility",
             "No problem at all! We accept UPI, Net Banking, and Credit/Debit cards. For premiums above ₹50,000, we also offer quarterly payment options. Would any of these work for you?", 8.0),
            ("Can I pay in EMIs?", "payment_flexibility",
             "Absolutely! For annual premiums, we can split into 2 or 4 instalments. For ULIPs above ₹1 Lakh, we also offer monthly SIP-style payments. Which option would you prefer?", 8.8),
            ("Can I pay monthly instead of yearly?", "payment_flexibility",
             "Yes! We offer monthly, quarterly, and half-yearly payment modes. There is a small frequency loading of 2-3%, but many customers find it much more manageable. Shall I switch your payment mode?", 8.5),
            ("Do you accept UPI?", "payment_flexibility",
             "Yes, we accept all UPI apps - GPay, PhonePe, Paytm, BHIM and more. Here's your direct payment link: [PAYMENT_LINK]. It also has a UPI QR code you can scan.", 9.0),
            ("I want to pay through my agent", "payment_flexibility",
             "Of course! Your agent can accept the payment and we'll process it. However, the fastest way is our digital payment link - it reflects in your policy within 2 hours versus 2-3 days through the branch. The choice is yours!", 7.8),
            ("Is this policy worth it?", "value_doubt",
             "Let me share your policy's value: Your ₹[PREMIUM] premium provides ₹[SUM_ASSURED] life cover for your family. That's [MULTIPLIER]x protection. Plus you've already paid ₹[TOTAL_PAID] building significant policy value. Surrendering now means losing all of that.", 8.9),
            ("Returns are very low", "value_doubt",
             "I understand your concern. Pure term insurance is protection, not investment - that's intentional. Your ₹[PREMIUM]/year buys ₹[SUM_ASSURED] protection - that's a [MULTIPLIER]x cover. For investment returns, our ULIP plans combine both.", 8.2),
            ("I'm not getting any benefit", "value_doubt",
             "The benefit of term insurance is the certainty that your family receives ₹[SUM_ASSURED] if something happens to you. It's like car insurance - you don't want to use it, but you'll be grateful it exists when needed.", 7.9),
            ("I want to surrender my policy", "surrender_cancel",
             "I understand. Before we process the surrender, let me share the surrender value: ₹[SURRENDER_VALUE]. If you surrender now you'll receive this amount, but you'll lose ₹[SUM_ASSURED] of life cover. Would you be open to a premium holiday instead, keeping your cover active?", 9.1),
            ("Cancel my policy", "surrender_cancel",
             "I can process that for you. However, after [TENURE] years you've built up significant policy value. May I ask what's driving the decision? Often we can find a solution - premium holiday, reduced cover, or a payment plan that keeps your family protected.", 8.7),
            ("I don't need insurance anymore", "surrender_cancel",
             "I respect your decision. May I just confirm - you have dependents (family members who rely on your income)? If yes, the risk of not having cover can be significant. Would you like to speak with our specialist who can review if any alternatives work for you?", 8.0),
            ("I got a better offer from HDFC Life", "competitor",
             "That's great that you're comparing! Could I ask - is the premium similar or lower? Sometimes lower premiums mean lower cover or stricter claim conditions. Your current Suraksha policy has [CLAIM_SETTLEMENT_RATE]% claim settlement rate. Are you comfortable sharing the competing offer details?", 8.3),
            ("LIC gives more bonus", "competitor",
             "LIC is a great insurer. Their traditional plans do offer bonuses, but they're typically lower sum assured. Your Suraksha plan gives ₹[SUM_ASSURED] guaranteed cover. For a fair comparison, what sum assured is LIC offering at that premium?", 7.8),
            ("How do I pay?", "process",
             "It's very simple! Click this payment link: [PAYMENT_LINK]. You can pay via UPI, Net Banking, Credit/Debit card, or scan the QR code. Payment reflects instantly and you'll get a WhatsApp confirmation.", 9.2),
            ("Where is my payment link?", "process",
             "Here it is! [PAYMENT_LINK] - This link is valid for 30 days and works for UPI, Net Banking, and all cards. It's secured with 256-bit encryption. Let me know if you face any issues.", 9.5),
            ("I already paid through my agent", "process",
             "Thank you for the payment! It may take 24-48 hours to reflect if paid through the branch. To confirm, can you share the receipt or transaction reference? I'll update your policy immediately.", 8.8),
            ("Payment link not working", "technical",
             "I'm sorry for the inconvenience! Let me generate a fresh payment link for you right now: [NEW_PAYMENT_LINK]. If this doesn't work either, please try: 1) Clear browser cache, 2) Try a different browser, 3) Call our helpline 1800-XXX-XXXX.", 8.5),
            ("I didn't get the email", "technical",
             "I apologize for that! Let me resend it to [EMAIL] right now. Please also check your Spam folder. Alternatively, here's your direct payment link on WhatsApp: [PAYMENT_LINK]", 9.0),
            ("Is this a scam?", "trust",
             "Completely understandable to verify! I am the AI-powered renewal assistant of Suraksha Life Insurance, regulated by IRDAI (Registration No: [IRDAI_REG]). You can verify by calling our official helpline 1800-XXX-XXXX or visiting suraksha-life.com. Your policy no. [POLICY_ID] is valid and active.", 9.3),
            ("Are you a robot?", "trust",
             "Yes, I am Suraksha's AI-powered renewal assistant! I handle routine renewal queries 24/7. If you'd prefer to speak with a human specialist, just say 'talk to a person' and I'll connect you immediately. Many customers find it faster and convenient to renew directly with me though!", 8.9),
            ("I want to talk to a real person", "trust",
             "Absolutely! I'll connect you with a Renewal Relationship Manager right away. They have your full policy history and will call you within 2 hours at [PREFERRED_TIME]. Is [PHONE] the best number to reach you?", 9.5),
            ("What is my sum assured?", "product_query",
             "Your sum assured is ₹[SUM_ASSURED]. This is the guaranteed amount your family will receive in case of any eventuality. Your policy [POLICY_ID] ([PRODUCT_NAME]) has been protecting your family since [START_DATE].", 9.0),
            ("When does my policy mature?", "product_query",
             "Your [PRODUCT_NAME] policy (No. [POLICY_ID]) matures on [MATURITY_DATE]. At maturity, you'll receive ₹[MATURITY_VALUE] (projected). To ensure you receive the full maturity benefit, your premium due on [DUE_DATE] must be paid.", 9.1),
            ("What's my fund value?", "product_query",
             "Your Suraksha Wealth Builder ULIP current fund value is ₹[FUND_VALUE] as of today. Your NAV has grown [NAV_CHANGE]% this year. Continuing the policy ensures your fund keeps growing tax-efficiently under Section 10(10D).", 8.8),
            ("How do I file a claim?", "claims",
             "For life insurance claims: 1) Call 1800-XXX-XXXX (24/7) 2) Email claims@suraksha-life.com 3) Visit any Suraksha branch with: Death certificate, Policy document, ID proof of nominee. Claims are settled within 30 days of complete documentation.", 9.0),
            ("What is the death benefit?", "claims",
             "The death benefit for your [PRODUCT_NAME] policy is ₹[SUM_ASSURED]. This is paid to your nominee [NOMINEE_NAME] as a lump sum, tax-free under Section 10(10D). Have you updated your nominee details recently?", 9.2),
            ("What happens if I don't pay?", "surrender_cancel",
             "If the premium is not paid by the due date, there's a 30-day grace period where your cover continues. After that, the policy lapses. Revival is possible within 2 years with a small fee. To avoid this, shall I set up AutoPay?", 8.8),
            ("Mujhe nahi chahiye yeh policy", "surrender_cancel",
             "Main samajhta hoon. Lekin [TENURE] saalon ki hard-earned savings aur ₹[SUM_ASSURED] ki protection kho jaayegi. Kya aap mujhe bata sakte hain kyun aap band karna chahte hain? Shayad hum koi solution nikal sakein.", 8.5),
            ("Iska koi fayda nahi", "value_doubt",
             "Main samajhta hoon aapki baat. Yeh policy aapke parivaar ko ₹[SUM_ASSURED] ki suraksha deti hai. Jaise ghar ka taala - aap chahte hain ki kabhi kaam na aaye, lekin hota hai toh bahut bada sahara milta hai.", 8.0),
            ("Is this IRDAI approved?", "trust",
             "Yes, absolutely. Suraksha Life Insurance is registered with IRDAI (Insurance Regulatory and Development Authority of India) under registration number [IRDAI_REG]. All our products are IRDAI approved. You can verify at irdai.gov.in.", 9.4),
        ], 1)
    ]
    return objections


def generate_compliance_rules():
    return [
        {"rule_id": f"CR-{i:03d}", "rule": rule, "category": cat, "severity": sev, "check_type": check}
        for i, (rule, cat, sev, check) in enumerate([
            ("AI must self-identify as AI in every communication", "disclosure", "high", "regex"),
            ("Opt-out mechanism must be present in every communication", "disclosure", "high", "keyword"),
            ("No guaranteed return promises for ULIPs", "product_accuracy", "critical", "regex"),
            ("No pressure language ('must pay today or lose everything')", "ethics", "high", "keyword"),
            ("DND check required before voice calls", "regulatory", "high", "api_check"),
            ("PII must not appear in AI inference prompts", "privacy", "critical", "pii_scan"),
            ("All communications in customer preferred language", "language", "medium", "language_check"),
            ("Grace period must be accurately stated as 30 days", "product_accuracy", "high", "factual"),
            ("Premium holiday eligibility criteria must be stated correctly", "product_accuracy", "medium", "factual"),
            ("Revival terms must be accurate (2 years, with late fees)", "product_accuracy", "high", "factual"),
            ("Cannot promise specific investment returns", "product_accuracy", "critical", "regex"),
            ("Must mention IRDAI grievance redressal in formal communications", "disclosure", "medium", "keyword"),
            ("Policy number must be mentioned in all renewal communications", "disclosure", "high", "keyword"),
            ("Premium amount must exactly match policy records", "product_accuracy", "critical", "factual"),
            ("Sum assured must exactly match policy records", "product_accuracy", "critical", "factual"),
            ("No calls between 9 PM and 9 AM", "regulatory", "high", "time_check"),
            ("Maximum 3 contact attempts per channel per week", "regulatory", "medium", "frequency_check"),
            ("Nominee information must not be shared without verification", "privacy", "high", "access_control"),
            ("Bank account details must never appear in any communication", "privacy", "critical", "pii_scan"),
            ("Aadhaar number must be masked if detected", "privacy", "critical", "pii_scan"),
        ], 1)
    ]


def generate_distress_keywords():
    return {
        "English": {
            "bereavement": ["husband passed away", "wife passed away", "death in family", "funeral", "lost my spouse", "my husband died", "my wife died", "bereaved", "mourning", "passed away", "deceased"],
            "financial_hardship": ["can't afford", "lost my job", "no money", "financially struggling", "bankrupt", "unemployed", "salary cut", "pay cut", "going through tough times", "money problems"],
            "medical": ["hospitalized", "cancer", "surgery", "critical illness", "ICU", "heart attack", "stroke", "seriously ill", "terminal", "diagnosed with"],
            "legal": ["consumer court", "ombudsman", "lawyer", "legal notice", "going to sue", "complaint to IRDAI", "cheating", "fraud", "mis-sold"]
        },
        "Hindi": {
            "bereavement": ["pati guzar gaye", "patni guzar gayi", "maut ho gayi", "mrityu ho gayi", "chale gaye", "nahi rahe", "swarg sidhaar gaye", "beraham maut", "dukh ki ghadi"],
            "financial_hardship": ["paise nahi hain", "naukri chali gayi", "kaafi takleef mein hoon", "badi pareshani hai", "ghar chalaana mushkil hai", "karza chadh gaya hai"],
            "medical": ["hospital mein hoon", "beemar hoon", "operation hua", "operation hoga", "gambhir bimari", "ICU mein"],
            "legal": ["consumer forum", "lokpal", "vakeel", "court mein jaaunga", "IRDAI complaint", "dhoka hua", "dhokha diya"]
        },
        "Marathi": {
            "bereavement": ["pati gevale", "patni gevali", "mrityu zali", "varle", "gele", "nighun gele"],
            "financial_hardship": ["paisa nahi", "naukri geli", "khup kathin ahe", "aarthik samasyaa"],
            "medical": ["hospital madhye ahe", "ajar aahe", "operation ahe"],
            "legal": ["court madhye jato", "takrar karnar", "IRDAI la takrar"]
        },
        "Tamil": {
            "bereavement": ["kanavar poitta", "manaivi poitta", "ilanthu vittaar", "maranam"],
            "financial_hardship": ["panam illa", "velai poguchchu", "kattinam"],
            "medical": ["hospital-il irukkiren", "noi", "surgery"],
            "legal": ["court pokiren", "pukaaru seiven", "IRDAI pukaaru"]
        },
        "Telugu": {
            "bereavement": ["bharthu poyaru", "bharya poyindi", "chanipoyyaru", "maranam"],
            "financial_hardship": ["dabbu ledu", "job poyindi", "kastam"],
            "medical": ["hospital lo unnanu", "operation", "vyadhi"],
            "legal": ["court ki veltanu", "complaint chestanu"]
        },
        "Kannada": {
            "bereavement": ["ganda hogidare", "hendathi hogidare", "nidhanavagidare"],
            "financial_hardship": ["hana illa", "kaleji hogide", "tumba kashtа"],
            "medical": ["hospital li iddene", "vyadhi", "operation"],
            "legal": ["court ge hoguttene", "complaint maduttene"]
        },
        "Malayalam": {
            "bereavement": ["bharthav poyi", "bhaarya poyi", "marichupoyi", "marichu"],
            "financial_hardship": ["panam illa", "job poyi", "valiyan budhimuttu"],
            "medical": ["hospital il aanu", "ariyam", "operation"],
            "legal": ["court il pokum", "paruthi parayum"]
        },
        "Bengali": {
            "bereavement": ["sami chale gache", "stri chale geche", "mara gache", "mrittyu hoye gache"],
            "financial_hardship": ["taka nei", "chakri giyeche", "khub kosto"],
            "medical": ["hospital-e achi", "opur", "operation"],
            "legal": ["court-e jabo", "complaint korbo", "IRDAI complaint"]
        },
        "Gujarati": {
            "bereavement": ["pati gaya", "patni gayi", "gujri gaya", "mrittyu"],
            "financial_hardship": ["paisa nathi", "nokri gayi", "ghanu kashat"],
            "medical": ["hospital ma chhu", "bimari", "operation"],
            "legal": ["court ma javanu", "complaint karish"]
        }
    }


def generate_team_members():
    return [
        # Senior RRMs
        {"employee_id": "EMP-001", "name": "Priya Sharma", "role": "senior_rrm", "specialization": "bereavement", "email": "priya.sharma@suraksha-life.com", "cases_this_week": 8, "avg_resolution_hours": 1.8, "customer_rating": 4.9},
        {"employee_id": "EMP-002", "name": "Arjun Mehta", "role": "senior_rrm", "specialization": "hni", "email": "arjun.mehta@suraksha-life.com", "cases_this_week": 6, "avg_resolution_hours": 2.2, "customer_rating": 4.8},
        {"employee_id": "EMP-003", "name": "Kavitha Nair", "role": "senior_rrm", "specialization": "high_value", "email": "kavitha.nair@suraksha-life.com", "cases_this_week": 9, "avg_resolution_hours": 1.9, "customer_rating": 4.7},
        {"employee_id": "EMP-004", "name": "Suresh Patil", "role": "senior_rrm", "specialization": "high_value", "email": "suresh.patil@suraksha-life.com", "cases_this_week": 7, "avg_resolution_hours": 2.5, "customer_rating": 4.6},
        {"employee_id": "EMP-005", "name": "Deepa Krishnan", "role": "senior_rrm", "specialization": "bereavement", "email": "deepa.krishnan@suraksha-life.com", "cases_this_week": 5, "avg_resolution_hours": 1.6, "customer_rating": 4.9},
        {"employee_id": "EMP-006", "name": "Ravi Desai", "role": "senior_rrm", "specialization": "hni", "email": "ravi.desai@suraksha-life.com", "cases_this_week": 4, "avg_resolution_hours": 2.8, "customer_rating": 4.5},
        {"employee_id": "EMP-007", "name": "Anitha Reddy", "role": "senior_rrm", "specialization": "high_value", "email": "anitha.reddy@suraksha-life.com", "cases_this_week": 11, "avg_resolution_hours": 1.7, "customer_rating": 4.8},
        {"employee_id": "EMP-008", "name": "Mohan Singh", "role": "senior_rrm", "specialization": "high_value", "email": "mohan.singh@suraksha-life.com", "cases_this_week": 6, "avg_resolution_hours": 2.3, "customer_rating": 4.7},
        # Revival Specialists
        {"employee_id": "EMP-009", "name": "Rahul Deshmukh", "role": "revival_specialist", "specialization": "medical_underwriting", "email": "rahul.deshmukh@suraksha-life.com", "cases_this_week": 12, "avg_resolution_hours": 4.2, "customer_rating": 4.6},
        {"employee_id": "EMP-010", "name": "Sunita Joshi", "role": "revival_specialist", "specialization": "payment_plans", "email": "sunita.joshi@suraksha-life.com", "cases_this_week": 10, "avg_resolution_hours": 3.8, "customer_rating": 4.7},
        {"employee_id": "EMP-011", "name": "Anil Kumar", "role": "revival_specialist", "specialization": "waiver_negotiation", "email": "anil.kumar@suraksha-life.com", "cases_this_week": 8, "avg_resolution_hours": 4.5, "customer_rating": 4.5},
        {"employee_id": "EMP-012", "name": "Latha Venkatesh", "role": "revival_specialist", "specialization": "medical_underwriting", "email": "latha.venkatesh@suraksha-life.com", "cases_this_week": 9, "avg_resolution_hours": 3.9, "customer_rating": 4.8},
        {"employee_id": "EMP-013", "name": "Ganesh Iyer", "role": "revival_specialist", "specialization": "payment_plans", "email": "ganesh.iyer@suraksha-life.com", "cases_this_week": 7, "avg_resolution_hours": 4.1, "customer_rating": 4.6},
        # Compliance Handlers
        {"employee_id": "EMP-014", "name": "Meera Bose", "role": "compliance_handler", "specialization": "irdai_complaints", "email": "meera.bose@suraksha-life.com", "cases_this_week": 2, "avg_resolution_hours": 12.0, "customer_rating": 4.5},
        {"employee_id": "EMP-015", "name": "Sanjay Gupta", "role": "compliance_handler", "specialization": "mis_selling", "email": "sanjay.gupta@suraksha-life.com", "cases_this_week": 3, "avg_resolution_hours": 10.5, "customer_rating": 4.4},
        # AI Ops Managers
        {"employee_id": "EMP-016", "name": "Rohan Jain", "role": "ai_ops_manager", "specialization": "model_tuning", "email": "rohan.jain@suraksha-life.com", "cases_this_week": 0, "avg_resolution_hours": 0, "customer_rating": 0},
        {"employee_id": "EMP-017", "name": "Sneha Kapoor", "role": "ai_ops_manager", "specialization": "quality_evaluation", "email": "sneha.kapoor@suraksha-life.com", "cases_this_week": 0, "avg_resolution_hours": 0, "customer_rating": 0},
        {"employee_id": "EMP-018", "name": "Nikhil Verma", "role": "ai_ops_manager", "specialization": "guardrails", "email": "nikhil.verma@suraksha-life.com", "cases_this_week": 0, "avg_resolution_hours": 0, "customer_rating": 0},
        # Renewal Head
        {"employee_id": "EMP-019", "name": "Vikram Bhatia", "role": "renewal_head", "specialization": "strategy", "email": "vikram.bhatia@suraksha-life.com", "cases_this_week": 0, "avg_resolution_hours": 0, "customer_rating": 0},
        # AI Trainer
        {"employee_id": "EMP-020", "name": "Prachi Dhawan", "role": "ai_trainer", "specialization": "prompt_engineering", "email": "prachi.dhawan@suraksha-life.com", "cases_this_week": 0, "avg_resolution_hours": 0, "customer_rating": 0},
    ]


def generate_preseeded_journeys(policies):
    """Generate 50 completed, 20 in-progress, 8 escalated, 5 lapsed journeys."""
    journeys = []
    now = datetime.now()

    policy_ids = [p["policy_id"] for p in policies[3:]]  # Skip first 3 named customers
    random.shuffle(policy_ids)

    statuses_pool = (
        [("paid", "completed")] * 50 +
        [("whatsapp_sent", "in_progress")] * 8 +
        [("email_sent", "in_progress")] * 7 +
        [("voice_called", "in_progress")] * 5 +
        [("lapsed", "lapsed")] * 5
    )

    for i, pid in enumerate(policy_ids[:75]):
        if i >= len(statuses_pool):
            break
        status_pair = statuses_pool[i]
        status = status_pair[0]
        delta_days = random.randint(1, 30)
        started = (now - timedelta(days=delta_days)).isoformat()
        updated = (now - timedelta(hours=random.randint(1, 24))).isoformat()

        j = {
            "policy_id": pid,
            "customer_id": f"CUST-{random.randint(10, 500):05d}",
            "status": status,
            "current_step": status,
            "steps": [
                {"step": "t45_email", "agent": "email_agent", "channel": "email", "status": "completed",
                 "timestamp": (now - timedelta(days=delta_days - 1)).isoformat(), "message_preview": "Your policy is up for renewal...", "critique_score": round(random.uniform(7.5, 9.5), 1), "verdict": "APPROVED"},
            ],
            "conversation_history": [],
            "escalation_reason": None,
            "started_at": started,
            "updated_at": updated,
            "paid_at": updated if status == "paid" else None,
            "payment_amount": random.choice([12000, 18000, 24000, 36000, 48000]) if status == "paid" else None,
            "attempt_count": 1,
            "trace_id": str(uuid.uuid4())
        }
        journeys.append(j)

    return journeys


def generate_preseeded_queue():
    cases = [
        {
            "case_id": "CASE-00001",
            "policy_id": "SLI-334521",
            "customer_id": "CUST-00050",
            "priority": "urgent",
            "status": "open",
            "escalation_reason": "distress_detected",
            "escalation_detail": "Customer mentioned bereavement: 'My father passed away last week. I cannot think about policy right now.'",
            "assigned_to": None,
            "sla_hours": 2,
            "escalated_at": (datetime.now() - timedelta(hours=1)).isoformat(),
            "conversation_history": [
                {"role": "ai", "content": "Hi! Your Suraksha Term Shield policy is due for renewal on March 20. Tap here to renew.", "timestamp": (datetime.now() - timedelta(hours=1, minutes=5)).isoformat(), "channel": "whatsapp"},
                {"role": "customer", "content": "My father passed away last week. I cannot think about policy right now.", "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(), "channel": "whatsapp"},
            ],
            "briefing_note": "**URGENT - BEREAVEMENT CASE**\n\nCustomer Ramesh Gupta (CUST-00050) is going through bereavement. His father passed away last week.\n\n**Recommended Approach:**\n- Lead with condolence, NOT renewal\n- Offer 3-month premium holiday immediately\n- Check if father was nominee - may need claim assistance\n- Do NOT mention payment or due dates in first call\n\n**Policy:** Suraksha Term Shield | Premium: ₹18,000 | Tenure: 7 years | Zero lapses",
            "recommended_approach": "Call immediately. Open with condolences. Offer premium holiday. Ask about nominee status.",
            "detected_sentiment": "distress_bereavement"
        },
        {
            "case_id": "CASE-00002",
            "policy_id": "SLI-667891",
            "customer_id": "CUST-00120",
            "priority": "standard",
            "status": "open",
            "escalation_reason": "critique_failure",
            "escalation_detail": "Planner Critique rejected after 3 retries. Customer segment mismatch detected in all plans.",
            "assigned_to": None,
            "sla_hours": 24,
            "escalated_at": (datetime.now() - timedelta(hours=3)).isoformat(),
            "conversation_history": [],
            "briefing_note": "**CRITIQUE FAILURE - MANUAL PLAN REQUIRED**\n\nThe AI planning agent failed to generate an approved renewal plan for this customer after 3 attempts. The critique agent flagged segment mismatch.\n\n**Reason:** Customer profile shows HNI segment (ULIP ₹2,50,000 premium) but CRM data shows budget_conscious tag - likely data error.\n\n**Action Required:** Manually contact customer with HNI-appropriate approach. Suggest wealth management review alongside renewal.",
            "recommended_approach": "Use HNI approach. Focus on fund performance and portfolio review. Do not use standard budget-conscious messaging.",
            "detected_sentiment": "neutral"
        },
        {
            "case_id": "CASE-00003",
            "policy_id": "SLI-221456",
            "customer_id": "CUST-00085",
            "priority": "urgent",
            "status": "assigned",
            "escalation_reason": "distress_detected",
            "escalation_detail": "Customer mentioned medical emergency: 'I am in the hospital. I had a heart attack.'",
            "assigned_to": "EMP-001",
            "assigned_at": (datetime.now() - timedelta(minutes=45)).isoformat(),
            "sla_hours": 2,
            "escalated_at": (datetime.now() - timedelta(hours=1, minutes=30)).isoformat(),
            "conversation_history": [
                {"role": "ai", "content": "Namaste! Aapki Suraksha policy ka renewal due hai. Payment ke liye yahan tap karein.", "timestamp": (datetime.now() - timedelta(hours=1, minutes=35)).isoformat(), "channel": "whatsapp"},
                {"role": "customer", "content": "Main hospital mein hoon. Mujhe heart attack aaya hai. Baad mein baat karna.", "timestamp": (datetime.now() - timedelta(hours=1, minutes=30)).isoformat(), "channel": "whatsapp"},
            ],
            "briefing_note": "**URGENT - MEDICAL EMERGENCY**\n\nCustomer is hospitalized with a heart attack. DO NOT discuss renewal.\n\n**Immediate Actions:**\n1. Express concern for health\n2. Inform about 30-day grace period - no action needed right now\n3. Check if hospitalisation is covered under any rider\n4. Note for follow-up once customer recovers\n\n**Policy:** Suraksha Endowment Plus | ₹22,000 premium | 6 years tenure",
            "recommended_approach": "Health first. Renewal can wait 30 days. Check rider coverage for hospitalization.",
            "detected_sentiment": "distress_medical"
        },
        {
            "case_id": "CASE-00004",
            "policy_id": "SLI-559012",
            "customer_id": "CUST-00200",
            "priority": "standard",
            "status": "open",
            "escalation_reason": "human_requested",
            "escalation_detail": "Customer explicitly requested human agent after 3 WhatsApp exchanges.",
            "assigned_to": None,
            "sla_hours": 24,
            "escalated_at": (datetime.now() - timedelta(hours=5)).isoformat(),
            "conversation_history": [
                {"role": "ai", "content": "Hi Anita! Your Suraksha Child Future Plan is due for renewal on March 18.", "timestamp": (datetime.now() - timedelta(hours=5, minutes=15)).isoformat(), "channel": "whatsapp"},
                {"role": "customer", "content": "I have questions about the maturity benefits. Can you explain?", "timestamp": (datetime.now() - timedelta(hours=5, minutes=10)).isoformat(), "channel": "whatsapp"},
                {"role": "ai", "content": "Your Child Future Plan matures in 2035 with a projected value of ₹4,80,000...", "timestamp": (datetime.now() - timedelta(hours=5, minutes=8)).isoformat(), "channel": "whatsapp"},
                {"role": "customer", "content": "I want to talk to a real person please. I have more complex questions.", "timestamp": (datetime.now() - timedelta(hours=5)).isoformat(), "channel": "whatsapp"},
            ],
            "briefing_note": "**HUMAN REQUESTED**\n\nCustomer Anita Sharma has complex questions about maturity benefits of her Child Future Plan. She is not satisfied with AI explanations.\n\n**Background:** Policy has 12 years remaining. Premium ₹15,000/year. Customer is likely planning education funding.\n\n**Recommended Approach:** Walk through the maturity benefit schedule year by year. Discuss Suraksha's Education Benefit rider option. Customer seems financially literate.",
            "recommended_approach": "Detailed product walkthrough. Focus on education planning angle. Suggest Education Benefit rider.",
            "detected_sentiment": "neutral_curious"
        },
        {
            "case_id": "CASE-00005",
            "policy_id": "SLI-778234",
            "customer_id": "CUST-00310",
            "priority": "compliance",
            "status": "open",
            "escalation_reason": "compliance_flag",
            "escalation_detail": "AI response flagged for potential mis-selling: response contained phrase suggesting 'guaranteed 14% returns' for ULIP product.",
            "assigned_to": "EMP-014",
            "assigned_at": (datetime.now() - timedelta(hours=2)).isoformat(),
            "sla_hours": 4,
            "escalated_at": (datetime.now() - timedelta(hours=2, minutes=30)).isoformat(),
            "conversation_history": [],
            "briefing_note": "**COMPLIANCE ALERT - POTENTIAL MIS-SELLING**\n\nAI draft response for ULIP renewal was flagged by the Safety Gate for containing language that could be interpreted as guaranteeing investment returns.\n\n**Flagged phrase:** 'your fund has grown 14% and we expect similar returns'\n\n**Regulatory concern:** IRDAI prohibits guaranteeing ULIP returns. This was caught BEFORE delivery (no customer harm).\n\n**Action:** Review the draft, amend to correct language, and document this catch for the monthly IRDAI report.",
            "recommended_approach": "Draft correction: 'Your fund has grown 14% in the past year. Past performance is not indicative of future returns.'",
            "detected_sentiment": "neutral"
        },
        {
            "case_id": "CASE-00006",
            "policy_id": "SLI-901234",
            "customer_id": "CUST-00400",
            "priority": "standard",
            "status": "open",
            "escalation_reason": "critique_failure",
            "escalation_detail": "Voice Agent Critique failed 3 times. Script for regional language (Kannada) customer rated below 7.0 on language quality.",
            "assigned_to": None,
            "sla_hours": 24,
            "escalated_at": (datetime.now() - timedelta(hours=8)).isoformat(),
            "conversation_history": [],
            "briefing_note": "**LANGUAGE QUALITY FAILURE**\n\nThe Voice Agent could not generate a Kannada-language script that passed quality review after 3 attempts.\n\n**Reason:** Customer's profile shows preference for Havyaka Kannada dialect, but the AI was generating standard Kannada.\n\n**Action:** Call this customer in standard Kannada or switch to English (customer also speaks English). Note the dialect gap in the system for the AI trainer.",
            "recommended_approach": "Call in English or standard Kannada. Customer also speaks English well. Note dialect preference for model improvement.",
            "detected_sentiment": "neutral"
        },
        {
            "case_id": "CASE-00007",
            "policy_id": "SLI-112345",
            "customer_id": "CUST-00450",
            "priority": "urgent",
            "status": "open",
            "escalation_reason": "distress_detected",
            "escalation_detail": "Customer mentioned financial hardship: 'Meri naukri chali gayi hai. Ghar chalaana mushkil ho gaya hai.'",
            "assigned_to": None,
            "sla_hours": 2,
            "escalated_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "conversation_history": [
                {"role": "ai", "content": "Namaste Ramesh-ji! Aapki Suraksha Term Shield policy ka renewal 22 March ko due hai.", "timestamp": (datetime.now() - timedelta(minutes=35)).isoformat(), "channel": "whatsapp"},
                {"role": "customer", "content": "Meri naukri chali gayi hai. Ghar chalaana mushkil ho gaya hai. Policy band karna padega.", "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(), "channel": "whatsapp"},
            ],
            "briefing_note": "**URGENT - JOB LOSS / FINANCIAL HARDSHIP**\n\nCustomer has lost their job and is facing financial difficulty. At risk of lapsing.\n\n**Immediate Options to Offer:**\n1. Premium Holiday (3-6 months) - policy stays active\n2. Reduced paid-up value option\n3. Auto-pay with delayed start\n4. Grace period (30 days from due date)\n\n**IMPORTANT:** Do not discuss payment at start. Acknowledge the difficulty first.",
            "recommended_approach": "Empathy first. Lead with Premium Holiday option. Do not pressure for payment.",
            "detected_sentiment": "distress_financial"
        },
        {
            "case_id": "CASE-00008",
            "policy_id": "SLI-567890",
            "customer_id": "CUST-00480",
            "priority": "standard",
            "status": "on_hold",
            "escalation_reason": "human_requested",
            "escalation_detail": "Customer requested agent to discuss surrender value calculation.",
            "assigned_to": "EMP-003",
            "assigned_at": (datetime.now() - timedelta(hours=4)).isoformat(),
            "sla_hours": 24,
            "escalated_at": (datetime.now() - timedelta(hours=6)).isoformat(),
            "conversation_history": [],
            "briefing_note": "**SURRENDER INQUIRY**\n\nCustomer wants to discuss surrender value. 10-year endowment policy. Premium ₹30,000/year. Customer has been with Suraksha 10 years.\n\n**Context:** Surrender value now would be approx ₹2,40,000 vs projected maturity of ₹5,20,000 in 5 years.\n\n**Goal:** Convince customer to hold for 5 more years. Show the gap clearly. Offer premium holiday if cash needed.",
            "recommended_approach": "Show maturity vs surrender gap. Offer premium holiday for 6 months as alternative. Do not let a 10-year customer surrender.",
            "detected_sentiment": "considering_surrender"
        }
    ]
    return cases


def generate_preseeded_conversations():
    return [
        {
            "policy_id": "SLI-2298741",
            "messages": []
        },
        {
            "policy_id": "SLI-882341",
            "messages": []
        },
        {
            "policy_id": "SLI-445521",
            "messages": []
        }
    ]


def main():
    print("Generating seed data...")

    customers = generate_customers(500)
    customers_map = {c["customer_id"]: c for c in customers}
    policies = generate_policies(customers)
    propensity = generate_propensity(policies, customers_map)
    objections = generate_objections()
    compliance = generate_compliance_rules()
    distress = generate_distress_keywords()
    team = generate_team_members()
    journeys = generate_preseeded_journeys(policies)
    queue = generate_preseeded_queue()
    conversations = generate_preseeded_conversations()

    files = {
        "customers.json": customers,
        "policies.json": policies,
        "propensity_scores.json": propensity,
        "objection_library.json": objections,
        "compliance_rules.json": compliance,
        "distress_keywords.json": distress,
        "team_members.json": team,
        "preseeded_journeys.json": journeys,
        "preseeded_queue.json": queue,
        "preseeded_conversations.json": conversations,
    }

    for filename, data in files.items():
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Written: {filename} ({len(data) if isinstance(data, list) else 'dict'} items)")

    print("Seed data generation complete!")


if __name__ == "__main__":
    main()
