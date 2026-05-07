# NyayaMitra AI Legal Backend

NyayaMitra is an intelligent, high-performance legal document analysis engine built for hackathon and startup pitch demonstrations. It uses advanced NLP, Heuristic Intelligence, and OCR fallbacks to ingest messy legal documents and output highly-polished, premium JSON payloads for frontend consumption.

## 🚀 Features
- **Smart Legal Summarization**: Extracts the Core Issue, Actionable Outcome, and Next Steps.
- **AI Heat & Risk Scoring**: Heuristic scoring for compliance urgency and escalation risk.
- **Automated Timelines & Deadlines**: Extracts chronological legal events and normalizes compliance deadlines.
- **Intelligent Fallbacks**: Never crashes. Gracefully degrades to partial JSON outputs if OCR or NLP models fail on blurry PDFs.
- **Frontend-Ready Payload**: The `frontend_adapted` output completely flattens complex nested AI models into UI-ready dictionaries with pre-calculated colors (`danger`, `warning`) and formatted strings.

---

## 🛠️ Tech Stack
- **FastAPI / Uvicorn** (High-performance Async Python)
- **spaCy (`en_core_web_sm`)** (Entity and date extraction)
- **PaddleOCR** (Intelligent OCR fallback for scanned PDFs)
- **PyMuPDF** (Primary high-speed PDF text extraction)
- **Loguru** (Premium startup & trace logging)

---

## ⚙️ How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Start the Server
```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Demo Safe Mode (Recommended for Live Pitching)
To ensure absolute presentation safety (disables heavy OCR memory usage and ensures zero latency):
```bash
# Windows (PowerShell)
$env:DEMO_MODE="true"
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

---

## 🔗 API Endpoints

### `GET /demo-test`
**Perfect for judging.** Returns an instant, pre-calculated, pristine premium payload showing off the absolute best of the AI intelligence without actually processing a file.

### `POST /upload`
**The Core Engine.** 
- **Body**: `multipart/form-data` with a `file` field (.pdf).
- **Query Params**: 
  - `mock_mode=true` (Force 0-latency perfect response for live demos).
  - `lang=en` (OCR Language fallback).

### `GET /health`
Validates that the server and environment variables are active.

### `GET /metrics`
Returns current CPU/Memory usage and the number of cached PDF results.

---

## 📸 Screenshots
*(Insert UI Screenshots here during final presentation polish)*
- [Architecture Diagram]
- [Dashboard Render]
- [Alerts Panel Render]

---

## 🛠️ Team Roles
- **Backend AI Engineer**: Architected the FastAPI extraction and intelligence scoring engines.
- **Frontend Developer**: Consumes the `frontend_adapted` object for the React/Vue interface.
- **Domain Expert**: Tuned the heuristic NLP keywords (e.g. "forthwith", "mandatory").

---

## 🛑 Troubleshooting
- **"ModuleNotFoundError: No module named 'spacy'"**: Run `pip install spacy && python -m spacy download en_core_web_sm`.
- **"Out of Memory / OCR Crash"**: Ensure `LIGHT_MODE=true` or `DEMO_MODE=true` is set to skip PaddleOCR on weak laptops.
- **"Expected ',', found name"**: If you manually edit `app.py` dictionaries, ensure strict Python JSON/Dict formatting.
