# NyayaMitra Hackathon UI

Lightweight frontend for the verified FastAPI backend.

## Run

Start the backend first:

```bash
cd /Users/ajaykowkuntla/Downloads/hacker_earth/backend
DEMO_MODE=true venv_mac/bin/python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Start the frontend:

```bash
cd /Users/ajaykowkuntla/Downloads/hacker_earth/frontend
python3 server.py
```

Open:

```text
http://127.0.0.1:5173
```

## Demo PDF Guidance

Use clean digital court PDFs with selectable text and readable formatting.

Avoid:

- noisy scans
- handwritten documents
- corrupted PDFs
- very large scanned bundles

For a guaranteed presentation path, keep "Demo-safe mock upload" enabled. If upload fails, the UI automatically loads `/demo-test`.
