# RenewAI Full System Architecture v2.0
**Suraksha Life Insurance | 6-Agent System + Critique Agents + Audit DB | GCP Mumbai (asia-south1) | LangGraph + Gemini**

This document outlines the core architecture of the RenewAI system.

## Flowchart Diagram
*Below is the diagram source in Draw.io (mxGraph) XML format. You can copy this XML and paste it directly into [draw.io](https://app.diagrams.net/) (via Arrange -> Insert -> Advanced -> From Text) to render the flowchart visually.*

```xml
<mxGraphModel dx="2377" dy="1238" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="title" parent="1" style="text;html=0;align=center;verticalAlign=middle;fontSize=20;fontStyle=1;strokeColor=none;fillColor=none;" value="PROJECT RenewAI  Full System Architecture v2.0" vertex="1">
      <mxGeometry height="40" width="600" x="500" y="30" as="geometry" />
    </mxCell>
    <mxCell id="subtitle" parent="1" style="text;html=0;align=center;verticalAlign=middle;fontSize=13;fontStyle=0;fontColor=#888888;strokeColor=none;fillColor=none;" value="Suraksha Life Insurance | 6-Agent System + Critique Agents + Audit DB | GCP Mumbai (asia-south1) | LangGraph + Gemini" vertex="1">
      <mxGeometry height="30" width="800" x="400" y="65" as="geometry" />
    </mxCell>
    <mxCell id="subtitle2" parent="1" style="text;html=0;align=center;verticalAlign=middle;fontSize=11;fontStyle=0;fontColor=#888888;strokeColor=none;fillColor=none;" value="Investment: ₹3.78 Cr | Net Year 1: ₹48 Cr | 3-Yr NPV: ₹89 Cr | Payback: 7.8 Months | Persistency: 71%→88% | Team: 123→20 | OpEx: ₹18.6→₹5.7 Cr/yr" vertex="1">
      <mxGeometry height="25" width="900" x="350" y="90" as="geometry" />
    </mxCell>
    <mxCell id="t1" parent="1" style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;fixedSize=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;fontStyle=1;" value="Policy Due Date&#xa;(T-45 Trigger)&#xa;Cloud Scheduler + Cloud Tasks&#xa;~3,900/day | ~5,500 Q4 peak" vertex="1">
      <mxGeometry height="80" width="200" x="340" y="130" as="geometry" />
    </mxCell>
    <mxCell id="t2" parent="1" style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;fixedSize=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;fontStyle=1;" value="Customer Inbound&#xa;Message&#xa;(WhatsApp / Email reply)" vertex="1">
      <mxGeometry height="80" width="200" x="600" y="130" as="geometry" />
    </mxCell>
    <mxCell id="t3" parent="1" style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;fixedSize=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;fontStyle=1;" value="Lapse Event&#xa;(Revival Campaign)&#xa;90-day post-lapse window" vertex="1">
      <mxGeometry height="80" width="200" x="860" y="130" as="geometry" />
    </mxCell>
    <mxCell id="et1" edge="1" parent="1" source="t1" style="rounded=1;strokeColor=#d6b656;strokeWidth=2;entryX=0.35;entryY=0;entryDx=0;entryDy=0;" target="orch">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="et2" edge="1" parent="1" source="t2" style="rounded=1;strokeColor=#d6b656;strokeWidth=2;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="orch">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="et3" edge="1" parent="1" source="t3" style="rounded=1;strokeColor=#d6b656;strokeWidth=2;entryX=0.65;entryY=0;entryDx=0;entryDy=0;" target="orch">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="orch" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;fontStyle=0;align=left;spacingLeft=15;spacingTop=5;strokeWidth=2;" value="ORCHESTRATOR AGENT (LangGraph Graph)&#xa;LLM: Gemini 2.0 Flash (function calling) | Classifier: Gemini 2.5 Pro + Guardrails AI&#xa;&#xa;- Segments renewal case (risk, channel, language, tone)&#xa;- Reads Propensity-to-Lapse scores (Vertex AI AutoML)&#xa;- Runs T-45 branching: T-45 Email → T-30 WA → T-20 Voice → T-10 Last Chance → T-5 Critical → Post-lapse Revival&#xa;- Reviews execution outcomes, decides next step&#xa;- High-complexity flag → Human Queue&#xa;- State checkpoints: Firestore | Each renewal = 1 graph execution" vertex="1">
      <mxGeometry height="170" width="520" x="440" y="260" as="geometry" />
    </mxCell>
    <mxCell id="e_orch_plan" edge="1" parent="1" source="orch" style="rounded=1;strokeColor=#6c8ebf;strokeWidth=2;fontSize=10;fontStyle=0;" target="plan_box" value="Sends objective">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_orch_hq" edge="1" parent="1" source="orch" style="rounded=1;strokeColor=#7B68EE;strokeWidth=2;dashed=1;fontSize=10;" target="hq" value="High complexity / distress">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="1300" y="330" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="plan_box" parent="1" style="rounded=1;fillColor=#f5f5f5;strokeColor=#999999;strokeWidth=2;dashed=1;dashPattern=8 4;" value="" vertex="1">
      <mxGeometry height="280" width="600" x="400" y="500" as="geometry" />
    </mxCell>
    <mxCell id="plan_box_title" parent="1" style="text;html=0;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;strokeColor=none;fillColor=none;" value="PLANNER-CRITIQUE LOOP" vertex="1">
      <mxGeometry height="25" width="300" x="550" y="508" as="geometry" />
    </mxCell>
    <mxCell id="planner" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10;align=left;spacingLeft=10;spacingTop=5;strokeWidth=2;" value="PLANNER AGENT&#xa;LLM: Gemini 2.0 Flash&#xa;&#xa;- Receives objective from Orchestrator&#xa;- Reads CRM + Semantic Memory + Propensity scores&#xa;- Considers communication preferences (41% prefer evening/weekend)&#xa;- Selects language from 9 options (96% coverage)&#xa;- Builds detailed execution plan with channel, timing, tone" vertex="1">
      <mxGeometry height="150" width="260" x="420" y="545" as="geometry" />
    </mxCell>
    <mxCell id="plan_crit" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10;align=left;spacingLeft=10;spacingTop=5;strokeWidth=2;" value="PLANNER CRITIQUE&#xa;LLM: Gemini 2.5 Pro (evaluator) + Guardrails AI&#xa;&#xa;- Validates plan against CRM + Memory&#xa;- Correct channel? Language? Preferred time?&#xa;- Customer segment match? Risk level correct?&#xa;- APPROVED → Execution Agents&#xa;- REJECTED → Back to Planner with feedback" vertex="1">
      <mxGeometry height="150" width="260" x="720" y="545" as="geometry" />
    </mxCell>
    <mxCell id="e_p_c" edge="1" parent="1" source="planner" style="rounded=1;strokeColor=#82b366;strokeWidth=2;fontSize=10;" target="plan_crit" value="Proposed plan">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_c_p" edge="1" parent="1" source="plan_crit" style="rounded=1;strokeColor=#b85450;strokeWidth=2;dashed=1;fontSize=10;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="planner" value="REJECTED + feedback">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="850" y="530" />
          <mxPoint x="550" y="530" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="crm" parent="1" style="shape=cylinder3;whiteSpace=wrap;boundedLbl=1;backgroundOutline=1;size=12;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=10;align=center;strokeWidth=2;" value="CRM (Master Policy Store)&#xa;&#xa;4.8M policyholders&#xa;Policy details + premium history&#xa;Contact info + agent assignments&#xa;Channel + language preference&#xa;Bidirectional sync: Cloud Functions" vertex="1">
      <mxGeometry height="150" width="180" x="80" y="470" as="geometry" />
    </mxCell>
    <mxCell id="mem" parent="1" style="shape=cylinder3;whiteSpace=wrap;boundedLbl=1;backgroundOutline=1;size=12;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=10;align=center;strokeWidth=2;" value="Semantic Memory&#xa;(Firestore + Cloud Vector Search)&#xa;&#xa;Conversation history&#xa;Customer intent + sentiment&#xa;Policy docs (RAG, Gemini Embeddings)&#xa;150-200+ objection-response pairs&#xa;&lt;50ms p99 retrieval (ScaNN)" vertex="1">
      <mxGeometry height="160" width="200" x="70" y="650" as="geometry" />
    </mxCell>
    <mxCell id="redis_cache" parent="1" style="shape=cylinder3;whiteSpace=wrap;boundedLbl=1;backgroundOutline=1;size=12;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=10;align=center;strokeWidth=2;" value="Redis (Memorystore)&#xa;Session Cache&#xa;&#xa;WA session memory (TTL 72h)&#xa;Voice call state&#xa;Payment status (TTL 5min)&#xa;Rate limiting&#xa;~10K concurrent sessions" vertex="1">
      <mxGeometry height="150" width="180" x="70" y="840" as="geometry" />
    </mxCell>
    <mxCell id="e_p_crm" edge="1" parent="1" source="planner" style="rounded=1;strokeColor=#9673a6;strokeWidth=1.5;dashed=1;fontSize=10;" target="crm" value="Reads">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_p_mem" edge="1" parent="1" source="planner" style="rounded=1;strokeColor=#9673a6;strokeWidth=1.5;dashed=1;fontSize=10;" target="mem" value="Reads">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_approved" edge="1" parent="1" source="plan_box" style="rounded=1;strokeColor=#82b366;strokeWidth=3;fontSize=11;fontStyle=1;" target="exec_box" value="APPROVED PLAN">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="exec_box" parent="1" style="rounded=1;fillColor=#F0F8FF;strokeColor=#4A90D9;strokeWidth=2;dashed=1;dashPattern=8 4;" value="" vertex="1">
      <mxGeometry height="490" width="920" x="240" y="860" as="geometry" />
    </mxCell>
    <mxCell id="exec_title" parent="1" style="text;html=0;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;strokeColor=none;fillColor=none;" value="EXECUTION AGENTS (Each with Paired Critique Agent)" vertex="1">
      <mxGeometry height="25" width="600" x="400" y="868" as="geometry" />
    </mxCell>
    <mxCell id="exec_subtitle" parent="1" style="text;html=0;align=center;verticalAlign=middle;fontSize=10;fontColor=#888888;strokeColor=none;fillColor=none;" value="Max 3 critique retries → auto-escalate to Human Queue | All outputs go through Content Safety before delivery" vertex="1">
      <mxGeometry height="20" width="700" x="350" y="890" as="geometry" />
    </mxCell>
    <mxCell id="email" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10;align=left;spacingLeft=8;spacingTop=3;strokeWidth=2;" value="EMAIL AGENT&#xa;LLM: Gemini 2.0 Flash | API: SendGrid&#xa;&#xa;Personalized renewal emails (9 languages)&#xa;Segment-adaptive tone (LangSmith templates)&#xa;Policy doc RAG (Vector Search + Gemini Embeddings)&#xa;Tracks opens/clicks&#xa;Escalation: No open 3x → WA | Complaint → Human&#xa;&#xa;Target: 42% open rate (from 18%)" vertex="1">
      <mxGeometry height="170" width="250" x="270" y="925" as="geometry" />
    </mxCell>
    <mxCell id="email_c" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10;align=left;spacingLeft=8;spacingTop=3;strokeWidth=2;" value="EMAIL CRITIQUE&#xa;LLM: Gemini 2.5 Pro (evaluator)&#xa;&#xa;Factual accuracy vs RAG source&#xa;Tone score ≥7/10 or REJECT&#xa;Language quality ≥8/10 or REJECT&#xa;Zero hallucinated financial figures&#xa;Correct premium/benefits amounts?" vertex="1">
      <mxGeometry height="150" width="250" x="270" y="1130" as="geometry" />
    </mxCell>
    <mxCell id="e_em" edge="1" parent="1" source="email" style="rounded=1;strokeColor=#82b366;strokeWidth=1.5;fontSize=9;" target="email_c" value="Response + evidence">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_em_r" edge="1" parent="1" source="email_c" style="rounded=1;strokeColor=#b85450;strokeWidth=1.5;dashed=1;fontSize=9;exitX=1;exitY=0.5;entryX=1;entryY=0.5;curved=1;" target="email" value="Retry (max 3)">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="550" y="1205" />
          <mxPoint x="550" y="1010" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="wa" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10;align=left;spacingLeft=8;spacingTop=3;strokeWidth=2;" value="WHATSAPP AGENT&#xa;LLM: Gemini 2.0 Flash | API: Gupshup&#xa;&#xa;Interactive conversations (9 languages)&#xa;Payment QR: Razorpay / PhonePe Business&#xa;Intent detection: pay, EMI, hardship, human, receipt&#xa;Session memory: Redis (TTL 72h) + Firestore&#xa;Escalation: Negative sentiment → Human | No response 24h → Voice&#xa;~10K concurrent sessions&#xa;&#xa;Target: 58% response rate (from N/A)" vertex="1">
      <mxGeometry height="180" width="260" x="555" y="925" as="geometry" />
    </mxCell>
    <mxCell id="wa_c" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10;align=left;spacingLeft=8;spacingTop=3;strokeWidth=2;" value="WHATSAPP CRITIQUE&#xa;LLM: Gemini 2.5 Pro (evaluator)&#xa;&#xa;Verifies response vs evidence&#xa;EMI eligibility correct?&#xa;Correct policy data / amounts?&#xa;Tone empathy check&#xa;Cross-validate vs CRM + product catalog" vertex="1">
      <mxGeometry height="150" width="260" x="555" y="1130" as="geometry" />
    </mxCell>
    <mxCell id="e_wa" edge="1" parent="1" source="wa" style="rounded=1;strokeColor=#82b366;strokeWidth=1.5;fontSize=9;" target="wa_c" value="Response + evidence">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_wa_r" edge="1" parent="1" source="wa_c" style="rounded=1;strokeColor=#b85450;strokeWidth=1.5;dashed=1;fontSize=9;exitX=1;exitY=0.5;entryX=1;entryY=0.5;curved=1;" target="wa" value="Retry (max 3)">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="850" y="1205" />
          <mxPoint x="850" y="1015" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="voice" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10;align=left;spacingLeft=8;spacingTop=3;strokeWidth=2;" value="VOICE AGENT&#xa;TTS: Google WaveNet | STT: Google Chirp&#xa;LLM: Gemini 2.0 Flash | Telephony: Exotel&#xa;&#xa;Outbound AI calls (9 languages)&#xa;Preferred-time calling (41% evening/weekend)&#xa;Mid-call RAG: LangChain RetrievalQA&#xa;Objection library: 150-200+ pairs&#xa;Live payment check before calling&#xa;Escalation: Human request / Distress / 3 objections&#xa;&#xa;Target: 31% conversion (from N/A)" vertex="1">
      <mxGeometry height="190" width="250" x="855" y="925" as="geometry" />
    </mxCell>
    <mxCell id="voice_c" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10;align=left;spacingLeft=8;spacingTop=3;strokeWidth=2;" value="VOICE CRITIQUE&#xa;LLM: Gemini 2.5 Pro (evaluator)&#xa;&#xa;Verifies script vs evidence&#xa;Correct objection handling?&#xa;Accurate premium/grace amounts?&#xa;Streaming eval: pre-call full script,&#xa;mid-call spot checks &lt;200ms" vertex="1">
      <mxGeometry height="150" width="250" x="855" y="1130" as="geometry" />
    </mxCell>
    <mxCell id="e_vo" edge="1" parent="1" source="voice" style="rounded=1;strokeColor=#82b366;strokeWidth=1.5;fontSize=9;" target="voice_c" value="Response + evidence">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_vo_r" edge="1" parent="1" source="voice_c" style="rounded=1;strokeColor=#b85450;strokeWidth=1.5;dashed=1;fontSize=9;exitX=1;exitY=0.5;entryX=1;entryY=0.5;curved=1;" target="voice" value="Retry (max 3)">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="1130" y="1205" />
          <mxPoint x="1130" y="1020" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="esc_email_wa" edge="1" parent="1" source="email" style="rounded=1;strokeColor=#CC0000;strokeWidth=1;dashed=1;fontSize=8;entryX=0;entryY=0.3;exitX=1;exitY=0.3;" target="wa" value="No open 3x → WA">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="esc_wa_voice" edge="1" parent="1" source="wa" style="rounded=1;strokeColor=#CC0000;strokeWidth=1;dashed=1;fontSize=8;entryX=0;entryY=0.3;exitX=1;exitY=0.3;" target="voice" value="No response 24h → Voice">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_wa_redis" edge="1" parent="1" source="wa" style="rounded=1;strokeColor=#9673a6;strokeWidth=1;dashed=1;fontSize=9;exitX=0;exitY=0.7;" target="redis_cache" value="Session R/W">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="safety" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#FFE6E6;strokeColor=#CC0000;fontSize=10;align=center;strokeWidth=2;" value="CONTENT SAFETY + COMPLIANCE GATE (~800ms combined latency | &lt;5% rejection target)&#xa;&#xa;CRITIQUE CHECKS: Factual accuracy (RAG grounding) | Tone ≥7/10 | Language quality ≥8/10 | Hallucination detection | Cross-validate vs CRM + catalog&#xa;COMPLIANCE CHECKS: IRDAI disclosure (AI ID, opt-out, grievance #) | Mis-selling detection (HARD REJECT) | PII masking DPDPA 2023 (Aadhaar/PAN) | TRAI DND (no calls 9PM-9AM, max 3/channel/week)&#xa;SAFETY CHECKS: Distress keyword detection (9 languages, &lt;1s) | PII leak → CISO alert | Regulatory violation prevention" vertex="1">
      <mxGeometry height="130" width="820" x="290" y="1420" as="geometry" />
    </mxCell>
    <mxCell id="e_exec_safety" edge="1" parent="1" source="exec_box" style="rounded=1;strokeColor=#CC0000;strokeWidth=2;fontSize=10;" target="safety" value="All agent outputs">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_safety_hq" edge="1" parent="1" source="safety" style="rounded=1;strokeColor=#CC0000;strokeWidth=2;dashed=1;fontSize=9;" target="hq" value="Distress / Mis-selling / PII leak">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="1300" y="1485" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="customer" parent="1" style="ellipse;whiteSpace=wrap;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;fontStyle=1;align=center;strokeWidth=2;" value="POLICYHOLDER&#xa;4.8M customers | 9 languages | 14.4L renewals/yr&#xa;Email / WhatsApp / Voice&#xa;NPS target: ≥55 (from 34)" vertex="1">
      <mxGeometry height="110" width="340" x="530" y="1620" as="geometry" />
    </mxCell>
    <mxCell id="e_safety_cust" edge="1" parent="1" source="safety" style="rounded=1;strokeColor=#82b366;strokeWidth=2.5;fontSize=10;" target="customer" value="Approved response delivered">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_cust_back" edge="1" parent="1" source="customer" style="rounded=1;strokeColor=#d6b656;strokeWidth=1.5;dashed=1;fontSize=10;curved=1;" target="t2" value="Customer replies (inbound)">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="190" y="1675" />
          <mxPoint x="190" y="170" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="hq" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#E6E6FA;strokeColor=#7B68EE;fontSize=10;align=left;spacingLeft=8;spacingTop=3;strokeWidth=2;" value="HUMAN QUEUE MANAGER&#xa;Dashboard: React.js + Firebase Hosting&#xa;API: FastAPI on Cloud Run&#xa;&#xa;Routes escalated cases to right specialist&#xa;with full context briefing note:&#xa;- Policy summary + all prior AI interactions&#xa;- Detected sentiment + risk level&#xa;- Recommended approach&#xa;- Critique/Compliance rejection reason&#xa;&#xa;Target: ≤10% human escalation (from 100%)" vertex="1">
      <mxGeometry height="200" width="250" x="1240" y="850" as="geometry" />
    </mxCell>
    <mxCell id="e_exec_hq" edge="1" parent="1" source="exec_box" style="rounded=1;strokeColor=#7B68EE;strokeWidth=2;dashed=1;fontSize=10;" target="hq" value="3 critique failures">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="team" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#E6E6FA;strokeColor=#7B68EE;fontSize=10;align=left;spacingLeft=8;spacingTop=3;strokeWidth=2;" value="TEAM OF 20 SPECIALISTS (from 123)&#xa;&#xa;8 Senior Renewal Relationship Managers (₹7.2-10L)&#xa;5 Revival Specialists (₹7.5-9.5L)&#xa;2 Compliance + Grievance Handlers (₹8-11L)&#xa;3 AI Operations + Quality Managers (₹10-14L)&#xa;1 Renewal Head (₹22-28L)&#xa;1 AI Trainer / Prompt Engineer (₹6L retainer)&#xa;&#xa;All trained on: React dashboard, LangSmith,&#xa;escalation workflows, Critique/Compliance override" vertex="1">
      <mxGeometry height="190" width="250" x="1240" y="1100" as="geometry" />
    </mxCell>
    <mxCell id="e_hq_team" edge="1" parent="1" source="hq" style="rounded=1;strokeColor=#7B68EE;strokeWidth=2;fontSize=10;" target="team" value="Routes with context">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_exec_orch" edge="1" parent="1" source="exec_box" style="rounded=1;strokeColor=#6c8ebf;strokeWidth=2;dashed=1;fontSize=10;exitX=0;exitY=0.3;entryX=0;entryY=0.7;curved=1;" target="orch" value="Execution results returned">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="210" y="1000" />
          <mxPoint x="210" y="380" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="audit" parent="1" style="shape=cylinder3;whiteSpace=wrap;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#FF9933;strokeColor=#CC6600;fontSize=10;align=center;strokeWidth=2;fontColor=#FFFFFF;" value="AUDIT DATABASE&#xa;Cloud SQL (PostgreSQL) — Separate, Immutable, Append-Only&#xa;&#xa;Every agent response stored as JSON:&#xa;trace_id, step_sequence, agent_id, input, response,&#xa;evidence, critique_result, compliance_verdict,&#xa;critique_score, RAG_sources, model_version, timestamp&#xa;&#xa;HA regional | Daily backup 30-day retention&#xa;7-year IRDAI audit retention (BigQuery archive)&#xa;Agents WRITE only — Never READ&#xa;IRDAI audit-ready, tamper-proof, DPDPA 2023 compliant" vertex="1">
      <mxGeometry height="230" width="380" x="510" y="1810" as="geometry" />
    </mxCell>
    <mxCell id="e_all_audit" edge="1" parent="1" source="customer" style="rounded=1;strokeColor=#CC6600;strokeWidth=3;fontSize=10;fontStyle=1;" target="audit" value="WRITES JSON evidence (every agent, every step)">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e_safety_audit" edge="1" parent="1" source="safety" style="rounded=1;strokeColor=#CC6600;strokeWidth=2;dashed=1;fontSize=9;entryX=0;entryY=0.3;" target="audit" value="Safety verdicts + PII incidents">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="290" y="1485" />
          <mxPoint x="290" y="1880" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="e_hq_audit" edge="1" parent="1" source="team" style="rounded=1;strokeColor=#CC6600;strokeWidth=1.5;dashed=1;fontSize=9;entryX=1;entryY=0.3;" target="audit" value="Human actions logged">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="1200" y="1195" />
          <mxPoint x="1200" y="1880" />
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="bq_warehouse" parent="1" style="shape=cylinder3;whiteSpace=wrap;boundedLbl=1;backgroundOutline=1;size=12;fillColor=#DAE8FC;strokeColor=#6C8EBF;fontSize=10;align=center;strokeWidth=2;" value="BigQuery (Analytics Warehouse)&#xa;&#xa;4.8M customer records + propensity scores&#xa;Full interaction history (all channels)&#xa;10 KPI metrics + Critique/Compliance logs&#xa;7-year retention | Feeds → Looker Studio&#xa;IRDAI audit archive" vertex="1">
      <mxGeometry height="150" width="220" x="150" y="1870" as="geometry" />
    </mxCell>
    <mxCell id="e_audit_bq" edge="1" parent="1" source="audit" style="rounded=1;strokeColor=#6C8EBF;strokeWidth=1.5;dashed=1;fontSize=9;" target="bq_warehouse" value="Async sync (Pub/Sub)">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="observability" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#FFF2CC;strokeColor=#D6B656;fontSize=10;align=left;spacingLeft=8;spacingTop=3;strokeWidth=2;" value="OBSERVABILITY STACK&#xa;&#xa;LangSmith: Prompt tracing, agent action logs&#xa;Cloud Monitoring: Infrastructure metrics, uptime&#xa;Looker Studio: 10 KPI dashboards (from BigQuery)&#xa;PagerDuty: Alerting + incident response&#xa;&#xa;Critique rejection rates + Compliance verdicts in dashboards&#xa;Full trace of every agent decision end-to-end" vertex="1">
      <mxGeometry height="140" width="310" x="950" y="1830" as="geometry" />
    </mxCell>
    <mxCell id="e_bq_obs" edge="1" parent="1" source="bq_warehouse" style="rounded=1;strokeColor=#D6B656;strokeWidth=1.5;dashed=1;fontSize=9;" target="observability" value="Feeds dashboards">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="dashboard" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#E6E6FA;strokeColor=#7B68EE;fontSize=10;align=left;spacingLeft=10;spacingTop=5;strokeWidth=2;" value="HUMAN INVESTIGATION DASHBOARD (React.js + Firebase Hosting)&#xa;&#xa;Human investigators READ Audit DB for:&#xa;- Dispute backtracking (agent-by-agent JSON trace with Trace ID)&#xa;- IRDAI compliance audits (every message carries full audit stamp)&#xa;- Pinpoint which agent gave wrong response (critique score + verdict)&#xa;- Weekly 5% quality evaluation + Critique false-positive review&#xa;&#xa;Used by: AI Ops Manager (3), Compliance Handler (2), Renewal Head (1)&#xa;Cadence: Weekly quality eval | Monthly KPI + objection refresh | Quarterly Board review | Annual DPDPA audit" vertex="1">
      <mxGeometry height="150" width="680" x="260" y="2110" as="geometry" />
    </mxCell>
    <mxCell id="e_audit_dash" edge="1" parent="1" source="audit" style="rounded=1;strokeColor=#7B68EE;strokeWidth=2.5;fontSize=10;fontStyle=1;" target="dashboard" value="READS for backtracking + audits">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="kpi_box" parent="1" style="rounded=1;fillColor=#E8F5E9;strokeColor=#4CAF50;strokeWidth=2;" value="" vertex="1">
      <mxGeometry height="220" width="680" x="260" y="2330" as="geometry" />
    </mxCell>
    <mxCell id="kpi_title" parent="1" style="text;html=0;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;strokeColor=none;fillColor=none;" value="10 SUCCESS KPIs — FINAL TARGETS (Year 1)" vertex="1">
      <mxGeometry height="25" width="400" x="400" y="2338" as="geometry" />
    </mxCell>
    <mxCell id="kpi_list" parent="1" style="text-html=0;align=left;verticalAlign=top;fontSize=10;strokeColor=none;fillColor=none;spacingLeft=10;" value="1. 13th Month Persistency: 71% → 88%                  6. Human Escalation: 100% → ≤10%&#xa;2. Cost per Renewal: ₹182 → ₹45                           7. Customer NPS: 34 → ≥55&#xa;3. Email Open Rate: 18% → 42%                              8. IRDAI Violations: 12/yr → 0&#xa;4. WhatsApp Response Rate: N/A → 58%                 9. AI Accuracy Score: N/A → ≥87%&#xa;5. Voice Conversion Rate: N/A → 31%                     10. Distress Escalation &lt;2h: N/A → 100%" vertex="1">
      <mxGeometry height="100" width="640" x="280" y="2370" as="geometry" />
    </mxCell>
    <mxCell id="financial_summary" parent="1" style="text;html=0;align=center;verticalAlign=top;fontSize=11;fontStyle=1;strokeColor=none;fillColor=none;" value="YEAR 1 FINANCIALS: Cost Saving ₹12.9 Cr + Revenue Uplift ₹38.9 Cr — Investment ₹3.78 Cr = NET ₹48 Cr  |  3-Year NPV (12%): ₹89 Cr" vertex="1">
      <mxGeometry height="30" width="650" x="275" y="2480" as="geometry" />
    </mxCell>
    <mxCell id="kpi_note" parent="1" style="text;html=0;align=center;verticalAlign=middle;fontSize=9;fontColor=#888888;strokeColor=none;fillColor=none;" value="Reviewed: Monthly by Renewal Head | Quarterly by Board Risk Committee (CTO + Chief Actuary + CISO + Compliance Head)" vertex="1">
      <mxGeometry height="20" width="650" x="275" y="2515" as="geometry" />
    </mxCell>
    <mxCell id="gcp_note" parent="1" style="rounded=1;whiteSpace=wrap;fillColor=#F5F5F5;strokeColor=#CCCCCC;fontSize=9;align=left;spacingLeft=8;spacingTop=3;strokeWidth=1;" value="GCP INFRASTRUCTURE — Mumbai (asia-south1) | Data Residency: India Only&#xa;&#xa;Compute: Cloud Run (auto-scaling for Q4 peak ~5,500/day) | Network: VPC + IAM | Encryption: Cloud KMS (rest) + TLS 1.3 (transit)&#xa;Privacy: Cloud DLP | Events: Cloud Functions + Pub/Sub | Tasks: Cloud Scheduler + Cloud Tasks | Hosting: Firebase | Monitoring: Cloud Monitoring&#xa;Frameworks: IRDAI Tech Framework (2024) | RBI FREE-AI Framework (2025) | DPDPA 2023 | Zero-downtime deployment" vertex="1">
      <mxGeometry height="90" width="680" x="260" y="2570" as="geometry" />
    </mxCell>
    <mxCell id="leg_box" parent="1" style="rounded=1;fillColor=#FAFAFA;strokeColor=#CCCCCC;strokeWidth=1;" value="" vertex="1">
      <mxGeometry height="360" width="280" x="1240" y="1430" as="geometry" />
    </mxCell>
    <mxCell id="leg_title" parent="1" style="text;html=0;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;strokeColor=none;fillColor=none;" value="LEGEND" vertex="1">
      <mxGeometry height="25" width="260" x="1250" y="1435" as="geometry" />
    </mxCell>
    <mxCell id="l1" parent="1" style="rounded=1;fillColor=#fff2cc;strokeColor=#d6b656;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1475" as="geometry" />
    </mxCell>
    <mxCell id="l1t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="Trigger Events" vertex="1">
      <mxGeometry height="22" width="180" x="1290" y="1470" as="geometry" />
    </mxCell>
    <mxCell id="l2" parent="1" style="rounded=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1505" as="geometry" />
    </mxCell>
    <mxCell id="l2t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="Orchestrator (LangGraph + Gemini)" vertex="1">
      <mxGeometry height="22" width="220" x="1290" y="1500" as="geometry" />
    </mxCell>
    <mxCell id="l3" parent="1" style="rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1535" as="geometry" />
    </mxCell>
    <mxCell id="l3t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="Execution / Planner Agents (Gemini 2.0 Flash)" vertex="1">
      <mxGeometry height="22" width="240" x="1290" y="1530" as="geometry" />
    </mxCell>
    <mxCell id="l4" parent="1" style="rounded=1;fillColor=#f8cecc;strokeColor=#b85450;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1565" as="geometry" />
    </mxCell>
    <mxCell id="l4t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="Critique Agents (Gemini 2.5 Pro evaluator)" vertex="1">
      <mxGeometry height="22" width="240" x="1290" y="1560" as="geometry" />
    </mxCell>
    <mxCell id="l5" parent="1" style="rounded=1;fillColor=#e1d5e7;strokeColor=#9673a6;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1595" as="geometry" />
    </mxCell>
    <mxCell id="l5t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="Operational Data (CRM + Memory + Redis)" vertex="1">
      <mxGeometry height="22" width="240" x="1290" y="1590" as="geometry" />
    </mxCell>
    <mxCell id="l6" parent="1" style="rounded=1;fillColor=#FF9933;strokeColor=#CC6600;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1625" as="geometry" />
    </mxCell>
    <mxCell id="l6t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="Audit DB (write-only, immutable evidence)" vertex="1">
      <mxGeometry height="22" width="240" x="1290" y="1620" as="geometry" />
    </mxCell>
    <mxCell id="l7" parent="1" style="rounded=1;fillColor=#E6E6FA;strokeColor=#7B68EE;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1655" as="geometry" />
    </mxCell>
    <mxCell id="l7t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="Human Layer (Queue, Team, Dashboard)" vertex="1">
      <mxGeometry height="22" width="240" x="1290" y="1650" as="geometry" />
    </mxCell>
    <mxCell id="l8" parent="1" style="rounded=1;fillColor=#FFE6E6;strokeColor=#CC0000;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1685" as="geometry" />
    </mxCell>
    <mxCell id="l8t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="Safety + Compliance Gate (~800ms)" vertex="1">
      <mxGeometry height="22" width="240" x="1290" y="1680" as="geometry" />
    </mxCell>
    <mxCell id="l9" parent="1" style="rounded=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1715" as="geometry" />
    </mxCell>
    <mxCell id="l9t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="Analytics (BigQuery → Looker Studio)" vertex="1">
      <mxGeometry height="22" width="240" x="1290" y="1710" as="geometry" />
    </mxCell>
    <mxCell id="l10" parent="1" style="rounded=1;fillColor=#FFF2CC;strokeColor=#D6B656;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1745" as="geometry" />
    </mxCell>
    <mxCell id="l10t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="Observability (LangSmith + PagerDuty)" vertex="1">
      <mxGeometry height="22" width="240" x="1290" y="1740" as="geometry" />
    </mxCell>
    <mxCell id="l11" parent="1" style="rounded=1;fillColor=#E8F5E9;strokeColor=#4CAF50;" value="" vertex="1">
      <mxGeometry height="14" width="18" x="1260" y="1775" as="geometry" />
    </mxCell>
    <mxCell id="l11t" parent="1" style="text;html=0;align=left;fontSize=10;strokeColor=none;fillColor=none;" value="KPI Scoreboard (10 metrics)" vertex="1">
      <mxGeometry height="22" width="240" x="1290" y="1770" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

## System Overview
The v2.0 Architecture is designed to securely and effectively engage life insurance customers who are due for renewal. Through a state-machine implementation via LangGraph, it relies on multiple specialized AI agents. 

### Trigger Mechanisms
- **Policy Due Date:** Triggered algorithmically exactly 45 days before expiry (T-45).
- **Customer Inbound Message:** Customer returning from an active channel (Email, WhatsApp).
- **Lapse Event (Revival):** Post-lapse automated out-reach.

### The 6 Primary Decision & Execution Agents
These agents function dynamically to achieve the final outcome. All LLM models primarily rely on **Gemini 2.0 Flash**.
1. **Orchestrator Agent**: Serves as the traffic controller parsing Risk, Channel propensity, Language, and tone mapping parameters before calling the specific execution pathway. 
2. **Planner Agent**: Uses data obtained from the internal CRM rules to plan how to execute the objective. Formulates execution channels, timing, and initial templates. 
3. **Planner Critique**: Acts as a peer-reviewer to validate the proposed execution pipeline designed by the Planner Agent. 
4. **Email Agent (SendGrid API)**: Drafts contextual outreach emails to policyholders dynamically embedded with exact premium limits.
5. **WhatsApp Agent (Gupshup API)**: Simulates 2-way real-time conversational SMS tracking intent detection directly through users mobile phone. 
6. **Voice Agent (Google Text-To-Speech / Exotel)**: Spoken, outbound localized human-sounding conversations dynamically interacting and capturing feedback. 

### Safety & Guardrails
- Before any outreach hits the customer, outputs run through the **Content Safety Gate**, evaluating for compliance breaches (IRDAI checks, mis-selling, unapproved distress markers) utilizing local lightweight regexes and keyword block-lists.
- All actions undergo immutable append-only storage directly within the **Audit DB** utilizing secure UUID tracing.
