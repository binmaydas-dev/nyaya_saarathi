from __future__ import annotations

import re
from loguru import logger


TAG_CLUSTERS = {
    "Compensation": [r"compensation", r"damages"],
    "Land Dispute": [r"land", r"property"],
    "Criminal": [r"criminal", r"bail", r"fir"],
    "Tax": [r"tax", r"gst"],
    "Labor": [r"labor", r"wages"],
    "Environmental": [r"environment", r"pollution"],
    "Roads": [r"road", r"street", r"pothole", r"municipal"],
    "Pension": [r"pension", r"welfare", r"benefit"]
}

ACTION_RULES = [
    {
        "name": "compensation",
        "patterns": [r"\bpay\b.*\bcompensation\b", r"\bcompensation\b", r"\bdamages\b", r"\bcompensate\b"],
        "action": "Release compensation amount",
        "reason": "Detected compensation directive",
        "priority": "High",
        "risk": "High"
    },
    {
        "name": "compliance_report",
        "patterns": [r"\bsubmit\b.*\bcompliance\s+report\b", r"\bfile\b.*\bcompliance\s+report\b", r"\bstatus\s+report\b", r"\bcounter\s+affidavit\b"],
        "action": "Prepare compliance submission",
        "reason": "Detected compliance reporting order",
        "priority": "Medium",
        "risk": "Medium"
    },
    {
        "name": "land_restoration",
        "patterns": [r"\brestore\b.*\bland\b", r"\bland\b.*\brestore\b", r"\brestoration\b", r"\bvacate\b.*\b(premises|land|property)\b"],
        "action": "Initiate land restoration process",
        "reason": "Detected land restoration directive",
        "priority": "High",
        "risk": "High"
    },
    {
        "name": "payment",
        "patterns": [r"\bpay\b.*\b(amount|sum|arrears|dues)\b", r"\bdeposit\b.*\b(amount|sum|dues)\b", r"\brelease\b.*\b(funds?|amount|sum)\b"],
        "action": "Process court-directed payment",
        "reason": "Detected payment directive",
        "priority": "High",
        "risk": "High"
    },
    {
        "name": "road_work",
        "patterns": [r"\brepair\b.*\broad\b", r"\brestore\b.*\broad\b", r"\bremove\b.*\bencroachment\b", r"\broad\b.*\bmaintenance\b"],
        "action": "Initiate municipal works action",
        "reason": "Detected municipal infrastructure directive",
        "priority": "Medium",
        "risk": "Medium"
    },
    {
        "name": "pension",
        "patterns": [r"\brelease\b.*\bpension\b", r"\bpay\b.*\bpension\b", r"\bpension\b.*\barrears\b"],
        "action": "Process pension benefit release",
        "reason": "Detected welfare benefit directive",
        "priority": "High",
        "risk": "Medium"
    },
    {
        "name": "routine_compliance",
        "patterns": [r"\bcomply\b", r"\bcompliance\b", r"\bshall\b", r"\bdirected\b", r"\bmust\b"],
        "action": "Coordinate compliance with court direction",
        "reason": "Detected mandatory court direction",
        "priority": "Medium",
        "risk": "Medium"
    }
]

DEPARTMENT_RULES = [
    ("Revenue Department", [r"\bland\b", r"\bproperty\b", r"\bcompensation\b", r"\bacquisition\b", r"\bmutation\b"]),
    ("Municipal Department", [r"\broad\b", r"\bstreet\b", r"\bdrain\b", r"\bmunicipal\b", r"\bencroachment\b", r"\bpothole\b"]),
    ("Welfare Department", [r"\bpension\b", r"\bwelfare\b", r"\bbenefit\b", r"\bdisability\b", r"\bscholarship\b"]),
    ("Public Works Department", [r"\bconstruction\b", r"\bbuilding\b", r"\bbridge\b", r"\bpublic works\b"]),
    ("Police Department", [r"\bpolice\b", r"\bfir\b", r"\binvestigation\b", r"\bcriminal\b"]),
    ("Environment Department", [r"\benvironment\b", r"\bpollution\b", r"\bforest\b", r"\bwaste\b"]),
    ("Finance Department", [r"\btax\b", r"\bgst\b", r"\bfine\b", r"\bpenalty\b", r"\bdues\b"]),
    ("Health Department", [r"\bhealth\b", r"\bhospital\b", r"\bmedical\b"]),
    ("Education Department", [r"\beducation\b", r"\bschool\b", r"\bcollege\b"]),
]

PRIORITY_RANK = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}


def safe_int(value, default=999):

    try:

        if value is None:
            return default

        return int(value)

    except Exception:
        return default


def _unique_list(items: list) -> list:
    unique = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique


