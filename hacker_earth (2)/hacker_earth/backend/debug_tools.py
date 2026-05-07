import time
import uuid
import json
from functools import wraps
from loguru import logger
from fastapi.responses import JSONResponse

def trace_request(func):
    """
    Decorator to add detailed timing and request tracing.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        req_id = str(uuid.uuid4())
        start_time = time.time()
        logger.info(f"[TRACE START] {func.__name__} | ReqID: {req_id}")
        
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"[TRACE END] {func.__name__} | ReqID: {req_id} | Duration: {duration:.4f}s | Status: Success")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"[TRACE ERROR] {func.__name__} | ReqID: {req_id} | Duration: {duration:.4f}s | Error: {e}")
            raise
    return wrapper

def validate_schema(response_dict: dict) -> bool:
    """
    Validates that a response dictionary adheres strictly to the NyayaMitra normalized schema.
    """
    required_keys = {"status", "request_id", "processing_mode", "analytics", "dashboard", "data", "errors"}
    missing = required_keys - set(response_dict.keys())
    if missing:
        logger.warning(f"Schema Validation Failed. Missing keys: {missing}")
        return False
    return True

def generate_mock_success() -> dict:
    """
    Utility to quickly generate a flawless mock response for testing.
    """
    from response_formatter import normalize_response
    from frontend_adapter import adapt_for_frontend
    
    dash = {
        "risk_meter": 75, "heat_score": 88, "priority_color": "orange",
        "urgency_badge": "High", "tags": ["Labor", "Compensation"],
        "deadline_alerts": [{"raw": "within 14 days", "normalized_days": 14}],
        "summary_cards": ["ORDER: Pay the arrears within 14 days."],
        "timeline": [{"date": "10th October 2023", "event": "Order issued"}],
        "voice_narration": "Labor dispute with a 14-day compliance order.",
        "ai_reasoning": "High urgency due to strict financial compliance deadline.",
        "appeal_recommended": False
    }
    data = {"case_number": {"value": "L.D. 123", "confidence": 0.99}}
    
    resp = normalize_response("success", "mock", dashboard=dash, data=data)
    resp["frontend_adapted"] = adapt_for_frontend(dash, data)
    return resp
