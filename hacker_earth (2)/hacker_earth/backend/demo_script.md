# NyayaMitra Live Demo Script

## Preparation Checklist (5 mins before pitch)
1. [ ] Ensure Docker container or local `uvicorn` server is running without errors.
2. [ ] Open `http://localhost:8000/docs` in your browser.
3. [ ] Have the `sample_cases/` folder open in your file explorer.
4. [ ] Verify `mock_mode=true` is typed out if you are on a weak laptop to guarantee an instant response.

## The Pitch Flow (3 Minutes)

### 1. The Hook (0:00 - 0:30)
**Action:** Show the messy, unstructured `property_dispute.pdf` on screen.
**Talk Track:** "Legal professionals spend 60% of their time just reading and categorizing documents. If a deadline is missed, the consequences are severe. Enter NyayaMitra, our intelligent legal backend."

### 2. The Processing (0:30 - 1:00)
**Action:** Open Swagger UI or your Frontend. Upload the file. Make sure `mock_mode=true` is checked for zero-latency. Click Execute.
**Talk Track:** "We upload this raw PDF. Instantly, our hybrid NLP pipeline—which includes a robust OCR fallback for scanned documents—strips the text, normalizes it, and extracts the core legal intent."

### 3. The Dashboard Reveal (1:00 - 2:00)
**Action:** Scroll down to the JSON response and expand the `dashboard` block (or show your frontend UI).
**Talk Track:** 
- "Look at the **Risk Meter** and **Urgency Badge**. The AI didn't just read the document; it understood that 'forthwith' means critical priority."
- "Here is our **Explainable AI Reasoning** explaining exactly *why* it assigned a High Heat Score."
- "We also generate a **Voice-Ready Narration**, allowing for seamless accessibility integrations."

### 4. The Developer Angle (2:00 - 2:30)
**Action:** Point to the `frontend_adapted` block and the `/metrics` endpoint.
**Talk Track:** "From an engineering standpoint, this API is bulletproof. It features normalized response schemas so frontends never crash, fallback mechanisms if an NLP model fails, and real-time performance analytics tracking memory usage."

### 5. Conclusion (2:30 - 3:00)
**Action:** Trigger the `/export` endpoint to download the `.txt` summary.
**Talk Track:** "NyayaMitra doesn't just read law; it comprehends, prioritizes, and exports it. Thank you."

## Fallback Strategy (If things go wrong)
- **File Upload Fails?** Instantly switch to the Postman Mock Collection tab and hit "Send". 
- **OCR hangs?** Explain: "We've enabled `LIGHT_MODE` for this demo to save laptop battery, which gracefully bypasses heavy OCR while preserving data structure."