def _extract_directive_texts(text: str, extracted_data: dict) -> list:
    directives = []
    classified = extracted_data.get("classified_clauses", {})
    if isinstance(classified, dict):
        for key in ("orders", "suggestions"):
            for clause in classified.get(key, []) or []:
                if isinstance(clause, dict) and clause.get("text"):
                    directives.append(str(clause.get("text")))

    for key in ("orders", "important_clauses"):
        for clause in extracted_data.get(key, []) or []:
            if isinstance(clause, dict) and clause.get("text"):
                directives.append(str(clause.get("text")))
            elif isinstance(clause, str):
                directives.append(clause)

    for deadline in extracted_data.get("deadlines", []) or []:
        if isinstance(deadline, dict) and deadline.get("context"):
            directives.append(str(deadline.get("context")))

    if not directives and text:
        directives.append(text[:2500])

    return _unique_list([d.strip() for d in directives if isinstance(d, str) and d.strip()])


def _best_department(context: str) -> str:
    context_lower = context.lower()
    for department, patterns in DEPARTMENT_RULES:
        if any(re.search(pattern, context_lower) for pattern in patterns):
            return department
    return "Legal Department"


def _risk_level(risk_score: int, shortest_deadline: int, context: str) -> str:
    context_lower = context.lower()
    if shortest_deadline == 0 or risk_score >= 80 or re.search(r"\bcontempt\b|\barrest\b", context_lower):
        return "Critical"
    if shortest_deadline <= 7 or risk_score >= 60 or re.search(r"\bpenalty\b|\bfine\b", context_lower):
        return "High"
    if risk_score >= 35:
        return "Medium"
    return "Low"


def _highest_priority(*priorities: str) -> str:
    clean = [p for p in priorities if p in PRIORITY_RANK]
    if not clean:
        return "Low"
    return max(clean, key=lambda p: PRIORITY_RANK[p])


def _deadline_label(deadlines: list, shortest_deadline: int) -> str:
    if shortest_deadline == 999:
        return "Not specified"
    if shortest_deadline == 0:
        return "Immediate"
    for deadline in deadlines:
        if isinstance(deadline, dict) and deadline.get("normalized_days") == shortest_deadline:
            raw = str(deadline.get("raw") or "").strip()
            if raw:
                return raw
    return f"{shortest_deadline} days"


def _extract_large_amount(text_lower: str) -> bool:
    amount_patterns = [
        r"(?:rs\.?|inr|rupees)\s*([0-9][0-9,]*(?:\.\d+)?)\s*(crore|cr|lakh|lac)?",
        r"([0-9][0-9,]*(?:\.\d+)?)\s*(crore|cr|lakh|lac)\s*(?:rupees|rs\.?|inr)?"
    ]
    for pattern in amount_patterns:
        for amount, unit in re.findall(pattern, text_lower):
            try:
                value = float(amount.replace(",", ""))
            except Exception:
                continue
            unit = (unit or "").lower()
            if unit in ("crore", "cr"):
                value *= 10000000
            elif unit in ("lakh", "lac"):
                value *= 100000
            if value >= 1000000:
                return True
    return False


def _build_recommended_actions(text: str, extracted_data: dict, base_priority: str, risk_score: int, shortest_deadline: int) -> tuple[list, list]:
    deadlines = extracted_data.get("deadlines", [])
    if not isinstance(deadlines, list):
        deadlines = []

    deadline = _deadline_label(deadlines, shortest_deadline)
    directives = _extract_directive_texts(text, extracted_data)
    actions = []
    reasoning = []
    seen = set()

    for directive in directives:
        directive_lower = directive.lower()
        for rule in ACTION_RULES:
            if not any(re.search(pattern, directive_lower) for pattern in rule["patterns"]):
                continue

            action_priority = _highest_priority(base_priority, rule["priority"])
            if shortest_deadline == 0:
                action_priority = "Critical"
            elif shortest_deadline <= 7 and action_priority != "Critical":
                action_priority = "High"

            item = {
                "action": rule["action"],
                "department": _best_department(directive),
                "priority": action_priority,
                "risk_level": _highest_priority(_risk_level(risk_score, shortest_deadline, directive), rule["risk"]),
                "deadline": deadline
            }
            dedupe_key = (item["action"], item["department"], item["deadline"])
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            actions.append(item)
            reasoning.append(rule["reason"])

    if not actions:
        actions.append({
            "action": "Review order and assign nodal officer",
            "department": _best_department(text),
            "priority": base_priority if base_priority in PRIORITY_RANK else "Low",
            "risk_level": _risk_level(risk_score, shortest_deadline, text),
            "deadline": deadline
        })
        reasoning.append("No specific directive pattern detected; default review action generated")

    if shortest_deadline != 999:
        reasoning.append("Detected mandatory deadline")
    if re.search(r"\bshall\b|\bmust\b|\bdirected\b|\bmandatory\b|\bforthwith\b", text.lower()):
        reasoning.append("Detected mandatory court language")

    return actions[:6], _unique_list(reasoning)


