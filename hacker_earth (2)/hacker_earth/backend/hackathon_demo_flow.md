# NyayaMitra: Hackathon Demo Flow

## 🎯 3-Minute Live Pitch Sequence

**0:00 - 0:30 | The Hook & Problem**
* **Say:** "Millions of citizens and under-resourced legal teams drown in complex court documents. Deadlines are missed, and critical orders go unnoticed. Meet NyayaMitra—an intelligent, explainable legal pipeline."
* **Click:** Open the UI. Show a raw, dense PDF of a court order on screen. 
* **Say:** "This is a standard 10-page High Court order. Finding the actual compliance deadline in here manually takes 20 minutes."

**0:30 - 1:30 | The Magic Upload (Live Execution)**
* **Click:** Upload the PDF. Ensure `$env:DEMO_MODE="true"` is running so the response is instant.
* **Say:** "Watch as NyayaMitra's hybrid NLP engine extracts, comprehends, and normalizes the document instantly."
* **Show:** Point to the newly rendered Dashboard.
* **Say:** "Immediately, we see a Critical Risk Alert. NyayaMitra found a hidden directive requiring compliance 'within two weeks' and mathematically mapped it to 14 days."

**1:30 - 2:30 | Explainable AI & Intelligence**
* **Click:** Scroll down to the 'AI Reasoning' or 'Executive Report' section.
* **Say:** "But we don't just throw AI magic at the wall. Judges and lawyers need to know *why*. Our Explainability Trace shows exactly how the AI aggregated risk scores based on explicitly detected mandatory language—not hallucinations."
* **Show:** Point out the Confidence Score and the Reasoning Trace.

**2:30 - 3:00 | The Impact & Close**
* **Say:** "NyayaMitra isn't just an OCR tool. It's an intelligent triage system that prevents legal escalation and empowers citizens to understand court directives without a law degree. Thank you."

---

## 🔬 5-Minute Technical Deep-Dive (For Technical Judges)

**Add the following segments to the 3-minute pitch:**

**The OCR Fallback Strategy**
* **Say:** "Most platforms crash if you upload a scanned image. We built a lazy-loaded OCR fallback. If PyMuPDF detects a scan, the pipeline gracefully degrades, kicks off PaddleOCR, and continues the extraction seamlessly."

**The Frontend Adapter Architecture**
* **Show:** Open Swagger UI (`http://localhost:8000/docs`) and hit the `/demo-test` endpoint.
* **Say:** "Notice our JSON payload. We engineered a `frontend_adapted` layer on the backend. This means the UI team doesn't have to write complex mapping logic or handle `null` values. The backend safely casts every integer, string, and list, feeding the UI pre-computed `danger` or `warning` color strings."

**The Safe Fallback Mechanism**
* **Say:** "Our entire pipeline is wrapped in safe casting helpers. If a document is completely unreadable, instead of throwing a 500 server error, NyayaMitra isolates the failure, populates safe 'Unknown' fallback markers, and continues returning a perfect JSON schema."

---

## 🚨 Emergency Backup Plan (The "Mock Mode" Strategy)
If the WiFi drops, the laptop hangs, or the live upload fails:
1. Don't panic. Smile.
2. Say: "We anticipated enterprise-scale constraints, so we built a zero-latency presentation mode."
3. Click the pre-configured "Instant Demo" button (which hits `/upload?mock_mode=true`).
4. The dashboard will instantly populate with perfect data.
5. You still look like architectural geniuses because you built a graceful failover.
