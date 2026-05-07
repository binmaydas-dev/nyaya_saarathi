Nyaya Saarathi
Guiding Judgments into Action
AI-Assisted Legal Intelligence for Smarter Governance
⸻
Overview
Nyaya Saarathi is an AI-Assisted Legal Intelligence Platform designed to transform lengthy court judgment PDFs into structured, explainable, and actionable government decision plans.
The platform helps government departments and legal officers:
* analyze court judgments
* identify legal directives
* detect compliance deadlines
* generate administrative recommendations
* classify risk and priority
* support appeal considerations
* enable human verification workflows
The system combines OCR, NLP, Explainable AI, Decision Intelligence, and confidence-aware human-supervised processing to improve governance efficiency and reduce manual legal workload.
⸻
Key Features
* Court Judgment PDF Upload
* Legal Information Extraction
* Deadline Detection
* Decision Intelligence Engine
* Department Mapping
* Risk & Priority Classification
* Appeal Suggestions
* Explainable AI Reasoning
* Human Verification Workflow
* Dashboard Visualization
* Demo Mode Support
* Multilingual-Ready Architecture
⸻
System Workflow
PDF Upload
→ OCR / NLP Extraction
→ Decision Intelligence
→ Confidence Analysis
→ Human Verification
→ Dashboard Visualization
⸻
Technologies Used
Component	Technology
Backend	FastAPI
NLP	spaCy
OCR	PaddleOCR
Frontend	React
UI Framework	Tailwind CSS
Animation	Framer Motion
PDF Processing	PyMuPDF
Extraction Engine	Regex + NLP
⸻
Project Structure
Nyaya_Saarathi/
│
├── backend/
├── frontend/
├── README.md
├── requirements.txt
└── sample_case.pdf
⸻
Backend Setup
Step 1: Navigate to Backend
cd backend
⸻
Step 2: Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
macOS / Linux
python3 -m venv venv
source venv/bin/activate
⸻
Step 3: Install Dependencies
pip install -r requirements.txt
⸻
Step 4: Run Backend Server
Windows
set DEMO_MODE=true
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
macOS / Linux
DEMO_MODE=true python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
⸻
Backend URL
http://127.0.0.1:8000/docs
⸻
Frontend Setup
Step 1: Navigate to Frontend
cd frontend
⸻
Step 2: Install Dependencies
npm install
⸻
Step 3: Run Frontend
npm run dev
⸻
Frontend URL
http://127.0.0.1:5173
⸻
Demo Mode
For stable demonstration and testing, use:
/upload?mock_mode=true
or select the Load Demo Case option from the frontend interface.
⸻
Important API Routes
Route	Description
/health	Health Check
/demo-test	Demo Response
/upload	PDF Upload
/upload?mock_mode=true	Demo-Safe Upload
/docs	Swagger Documentation
⸻
Human Verification Workflow
Nyaya Saarathi uses a confidence-aware legal intelligence workflow.
If extraction confidence is low due to:
* poor OCR quality
* scanned documents
* ambiguous legal directives
the system automatically flags the case for mandatory human verification.
Workflow:
Low Confidence
→ Manual Review
→ Approve / Edit / Reject
→ Final Action
This reduces hallucination risks and improves trust in AI-assisted governance systems.
⸻
Explainable AI
Unlike black-box AI systems, Nyaya Saarathi provides explainable reasoning for generated recommendations.
Example reasoning:
* Detected compensation directive
* Detected mandatory deadline
* Identified compliance reporting requirement
This improves transparency and auditability in legal workflows.
⸻
Multilingual Architecture
The platform is future-ready for multilingual legal workflows.
Supported architecture:
* Telugu
* Hindi
* Kannada
* English
Workflow:
Regional Language
→ Translation Layer
→ English Legal Processing
→ Dashboard Output
⸻
Known Limitations
* OCR support is partially disabled in demo environments
* Best performance is achieved with digital text-based PDFs
* Low-quality scanned documents may require manual verification
⸻
Future Scope
* Advanced OCR Integration
* Government Workflow Integrations
* Cloud Deployment
* Legal Knowledge Graphs
* Multilingual Expansion
* Workflow Automation
* Real-Time Compliance Monitoring
Final Note

Nyaya Saarathi bridges the gap between court judgments and verified administrative action through explainable AI, confidence-aware workflows, and human-supervised legal intelligence.
