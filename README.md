# 🚀 SkillSprint AI — Enterprise GenAI Onboarding & Verification Engine

**SkillSprint AI** is an intelligent, automated employee onboarding and training platform that transforms raw company policy documents (PDFs, SOPs, Handbooks) into personalized, role-specific onboarding plans, practical tasks, and interactive quizzes.

Unlike standard LLM wrappers, SkillSprint AI employs a **Dual-Pipeline Architecture** combining GenAI flexibility with strict Python-based deterministic validation to eliminate hallucinations, enforce mandatory policy coverage, and guarantee 100% source traceability.

---

### ✨ Key Features

- 📄 **Multi-Format Document Parsing & Traceable Chunking:** Extracts text from PDF/DOCX files while tagging metadata down to document ID, version, page, and section.
- ⚡ **Dual-Pipeline Processing:**
  - **Pipeline 1 (GenAI Generation Engine):** Uses Google Gemini / OpenAI with strict Pydantic JSON schemas to generate structured onboarding roadmaps.
  - **Pipeline 2 (Ground-Truth Python Engine):** Independent, rule-based Python validator that evaluates generated plans against a master **Role Requirement Matrix** (0% LLM dependency).
- 📊 **Audit & Scoring Metrics:** Automatically calculates **Coverage Score %** and **Traceability Score %** while flagging unmapped or conflicting statements.
- 🔄 **Policy Versioning & Selective Regeneration:** Automatically detects updates (e.g., Policy v1.0 → v2.0) and regenerates only affected learning modules.
- 🛡️ **Prompt Injection Defense:** Input sanitization layer preventing adversarial document attacks.
- 👤 **Human-in-the-Loop Review & Dashboard:** Interactive UI featuring Admin review queues, side-by-side verification grids, and employee progress tracking.

---

### 🛠️ Tech Stack

- **Frontend / Dashboard:** Streamlit / Python
- **LLM Engine:** Google Gemini API (`google-genai`), Pydantic
- **Document Processing:** `pdfplumber`, `PyPDF`, `python-docx`
- **Validation Engine:** Python 3.11+ (Deterministic Rule Matchers, Regex Parsing)
- **Visualization:** Plotly, Pandas
