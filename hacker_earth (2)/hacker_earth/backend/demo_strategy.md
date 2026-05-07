# NyayaMitra: Demo Strategy & Brand Metadata

## 🚀 Brand Identity
* **Project Name:** NyayaMitra
* **Tagline:** Explainable Legal Intelligence.
* **Elevator Pitch:** "NyayaMitra is a hybrid-AI pipeline that instantly transforms dense, unstructured court PDFs into highly-actionable, explainable executive dashboards, ensuring citizens and lawyers never miss a critical compliance deadline."
* **Mission:** To democratize legal comprehension through transparent, resilient technology.

## 🧠 Technical Buzzwords (To use during pitch)
* **Backend-For-Frontend (BFF) Pattern** (Shows architectural maturity)
* **Heuristic Scoring Engine** (Sounds better than "if/else statements")
* **Explainable AI (XAI) / Reasoning Trace** (Highly prized by enterprise/gov judges)
* **Graceful Degradation** (Explaining how OCR fallback works)
* **Deterministic Fallbacks** (Explaining why the API never crashes)

## ⚠️ Demo Survival Strategy

### 1. The Environment Setup
* **Command to run:** `$env:DEMO_MODE="true"; python -m uvicorn app:app --host 127.0.0.1 --port 8000`
* **Why?** `DEMO_MODE` automatically disables the heavy PaddleOCR engine. If you are presenting on a laptop while running Zoom, Chrome, and the UI, running a heavy ML model can freeze your computer. `DEMO_MODE` ensures lightning-fast NLP extraction.

### 2. The PDF Selection
* **DO USE:** A clean, digital, text-selectable PDF (like a recent High Court order downloaded directly from a court website).
* **DO NOT USE:** A blurry, crooked, 10-year-old scanned document. While the OCR *can* handle it, it takes 15-30 seconds, which feels like an eternity during a 3-minute pitch.

### 3. The Swagger "Flex"
* Have `http://localhost:8000/docs` open in a background tab. 
* If the judges ask a deep technical question, switch to the Swagger tab, hit the `/demo-test` endpoint, and walk them through the pristine JSON response. 
* Point out the `ui_alerts` and the `reasoning_trace` arrays. This proves that your backend is incredibly robust and not just a thin wrapper around a basic script.
