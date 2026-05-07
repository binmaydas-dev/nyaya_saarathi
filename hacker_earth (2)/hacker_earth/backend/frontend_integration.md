# NyayaMitra Frontend Integration Guide

Welcome to the NyayaMitra Frontend team! We've designed this backend specifically so you don't have to write complex data transformation logic. 

## The Golden Rule: The Normalized Schema
Every single endpoint (even errors) will return this exact shape:

```json
{
  "status": "success", // or "partial_success", "error"
  "request_id": "uuid",
  "processing_mode": "text_extraction", // ocr, mock_demo, etc.
  "analytics": {}, // For your performance tracking widget
  "data": {}, // Raw extracted legal data
  "dashboard": {}, // Structured cards and analytics
  "errors": [], // Array of strings (if any)
  "frontend_adapted": {} // <--- THIS IS YOUR BEST FRIEND
}
```

## The `frontend_adapted` Object
We built the `frontend_adapted` block to map directly to your React/Vue components. It removes deeply nested null checks and converts backend logic into UI-ready states.

**Key Fields inside `frontend_adapted`:**
- `ui_risk_meter.value`: An integer `0-100` for your circular progress bar.
- `ui_risk_meter.color`: Pre-mapped to Bootstrap/Tailwind standard colors (`danger`, `warning`, `success`, `info`). Pass this straight to your CSS class!
- `ui_tags`: An array of objects `[{"label": "Tax", "key": "tax"}]` ready for mapping over Pill/Badge components.
- `ui_cards`: An array of objects `[{"id": 0, "content": "..."}]` for your summary bullet points.
- `ui_voice`: A perfect 1-sentence string to feed into your Text-to-Speech API.

## Endpoints Quick Reference

### 1. File Upload
**Endpoint:** `POST /upload`
**Query Params:** 
- `mock_mode=true` (Use this while building UI to get instant, beautiful data)
- `lang=en` (or `hi` for Hindi)
**Body:** FormData with `file` (PDF)

### 2. Export Summary
**Endpoint:** `GET /export/{request_id}?format=txt`
**Usage:** Call this when the user clicks the "Download Summary" button. It returns a downloadable file stream.

### 3. Health & Metrics
**Endpoint:** `GET /metrics`
**Usage:** Use this to power a small "System Status" footer in your UI showing memory usage and cached requests.

## Loading State Suggestions
1. **Initial Upload:** Show a generic spinner.
2. **Text Extraction:** If `processing_mode` returns `ocr`, show a specific "Running AI Character Recognition" toast. (Note: Since it's a single blocking request, you'll just wait for the response, but you can poll `/health` if you want to show activity).
3. **Demo Tip:** Use `mock_mode=true` during the hackathon pitch to ensure the loading spinner is on screen for exactly 0.5 seconds!
