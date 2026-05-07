import os
import uuid

def normalize_response(
    status: str,
    processing_mode: str,
    analytics: dict = None,
    data: dict = None,
    dashboard: dict = None,
    errors: list = None,
    request_id: str = None
) -> dict:
    """
    Standardizes the API response schema across the entire application.
    Ensures frontend integrations never break due to missing keys.
    """
    stable_id = request_id or str(uuid.uuid4())

    return {
        "status": status,
        "id": stable_id,
        "request_id": stable_id,
        "processing_mode": processing_mode,
        "analytics": analytics or {
            "pages_processed": 0,
            "extraction_time": "0.0s",
            "ocr_time": "0.0s",
            "nlp_time": "0.0s",
            "total_time": "0.0s",
            "memory_est_mb": 0.0
        },
        "dashboard": dashboard or {
            "risk_meter": 0,
            "heat_score": 0,
            "priority_color": "gray",
            "urgency_badge": "Unknown",
            "tags": [],
            "deadline_alerts": [],
            "summary_cards": [],
            "timeline": [],
            "voice_narration": "Summary unavailable.",
            "ai_reasoning": "Data processing unavailable.",
            "appeal_recommended": False,
            "appeal_suggestion": "Not Recommended",
            "recommended_actions": [],
            "decision_reasoning": [],
            "decision_intelligence": {
                "case_number": "",
                "recommended_actions": [],
                "priority_level": "Unknown",
                "risk_level": "Unknown",
                "appeal_suggestion": "Not Recommended",
                "reasoning": []
            }
        },
        "data": data or {},
        "errors": errors or []
    }
