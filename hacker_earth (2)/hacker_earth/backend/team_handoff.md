# NyayaMitra Team Handoff

## 🏗 Architecture Summary
NyayaMitra is a FastAPI-driven Python backend. It utilizes a hybrid NLP approach:
1. **PyMuPDF (`fitz`)** for rapid text ripping and scan-detection.
2. **PaddleOCR** for robust, multilingual fallback on image-based PDFs.
3. **spaCy & Regex Heuristics** for instantaneous entity, date, and deadline extraction without the cost or latency of an LLM.

## 📂 Key Files to Know
- `app.py`: The brain. Contains routes, caching, and orchestration.
- `response_formatter.py` & `frontend_adapter.py`: Your safety nets. They guarantee the JSON schema never changes and the React frontend never crashes.
- `insights.py`: The secret sauce. Contains the logic for Risk Scores, Urgency Badges, and Smart Tagging.
- `generate_samples.py`: Run this before the demo to generate fresh mock PDFs.

## 🚀 Deployment Commands
**Local Testing:**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
**Docker (Production):**
```bash
docker-compose up --build -d
```

## ⚠️ Demo Precautions & Troubleshooting
1. **The "Weak Laptop" Problem:** PaddleOCR takes ~1GB of RAM. If you present on a laptop with 4GB RAM, the OS might kill the process. 
   - **Solution:** Set `LIGHT_MODE=true` in your `.env` file before pitching.
2. **The "Wifi is down" Problem:** 
   - **Solution:** Add `?mock_mode=true` to your upload request. It skips processing and returns cached JSON instantly. You will look like a wizard.
3. **Dependencies Missing:** Always use the locked file: `pip install -r requirements-lock.txt`.

## Frontend Integration
Have the frontend team read `frontend_integration.md`. They should bind their state directly to the `frontend_adapted` JSON block.

Good luck team! Build an amazing dashboard and win this hackathon!
