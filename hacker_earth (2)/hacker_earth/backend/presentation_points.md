# Presentation Tech Points (Judge Q&A Cheat Sheet)

If the judges ask technical questions, use these points to defend your architecture.

## 1. "Why didn't you just use an LLM API for everything?"
**Answer:** "Cost, privacy, and speed. Sending confidential legal documents to a 3rd party API violates data privacy norms. By using offline, targeted NLP (spaCy + Regex heuristics), we keep processing local, incredibly cheap, and extremely fast. We built a domain-specific engine rather than a generic prompt wrapper."

## 2. "How do you handle scanned documents?"
**Answer:** "We implemented an intelligent fallback. Our `extract_pdf` module checks the text-to-page density ratio. If it's too low (under 100 chars/page), it automatically routes the document to `PaddleOCR`, which we configured to support both English and Hindi."

## 3. "What happens if a module fails during production?"
**Answer:** "Resilience is built-in. Every NLP module is wrapped in safe `try...except` blocks. If extraction fails, the API gracefully degrades, returning standardized safe defaults (like `priority: Unknown`) instead of crashing the frontend."

## 4. "How did you optimize performance?"
**Answer:** 
- **Lazy Loading:** Massive models like `spaCy` and `PaddleOCR` are only loaded into memory when absolutely necessary.
- **MD5 Hash Caching:** We hash uploaded files. If a user uploads the same file twice, the API returns the result from an LRU cache in 0.01 seconds.
- **Light Mode:** We implemented a `LIGHT_MODE` environment variable to strip out heavy processing for low-resource environments.

## 5. "How is the data passed to the frontend?"
**Answer:** "We use a unified `response_formatter.py` and a `frontend_adapter.py`. The backend flattens deeply nested NLP data into UI-ready arrays and Bootstrap-safe color codes, meaning the React team can literally map over the response without writing any transformation logic."
