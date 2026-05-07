def adapt_for_frontend(dashboard: dict, data: dict) -> dict:
    """
    Adapts the raw backend output into a flattened, UI-friendly format.
    Prevents the frontend (React/Vue) from crashing on deeply nested nulls.
    """
    
    # Safe array fallbacks
    deadlines = dashboard.get("deadline_alerts") or []
    summary_cards = dashboard.get("summary_cards") or []
    timeline = dashboard.get("timeline") or []
    tags = dashboard.get("tags") or []
    recommended_actions = dashboard.get("recommended_actions") or []
    decision_reasoning = dashboard.get("decision_reasoning") or []
    decision_intelligence = dashboard.get("decision_intelligence") or {}
    
    # Color mapping for UI libraries (Bootstrap/Tailwind safe)
    color_map = {
        "red": "danger",
        "orange": "warning",
        "yellow": "info",
        "green": "success",
        "gray": "secondary",
        "danger": "danger",
        "warning": "warning",
        "info": "info",
        "success": "success",
        "secondary": "secondary"
    }
    
    raw_color = dashboard.get("priority_color", "gray")
    ui_color = color_map.get(raw_color, "secondary")

    return {
        "ui_risk_meter": {
            "value": int(dashboard.get("risk_meter") or 0),
            "label": "Legal Risk",
            "color": str(ui_color)
        },
        "ui_heat_score": {
            "value": int(dashboard.get("heat_score") or 0),
            "label": "Action Heat",
            "color": str(ui_color)
        },
        "ui_urgency": {
            "badge_text": str(dashboard.get("urgency_badge") or "Unknown"),
            "badge_color": str(ui_color)
        },
        "ui_tags": [{"label": str(t), "key": str(t).lower().replace(" ", "_")} for t in (tags if isinstance(tags, list) else [])],
        "ui_deadlines": [
            {
                "days": int(dl.get("normalized_days")) if isinstance(dl, dict) and dl.get("normalized_days") is not None else "N/A",
                "raw_text": str(dl.get("raw") or "") if isinstance(dl, dict) else "",
                "is_critical": bool(dl.get("normalized_days") is not None and dl.get("normalized_days") < 7) if isinstance(dl, dict) else False
            }
            for dl in (deadlines if isinstance(deadlines, list) else [])
        ],
        "ui_cards": [{"id": i, "content": str(card)} for i, card in enumerate(summary_cards if isinstance(summary_cards, list) else [])],
        "ui_timeline_events": [
            {
                "id": i,
                "date": str(t.get("date") or "") if isinstance(t, dict) else "",
                "event": str(t.get("event") or "") if isinstance(t, dict) else ""
            }
            for i, t in enumerate(timeline if isinstance(timeline, list) else [])
        ],
        "ui_voice": str(dashboard.get("voice_narration") or ""),
        "ui_ai_reasoning": str(dashboard.get("ai_reasoning") or ""),
        "ui_appeal_recommended": bool(dashboard.get("appeal_recommended") or False),
        "ui_appeal_suggestion": str(dashboard.get("appeal_suggestion") or "Not Recommended"),
        "ui_recommended_actions": [
            {
                "action": str(action.get("action") or "Review order"),
                "department": str(action.get("department") or "Legal Department"),
                "priority": str(action.get("priority") or "Low"),
                "risk_level": str(action.get("risk_level") or "Low"),
                "deadline": str(action.get("deadline") or "Not specified")
            }
            for action in (recommended_actions if isinstance(recommended_actions, list) else [])
            if isinstance(action, dict)
        ],
        "ui_decision_reasoning": [
            str(item)
            for item in (decision_reasoning if isinstance(decision_reasoning, list) else [])
        ],
        "decision_intelligence": {
            "case_number": str(
                decision_intelligence.get("case_number")
                or (data.get("case_number", {}).get("value") if isinstance(data.get("case_number"), dict) else "")
                or ""
            ) if isinstance(decision_intelligence, dict) else "",
            "recommended_actions": [
                {
                    "action": str(action.get("action") or "Review order"),
                    "department": str(action.get("department") or "Legal Department"),
                    "priority": str(action.get("priority") or "Low"),
                    "risk_level": str(action.get("risk_level") or "Low"),
                    "deadline": str(action.get("deadline") or "Not specified")
                }
                for action in (
                    decision_intelligence.get("recommended_actions")
                    if isinstance(decision_intelligence, dict) and isinstance(decision_intelligence.get("recommended_actions"), list)
                    else (recommended_actions if isinstance(recommended_actions, list) else [])
                )
                if isinstance(action, dict)
            ],
            "priority_level": str(
                (
                    decision_intelligence.get("priority_level")
                    or dashboard.get("urgency_badge")
                    or "Unknown"
                )
                if isinstance(decision_intelligence, dict)
                else (dashboard.get("urgency_badge") or "Unknown")
            ),
            "risk_level": str(
                (
                    decision_intelligence.get("risk_level")
                    or dashboard.get("severity")
                    or "Unknown"
                )
                if isinstance(decision_intelligence, dict)
                else (dashboard.get("severity") or "Unknown")
            ),
            "appeal_suggestion": str(
                (
                    decision_intelligence.get("appeal_suggestion")
                    or dashboard.get("appeal_suggestion")
                    or "Not Recommended"
                )
                if isinstance(decision_intelligence, dict)
                else (dashboard.get("appeal_suggestion") or "Not Recommended")
            ),
            "reasoning": [
                str(item)
                for item in (
                    decision_intelligence.get("reasoning")
                    if isinstance(decision_intelligence, dict) and isinstance(decision_intelligence.get("reasoning"), list)
                    else (decision_reasoning if isinstance(decision_reasoning, list) else [])
                )
            ]
        },
        "ui_severity": str(dashboard.get("severity") or "Unknown"),
        "ui_compliance_urgency": str(dashboard.get("compliance_urgency") or "Unknown"),
        "ui_authority_involved": str(dashboard.get("authority_involved") or "Unknown"),
        "ui_legal_impact": str(dashboard.get("legal_impact") or "Unknown"),
        "ui_citizen_impact": str(dashboard.get("citizen_impact") or "Unknown"),
        "ui_recommended_action": str(dashboard.get("recommended_action") or "Unknown"),
        "ui_possible_consequences": str(dashboard.get("possible_consequences") or "Unknown"),
        
        "ui_probable_case_category": str(dashboard.get("probable_case_category") or "Unknown"),
        "ui_compliance_probability": str(dashboard.get("compliance_probability") or "Unknown"),
        "ui_escalation_risk": str(dashboard.get("escalation_risk") or "Unknown"),
        "ui_public_impact_score": int(dashboard.get("public_impact_score") or 0),
        "ui_procedural_complexity": str(dashboard.get("procedural_complexity") or "Unknown"),
        "ui_ai_confidence_score": int(dashboard.get("ai_confidence_score") or 0),
        "ui_extraction_quality": str(dashboard.get("extraction_quality") or "Unknown"),
        "ui_reasoning_trace": [str(t) for t in (dashboard.get("reasoning_trace") if isinstance(dashboard.get("reasoning_trace"), list) else [])],
        "ui_model_decision_basis": str(dashboard.get("model_decision_basis") or "Unknown"),
        "ui_alerts": [
            {
                "severity": str(a.get("severity", "Info")),
                "message": str(a.get("message", "")),
                "color": str(color_map.get(a.get("color", "gray").lower(), "secondary"))
            } for a in (dashboard.get("alerts") if isinstance(dashboard.get("alerts"), list) else [])
        ],
        "ui_executive_report": dashboard.get("executive_report") if isinstance(dashboard.get("executive_report"), dict) else {}
    }
