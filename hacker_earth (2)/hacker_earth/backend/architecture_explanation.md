# NyayaMitra: System Architecture Explanation

Use this document to explain the backend pipeline to technical judges, mentors, and recruiters.

## 1. Ingestion & Validation Layer
**What it does:** Receives the PDF, validates the file size and type, and generates an MD5 hash.
**The Smart Part:** We implemented an instant Cache-Hit system. If the exact same PDF is uploaded twice, the pipeline bypasses processing entirely and returns the pre-computed JSON in 0.01 seconds.

## 2. Extraction & Fallback Layer
**What it does:** Attempts to pull raw text using `PyMuPDF`. 
**The Smart Part:** We built a scan-detection heuristic. If the PDF contains zero parseable text, the system seamlessly redirects the file to our `PaddleOCR` fallback module to process the scanned images. 

## 3. NLP Intelligence Engine
**What it does:** Cleans the text and runs it through `spaCy` (`en_core_web_sm`) to extract named entities (Dates, Petitioners, Respondents).
**The Smart Part:** It uses advanced Regex heuristics to capture dynamic legal deadlines (e.g., "immediate effect", "within 3 weeks") and mathematically normalizes them into usable integer days for calendar systems.

## 4. AI Insights & Heuristics Core
**What it does:** Calculates the `risk_score`, `heat_score`, and `urgency`.
**The Smart Part:** It doesn't rely on expensive, slow, external LLM calls. It aggregates scores based on the density of mandatory legal language (e.g., "shall", "forthwith", "penalty"). It then generates an **Explainability Trace** to prove to the user exactly how it reached its conclusion.

## 5. The "Frontend Adapter" (BFF Pattern)
**What it does:** Takes the complex nested Python dictionaries and flattens them into a `frontend_adapted` payload.
**The Smart Part:** It prevents the frontend React/Vue app from crashing. It uses bulletproof `.get()`, `int()`, and `str()` casting to ensure that even if the AI fails to extract a deadline, the UI simply receives `"days": "N/A"` instead of a `NullReferenceException`. It also pre-computes UI colors (e.g., `danger`, `warning`).

## 6. Global Safety Nets
**What it does:** Prevents 500 Internal Server Errors.
**The Smart Part:** Every single phase (Extraction, OCR, NLP, Insights) is wrapped in isolated `try/except` blocks. If one module fails, the pipeline logs the error into an `errors[]` array, applies safe default values, and continues executing. The API guarantees a `200 OK` response with a consistent JSON schema.