def _appeal_suggestion(text_lower: str, risk_score: int, recommended_actions: list) -> tuple[str, bool, list]:
    reasons = []
    large_amount = _extract_large_amount(text_lower)
    penalty_language = bool(re.search(r"\bpenalt(y|ies)\b|\bfine\b|\bpunitive\b", text_lower))
    adverse_result = bool(re.search(r"\bdismissed\b|\badverse\b|\bset aside\b|\bquashed\b", text_lower))
    routine_compliance = any(
        "compliance" in action.get("action", "").lower()
        or "submission" in action.get("action", "").lower()
        for action in recommended_actions
        if isinstance(action, dict)
    )

    if adverse_result or (penalty_language and (large_amount or risk_score >= 70)):
        if penalty_language:
            reasons.append("Detected high-value penalty exposure")
        if adverse_result:
            reasons.append("Detected adverse case outcome")
        return "Appeal Recommended", True, reasons

    if routine_compliance:
        reasons.append("Routine compliance path detected")
        return "Compliance Preferred", False, reasons

    return "Not Recommended", False, reasons


def analyze_insights(text: str, extracted_data: dict) -> dict:

    logger.info("Running legal insights engine")

    try:

        text = text or ""
        text_lower = text.lower()
        if not isinstance(extracted_data, dict):
            extracted_data = {}

        # -----------------------------------
        # TAG DETECTION
        # -----------------------------------

        tags = []

        for tag, patterns in TAG_CLUSTERS.items():

            try:

                for pattern in patterns:

                    if re.search(pattern, text_lower):

                        tags.append(tag)
                        break

            except Exception:
                continue

        if not tags:
            tags.append("General")

        # -----------------------------------
        # BASE SCORES
        # -----------------------------------

        risk_score = 25
        heat_score = 25
        urgency_points = 0

        # -----------------------------------
        # LEGAL LANGUAGE ANALYSIS
        # -----------------------------------

        if re.search(r"penalty|fine|arrest|contempt", text_lower):

            risk_score += 25
            heat_score += 20

        if re.search(r"mandatory|immediate|forthwith|strictly", text_lower):

            urgency_points += 40
            heat_score += 25

        if re.search(r"compensation|compliance report|restore land|pension|road|municipal", text_lower):

            heat_score += 10

        # -----------------------------------
        # DEADLINE ANALYSIS
        # -----------------------------------

        shortest_deadline = 999

        deadlines = extracted_data.get("deadlines", [])

        if not isinstance(deadlines, list):
            deadlines = []

        for deadline in deadlines:

            if not isinstance(deadline, dict):
                continue

            days = safe_int(
                deadline.get("normalized_days")
            )

            if days < shortest_deadline:
                shortest_deadline = days

        # -----------------------------------
        # DEADLINE IMPACT
        # -----------------------------------

        if shortest_deadline == 0:

            urgency_points += 50
            risk_score += 20

        elif shortest_deadline <= 7:

            urgency_points += 40
            risk_score += 15

        elif shortest_deadline <= 30:

            urgency_points += 20

        # -----------------------------------
        # SCORE LIMITS
        # -----------------------------------

        risk_score = max(0, min(99, risk_score))
        heat_score = max(0, min(99, heat_score))

        # -----------------------------------
        # PRIORITY
        # -----------------------------------

        if urgency_points >= 80:

            urgency = "Critical"
            priority = "Critical"
            color = "red"

        elif urgency_points >= 40:

            urgency = "High"
            priority = "High"
            color = "orange"

        elif urgency_points >= 10:

            urgency = "Medium"
            priority = "Medium"
            color = "yellow"

        else:

            urgency = "Low"
            priority = "Low"
            color = "green"

        # -----------------------------------
        # DECISION INTELLIGENCE
        # -----------------------------------

        recommended_actions, decision_reasoning = _build_recommended_actions(
            text=text,
            extracted_data=extracted_data if isinstance(extracted_data, dict) else {},
            base_priority=priority,
            risk_score=risk_score,
            shortest_deadline=shortest_deadline
        )

        if shortest_deadline == 999:

            reasoning = (
                "No strict legal deadline detected."
            )

        else:

            reasoning = (
                f"Compliance expected within "
                f"{shortest_deadline} days."
            )

        # -----------------------------------
        # APPEAL LOGIC
        # -----------------------------------

        appeal_suggestion, appeal_recommended, appeal_reasons = _appeal_suggestion(
            text_lower=text_lower,
            risk_score=risk_score,
            recommended_actions=recommended_actions
        )

        reasoning_items = _unique_list(decision_reasoning + appeal_reasons)

        alerts = []
        if urgency_points >= 40:
            alerts.append({"severity": "Critical", "message": "Immediate compliance required", "color": "red"})
        if risk_score > 70:
            alerts.append({"severity": "High", "message": "Potential contempt risk detected", "color": "orange"})
        if shortest_deadline < 7:
            alerts.append({"severity": "High", "message": f"Approaching deadline in {shortest_deadline} days", "color": "orange"})
        if not alerts:
            alerts.append({"severity": "Info", "message": "Standard procedural monitoring advised", "color": "blue"})

        return {
            "urgency": urgency,
            "risk_score": risk_score,
            "heat_score": heat_score,
            "priority": priority,
            "priority_color": color,
            "appeal_recommended": appeal_recommended,
            "appeal_suggestion": appeal_suggestion,
            "reasoning": reasoning,
            "reasoning_items": reasoning_items,
            "recommended_actions": recommended_actions,
            "decision_intelligence": {
                "case_number": (
                    extracted_data.get("case_number", {}).get("value")
                    if isinstance(extracted_data.get("case_number"), dict)
                    else ""
                ),
                "recommended_actions": recommended_actions,
                "priority_level": priority,
                "risk_level": _highest_priority(*[
                    action.get("risk_level", "Low")
                    for action in recommended_actions
                    if isinstance(action, dict)
                ]),
                "appeal_suggestion": appeal_suggestion,
                "reasoning": reasoning_items
            },
            "tags": tags,
            "severity": "High" if risk_score > 60 else "Moderate",
            "compliance_urgency": "Immediate" if shortest_deadline < 7 else "Standard",
            "authority_involved": "High Court / Supreme Court" if "court" in text_lower else "Tribunal / Authority",
            "legal_impact": "Significant binding directives issued." if risk_score > 50 else "Procedural or minor observations.",
            "citizen_impact": "Direct action required by parties." if urgency_points > 20 else "No immediate citizen action needed.",
            "recommended_action": recommended_actions[0]["action"] if recommended_actions else "Review standard timeline.",
            "possible_consequences": "Legal escalation or contempt proceedings." if risk_score > 70 else "Standard procedural progression.",
            
            "probable_case_category": tags[0] if tags else "Civil Dispute",
            "compliance_probability": "Low" if risk_score > 70 else ("High" if urgency_points < 20 else "Medium"),
            "escalation_risk": "High" if "dismissed" in text_lower or risk_score > 60 else "Low",
            "public_impact_score": min(99, risk_score + (30 if "public" in text_lower or "environment" in text_lower else 0)),
            "procedural_complexity": "High" if len(text_lower) > 5000 else "Standard",
            "ai_confidence_score": 94 if len(text_lower) > 1000 else 72,
            "extraction_quality": "High" if len(tags) > 0 else "Moderate",
            "reasoning_trace": [
                f"Detected {len(tags)} critical legal keywords.",
                f"Calculated base risk score of {risk_score} using heuristic scaling.",
                f"Analyzed deadlines to infer an urgency level of {urgency}."
            ] + reasoning_items,
            "model_decision_basis": "Heuristic NLP aggregation based on explicit mandatory language extraction.",
            "alerts": alerts
        }

    except Exception as e:

        logger.error(f"Error in analyze_insights: {e}")

        return {
            "urgency": "Unknown",
            "risk_score": 0,
            "heat_score": 0,
            "priority": "Unknown",
            "priority_color": "gray",
            "appeal_recommended": False,
            "appeal_suggestion": "Not Recommended",
            "reasoning": "Insights generation failed. Safe fallback engaged.",
            "reasoning_items": ["Fallback mechanism engaged due to pipeline error."],
            "recommended_actions": [],
            "decision_intelligence": {
                "case_number": "",
                "recommended_actions": [],
                "priority_level": "Unknown",
                "risk_level": "Unknown",
                "appeal_suggestion": "Not Recommended",
                "reasoning": ["Fallback mechanism engaged due to pipeline error."]
            },
            "tags": [],
            "severity": "Unknown",
            "compliance_urgency": "Unknown",
            "authority_involved": "Unknown",
            "legal_impact": "Unknown",
            "citizen_impact": "Unknown",
            "recommended_action": "Consult legal counsel.",
            "possible_consequences": "Unknown",
            "probable_case_category": "Unknown",
            "compliance_probability": "Unknown",
            "escalation_risk": "Unknown",
            "public_impact_score": 0,
            "procedural_complexity": "Unknown",
            "ai_confidence_score": 0,
            "extraction_quality": "Failed",
            "reasoning_trace": ["Fallback mechanism engaged due to pipeline error."],
            "model_decision_basis": "Safe Fallback Default",
            "alerts": [{"severity": "Error", "message": "Insight generation failed", "color": "red"}]
        }
