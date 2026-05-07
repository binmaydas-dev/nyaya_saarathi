import os
import time
import uuid
import hashlib
import psutil
import re
from collections import OrderedDict
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from loguru import logger

from extract_pdf import extract_text_and_detect_scan
from ocr import perform_ocr
from preprocess import clean_text
from extractor import extract_legal_information
from classifier import classify_clauses
from summary import generate_summary, generate_voice_narration, generate_executive_report
from insights import analyze_insights
from errors import NyayaMitraException, custom_exception_handler, generic_exception_handler, FileTooLargeError, UnsupportedFileError, PDFProcessingError
from response_formatter import normalize_response
from frontend_adapter import adapt_for_frontend

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

RESULTS_CACHE = OrderedDict()
HASH_CACHE = {}  
CACHE_TIMESTAMPS = {}
MAX_CACHE_ITEMS = int(os.getenv("MAX_CACHE_ITEMS", "50"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
MAX_FILE_SIZE = 10 * 1024 * 1024 

LIGHT_MODE = os.getenv("LIGHT_MODE", "false").lower() == "true"
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

# Fallback: If DEMO_MODE is true, LIGHT_MODE is implicitly true to save memory during pitch
if DEMO_MODE:
    LIGHT_MODE = True

def log_startup_status():
    logger.info("==============================================")
    logger.info("🚀 INITIALIZING NYAYAMITRA AI BACKEND 🚀")
    logger.info("==============================================")

    for folder in [UPLOAD_DIR, OUTPUT_DIR]:
        if os.path.exists(folder):
            logger.info(f"✅ Directory validated: {folder}")
        else:
            logger.warning(f"⚠️ Directory missing: {folder}")

    logger.info(f"⚙️  LIGHT_MODE: {'ACTIVE (Fast NLP)' if LIGHT_MODE else 'INACTIVE (Full Pipeline)'}")
    logger.info(f"🎯 DEMO_MODE : {'ACTIVE (Presentation Safe)' if DEMO_MODE else 'INACTIVE'}")

    try:
        import spacy
        spacy.load("en_core_web_sm")
        logger.info("✅ NLP Engine: spaCy 'en_core_web_sm' loaded successfully.")
    except Exception:
        logger.warning("⚠️ NLP Engine: spaCy model missing. Will use regex fallback. (Run 'python -m spacy download en_core_web_sm')")

    logger.info("==============================================")
    logger.info("✅ BACKEND READY FOR HACKATHON PRESENTATION ✅")
    logger.info("==============================================")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log_startup_status()
    yield


app = FastAPI(
    title="NyayaMitra API - Final Presentation Ready",
    description="Intelligent AI/NLP legal document processing with absolute stability.",
    version="4.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(NyayaMitraException, custom_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

def safe_int(val, fallback=0):
    try:
        if val is None: return fallback
        return int(val)
    except (ValueError, TypeError):
        return fallback

def safe_str(val, fallback=""):
    try:
        if val is None: return fallback
        return str(val)
    except Exception:
        return fallback

def safe_list(val):
    if isinstance(val, list): return val
    return []

def safe_dict(val):
    if isinstance(val, dict): return val
    return {}

def attach_decision_dashboard_fields(dashboard: dict, insights: dict) -> dict:
    dashboard["recommended_actions"] = safe_list(safe_dict(insights).get("recommended_actions"))
    dashboard["appeal_suggestion"] = safe_str(safe_dict(insights).get("appeal_suggestion"), fallback="Not Recommended")
    dashboard["decision_reasoning"] = safe_list(safe_dict(insights).get("reasoning_items"))
    dashboard["decision_intelligence"] = safe_dict(safe_dict(insights).get("decision_intelligence"))
    return dashboard

def prune_cache():
    now = time.time()

    for cache_id, cached_at in list(CACHE_TIMESTAMPS.items()):
        if now - cached_at > CACHE_TTL_SECONDS:
            RESULTS_CACHE.pop(cache_id, None)
            CACHE_TIMESTAMPS.pop(cache_id, None)
            for file_hash, request_id in list(HASH_CACHE.items()):
                if request_id == cache_id:
                    HASH_CACHE.pop(file_hash, None)

    while len(RESULTS_CACHE) > MAX_CACHE_ITEMS:
        oldest_id, _ = RESULTS_CACHE.popitem(last=False)
        CACHE_TIMESTAMPS.pop(oldest_id, None)
        for file_hash, request_id in list(HASH_CACHE.items()):
            if request_id == oldest_id:
                HASH_CACHE.pop(file_hash, None)


def cache_result(request_id: str, response: dict, file_hash: str = None):
    prune_cache()
    RESULTS_CACHE[request_id] = response
    RESULTS_CACHE.move_to_end(request_id)
    CACHE_TIMESTAMPS[request_id] = time.time()
    if file_hash:
        HASH_CACHE[file_hash] = request_id
    prune_cache()


def get_cached_result(request_id: str):
    prune_cache()
    cached = RESULTS_CACHE.get(request_id)
    if cached is not None:
        RESULTS_CACHE.move_to_end(request_id)
    return cached

class ExtractionResponse(BaseModel):
    request_id: str
    status: str
    processing_mode: str
    analytics: dict
    dashboard: dict
    data: dict
    errors: list
    frontend_adapted: dict = Field(None, description="Flattened keys for frontend integration")

# --- HEALTH AND METRICS ---

@app.get("/health")
def health_check():
    return normalize_response(status="success", processing_mode="healthcheck", data={"service": "nyayamitra-backend", "status": "ok", "light_mode": LIGHT_MODE})

@app.get("/")
def read_root():
    return {"message": "Welcome to NyayaMitra API", "status": "ok"}

@app.get("/version")
def version_info():
    return normalize_response(status="success", processing_mode="version", data={"version": app.version, "environment": os.getenv("ENVIRONMENT", "development")})

@app.get("/metrics")
def system_metrics():
    prune_cache()
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return normalize_response(status="success", processing_mode="metrics", data={
        "memory_usage_mb": round(memory_info.rss / (1024 * 1024), 2),
        "cpu_percent": process.cpu_percent(),
        "total_requests_cached": len(RESULTS_CACHE),
        "max_cache_items": MAX_CACHE_ITEMS,
        "cache_ttl_seconds": CACHE_TTL_SECONDS
    })

@app.get("/demo-test")
def demo_test_route():
    """Returns a highly polished, pre-computed rich response instantly for judges."""
    logger.info("Serving /demo-test route for presentation.")
    demo_dashboard = {
        "risk_meter": 85,
        "heat_score": 92,
        "priority_color": "danger",
        "urgency_badge": "Critical",
        "tags": ["Land Dispute", "Compensation"],
        "deadline_alerts": [{"raw": "within two weeks", "normalized_days": 14, "context": "The respondent is directed to vacate within two weeks."}],
        "summary_cards": [
            "INTERPRETATION: The court has issued a final order regarding property possession.",
            "EXPLANATION: The legal text details the proceedings of the petitioner's claim.",
            "ACTIONABLE OUTCOME: Immediate compliance is required within 14 days.",
            "NEXT STEP: Consult legal counsel to file necessary compliance documents."
        ],
        "timeline": [{"date": "15th June 2023", "event": "Order/Direction issued"}],
        "voice_narration": "This case involves a Land Dispute. The court has issued an order requiring compliance within two weeks.",
        "ai_reasoning": "Urgency marked Critical due to mandatory compliance language and short deadline.",
        "appeal_recommended": True,
        "appeal_suggestion": "Appeal Recommended",
        "recommended_actions": [
            {
                "action": "Release compensation amount",
                "department": "Revenue Department",
                "priority": "Critical",
                "risk_level": "Critical",
                "deadline": "within two weeks"
            }
        ],
        "decision_reasoning": [
            "Detected compensation directive",
            "Detected mandatory deadline",
            "Detected mandatory court language"
        ],
        "decision_intelligence": {
            "case_number": "W.P.(C) DEMO/2026",
            "recommended_actions": [
                {
                    "action": "Release compensation amount",
                    "department": "Revenue Department",
                    "priority": "Critical",
                    "risk_level": "Critical",
                    "deadline": "within two weeks"
                }
            ],
            "priority_level": "Critical",
            "risk_level": "Critical",
            "appeal_suggestion": "Appeal Recommended",
            "reasoning": [
                "Detected compensation directive",
                "Detected mandatory deadline",
                "Detected mandatory court language"
            ]
        },
        "probable_case_category": "Land Dispute",
        "compliance_probability": "Medium",
        "escalation_risk": "High",
        "public_impact_score": 85,
        "procedural_complexity": "High",
        "ai_confidence_score": 96,
        "extraction_quality": "High",
        "reasoning_trace": [
            "Detected critical legal keywords.",
            "Calculated base risk score of 85 using heuristic scaling.",
            "Analyzed deadlines to infer an urgency level of Critical."
        ],
        "model_decision_basis": "Heuristic NLP aggregation based on explicit mandatory language extraction.",
        "alerts": [{"severity": "Critical", "message": "Immediate compliance required within 14 days", "color": "danger"}],
        "executive_report": {
            "case_overview": "This AI-generated report outlines a legal proceeding requiring professional review.",
            "primary_issue": "Land Dispute",
            "court_direction": "The respondent is directed to vacate the premises within two weeks...",
            "risk_assessment": "High risk detected due to severe language and short deadlines.",
            "recommended_next_step": "Ensure the legal team reviews all noted deadlines."
        }
    }
    
    response = normalize_response(
        status="success",
        request_id="demo-pitch-001",
        processing_mode="demo_test",
        analytics={
            "pages_processed": 1, "extraction_time": "0.01s", "ocr_time": "0.00s",
            "nlp_time": "0.02s", "total_time": "0.03s", "memory_est_mb": 120.5
        },
        dashboard=demo_dashboard,
        data={"case_number": {"value": "W.P.(C) DEMO/2026", "confidence": 0.99}},
        errors=[]
    )
    response["frontend_adapted"] = adapt_for_frontend(demo_dashboard, response["data"])
    return JSONResponse(content=response)

# --- MAIN UPLOAD PIPELINE ---

@app.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    mock_mode: bool = Query(False, description="Enable instant mock processing for flawless demoing"),
    demo_mode: bool = Query(False, description="Alias for mock processing during demos"),
    lang: str = Query('en', description="OCR Language (e.g., 'en', 'hi')")
):
    total_start = time.time()
    req_id = str(uuid.uuid4())
    req_logger = logger.bind(request_id=req_id)
    pipeline_errors = []
    mock_mode = mock_mode or demo_mode
    
    req_logger.info(f"Received file: {file.filename} | LIGHT_MODE: {LIGHT_MODE}")
    
    # 1. Validation & Hashing
    if not file.filename.lower().endswith('.pdf'):
        raise UnsupportedFileError()
        
    content = await file.read()
    file_size = len(content)
    if file_size > MAX_FILE_SIZE:
        raise FileTooLargeError()
        
    file_hash = hashlib.sha256(content).hexdigest()
    
    # 2. Cache Check
    if file_hash in HASH_CACHE and not mock_mode:
        req_logger.info("Cache hit! Returning pre-processed result.")
        cached_id = HASH_CACHE[file_hash]
        cached_response = get_cached_result(cached_id)
        if cached_response is not None:
            return JSONResponse(content=cached_response)
        HASH_CACHE.pop(file_hash, None)

    # 3. Mock Mode Fast-Path
    if mock_mode:
        req_logger.info("MOCK MODE activated. Returning guaranteed perfect response.")
        mock_text = (
            "W.P.(C) 1234/2023. The respondent is directed to pay compensation "
            "and submit a compliance report within 30 days."
        )
        mock_extracted = {
            "case_number": {"value": "W.P.(C) 1234/2023", "confidence": 0.99},
            "deadlines": [{"raw": "within 30 days", "normalized_days": 30, "context": mock_text}],
            "important_clauses": [{"text": mock_text, "start": 0, "end": len(mock_text)}],
            "classified_clauses": {"orders": [{"text": mock_text, "start": 0, "end": len(mock_text)}]}
        }
        insights = analyze_insights(mock_text, mock_extracted)
        summary_points = [
            "ORDER: Compensation and compliance reporting obligations were detected.",
            "ACTIONABLE OUTCOME: Department-level follow-up is required within 30 days."
        ]
        voice_narration = "The court direction requires compensation processing and compliance reporting within 30 days."
        mock_dashboard = attach_decision_dashboard_fields({

                "risk_meter": int(
                    insights.get("risk_score") or 0
                ),

                "heat_score": int(
                    insights.get("heat_score") or 0
                ),

                "priority_color": (
                    insights.get("priority_color")
                    or "gray"
                ),

                "urgency_badge": (
                    insights.get("urgency")
                    or "Unknown"
                ),

                "tags": (
                    insights.get("tags")
                    or []
                ),

                "deadline_alerts": (
                    mock_extracted.get("deadlines")
                    or []
                ),

                "summary_cards": (
                    summary_points
                    if isinstance(summary_points, list)
                    else []
                ),

                "timeline": [],

                "voice_narration": (
                    voice_narration
                    or "Summary unavailable."
                ),

                "ai_reasoning": (
                    insights.get("reasoning")
                    or "No reasoning available."
                ),

                "appeal_recommended": bool(
                    insights.get("appeal_recommended")
                    or False
                )
        }, insights)
        demo_response = normalize_response(
            status="success",
            request_id=req_id,
            processing_mode="mock_demo",
            analytics={
                "pages_processed": 1, "extraction_time": "0.01s", "ocr_time": "0.00s",
                "nlp_time": "0.05s", "total_time": "0.06s", "memory_est_mb": 150.5
            },
            dashboard=mock_dashboard,
            data=mock_extracted
        )
        demo_response["frontend_adapted"] = adapt_for_frontend(demo_response["dashboard"], demo_response["data"])
        return JSONResponse(content=demo_response)

    # 4. Standard Processing
    file_path = os.path.join(UPLOAD_DIR, f"{req_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(content)
        
    try:
        # Phase A: Extraction
        ext_start = time.time()
        ext_result = extract_text_and_detect_scan(file_path)
        raw_text = ext_result[0]
        is_scanned = ext_result[1]
        num_pages = ext_result[2] if len(ext_result) > 2 else (len(raw_text) // 2000 + 1)
        ext_time = time.time() - ext_start
        
        processing_mode = "text_extraction"
        ocr_time = 0.0
        ocr_conf = None
        
        # Phase B: OCR (Fallback)
        if is_scanned and not LIGHT_MODE:
            processing_mode = "ocr"
            req_logger.info("Initiating OCR fallback...")
            try:
                ocr_start = time.time()
                raw_text, ocr_conf = perform_ocr(file_path, lang=lang)
                ocr_time = time.time() - ocr_start
                if not raw_text.strip():
                    raise ValueError("OCR returned empty text.")
            except Exception as e:
                pipeline_errors.append(f"OCR gracefully failed: {e}")
                raw_text = "Text extraction failed during OCR fallback. Document may be unreadable."
                req_logger.warning(f"OCR skipped/failed: {e}")
        elif is_scanned and LIGHT_MODE:
            processing_mode = "scanned_light_mode"
            pipeline_errors.append("Scanned/image-based PDF detected. OCR skipped because LIGHT_MODE/DEMO_MODE is active.")
            if not raw_text.strip():
                raw_text = "Scanned PDF detected. OCR skipped in demo light mode."
            req_logger.warning("Scanned PDF detected, but OCR skipped in LIGHT_MODE.")

        # Phase C & D: NLP Pipeline (Wrapped for Safety)
        nlp_start = time.time()
        cleaned_text = clean_text(raw_text)
        
        try:
            extracted_data = extract_legal_information(cleaned_text)
        except Exception as e:
            pipeline_errors.append(f"Extraction Error: {e}")
            extracted_data = {"important_clauses": []}
            
        try:
            classified_clauses = classify_clauses(extracted_data.get("important_clauses", []))
            extracted_data["classified_clauses"] = classified_clauses
            extracted_data["orders"] = classified_clauses["orders"]
        except Exception as e:
            pipeline_errors.append(f"Classification Error: {e}")
            classified_clauses = {"orders": [], "observations": [], "suggestions": []}

        try:
            insights = analyze_insights(cleaned_text, extracted_data)
            summary_bullets = [] if LIGHT_MODE else generate_summary(cleaned_text, classified_clauses)
            voice_narration = "" if LIGHT_MODE else generate_voice_narration(extracted_data, insights)
            executive_report = {} if LIGHT_MODE else generate_executive_report(cleaned_text, classified_clauses, insights)
        except Exception as e:
            pipeline_errors.append(f"Insights Error: {e}")
            insights = {"risk_score": 0, "heat_score": 0, "priority_color": "gray", "urgency": "Unknown", "tags": [], "reasoning": "Failed", "appeal_recommended": False}
            summary_bullets = ["Summary unavailable due to processing error."]
            voice_narration = "Summary unavailable."
            executive_report = {"case_overview": "Failed to generate report."}

        nlp_time = time.time() - nlp_start
        total_time = time.time() - total_start

        analytics = {
            "pages_processed": num_pages,
            "extraction_time": f"{ext_time:.2f}s",
            "ocr_time": f"{ocr_time:.2f}s",
            "ocr_confidence": round(ocr_conf if ocr_conf is not None else 0.0, 2),
            "nlp_time": f"{nlp_time:.2f}s",
            "total_time": f"{total_time:.2f}s",
            "memory_est_mb": round(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024), 2)
        }
        
        dashboard = attach_decision_dashboard_fields({
            "risk_meter": safe_int(safe_dict(insights).get("risk_score")),
            "heat_score": safe_int(safe_dict(insights).get("heat_score")),
            "priority_color": safe_str(safe_dict(insights).get("priority_color"), fallback="gray"),
            "urgency_badge": safe_str(safe_dict(insights).get("urgency"), fallback="Unknown"),
            "tags": safe_list(safe_dict(insights).get("tags")),
            "deadline_alerts": safe_list(safe_dict(extracted_data).get("deadlines")),
            "summary_cards": safe_list(summary_bullets),
            "timeline": safe_list(safe_dict(extracted_data).get("timeline")),
            "voice_narration": safe_str(voice_narration, fallback="Summary unavailable."),
            "ai_reasoning": safe_str(safe_dict(insights).get("reasoning"), fallback="No reasoning available."),
            "appeal_recommended": bool(safe_dict(insights).get("appeal_recommended", False)),
            "severity": safe_str(safe_dict(insights).get("severity"), fallback="Unknown"),
            "compliance_urgency": safe_str(safe_dict(insights).get("compliance_urgency"), fallback="Unknown"),
            "authority_involved": safe_str(safe_dict(insights).get("authority_involved"), fallback="Unknown"),
            "legal_impact": safe_str(safe_dict(insights).get("legal_impact"), fallback="Unknown"),
            "citizen_impact": safe_str(safe_dict(insights).get("citizen_impact"), fallback="Unknown"),
            "recommended_action": safe_str(safe_dict(insights).get("recommended_action"), fallback="Unknown"),
            "possible_consequences": safe_str(safe_dict(insights).get("possible_consequences"), fallback="Unknown"),
            "probable_case_category": safe_str(safe_dict(insights).get("probable_case_category"), fallback="Unknown"),
            "compliance_probability": safe_str(safe_dict(insights).get("compliance_probability"), fallback="Unknown"),
            "escalation_risk": safe_str(safe_dict(insights).get("escalation_risk"), fallback="Unknown"),
            "public_impact_score": safe_int(safe_dict(insights).get("public_impact_score")),
            "procedural_complexity": safe_str(safe_dict(insights).get("procedural_complexity"), fallback="Unknown"),
            "ai_confidence_score": safe_int(safe_dict(insights).get("ai_confidence_score")),
            "extraction_quality": safe_str(safe_dict(insights).get("extraction_quality"), fallback="Unknown"),
            "reasoning_trace": safe_list(safe_dict(insights).get("reasoning_trace")),
            "model_decision_basis": safe_str(safe_dict(insights).get("model_decision_basis"), fallback="Unknown"),
            "alerts": safe_list(safe_dict(insights).get("alerts")),
            "executive_report": safe_dict(executive_report)
        }, insights)
        
        req_logger.info(f"--- TRACE LOG ---")
        req_logger.info(f"Extracted Data Keys: {list(safe_dict(extracted_data).keys())}")
        req_logger.info(f"Insights Output: {safe_dict(insights)}")
        req_logger.info(f"Dashboard Generated Successfully.")
        req_logger.info(f"-----------------")
        
        status_val = "success" if not pipeline_errors else "partial"
        
        response = normalize_response(
            status=status_val,
            request_id=req_id,
            processing_mode=processing_mode,
            analytics=analytics,
            dashboard=dashboard,
            data=extracted_data,
            errors=pipeline_errors
        )
        response["frontend_adapted"] = adapt_for_frontend(dashboard, extracted_data)
        
        if not mock_mode:
            cache_result(req_id, response, file_hash=file_hash)
            
        req_logger.info(f"Pipeline complete in {total_time:.2f}s with {len(pipeline_errors)} errors.")
        return JSONResponse(content=response)
        
    except Exception as e:
        req_logger.error(f"Catastrophic error: {e}")
        err_resp = normalize_response("error", "failed", errors=[str(e)], request_id=req_id)
        return JSONResponse(content=err_resp, status_code=500)
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as cleanup_error:
            req_logger.warning(f"Temporary upload cleanup failed: {cleanup_error}")

@app.get("/export/{export_id}")
async def export_results(export_id: str, export_format: str = Query('json', alias="format", description="Format: 'json' or 'txt'")):
    if not re.match(r'^[a-zA-Z0-9_-]+$', export_id):
        raise HTTPException(status_code=400, detail="Invalid export ID format.")
        
    data = get_cached_result(export_id)

    if data is None:
        raise HTTPException(status_code=404, detail="Result ID not found or expired.")
    
    if export_format == 'json':
        return JSONResponse(content=data)
    elif export_format == 'txt':
        txt_content = f"NYAYAMITRA LEGAL SUMMARY\n========================\n\n"
        txt_content += f"URGENCY: {data['dashboard']['urgency_badge']} | RISK SCORE: {data['dashboard']['risk_meter']}/100\n"
        
        safe_tags = safe_list(data['dashboard'].get('tags'))
        txt_content += f"TAGS: {', '.join(safe_tags)}\n\n"
        
        txt_content += "SUMMARY:\n"
        for bullet in data['dashboard']['summary_cards']:
            txt_content += f"- {bullet}\n"
        txt_content += f"\nNARRATION:\n{data['dashboard']['voice_narration']}\n"
        
        file_path = os.path.join(OUTPUT_DIR, f"{export_id}.txt")
        with open(file_path, "w") as f:
            f.write(txt_content)
        return FileResponse(path=file_path, filename=f"summary_{export_id}.txt", media_type='text/plain')
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Choose 'json' or 'txt'.")
