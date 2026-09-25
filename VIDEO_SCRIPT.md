# SkillSprint AI: Demonstration Video Script & Storyboard

**Project:** SkillSprint AI (Enterprise AI-Driven Employee Onboarding & Compliance Platform)  
**Target Video Format:** MP4 (1080p, 60fps, Crisp Audio)  
**Total Target Duration:** 7:30 – 8:00 Minutes  
**Narrator / Presenter:** Farhad Khan (Lead Dataset Architect & Security Specialist) with Team Callouts (Anas, Yazdan, Usman)  
**SRS Alignment:** Fully maps across all 20+ mandatory demonstration steps in SRS Section 1.10.

---

## Storyboard Overview & Time Distribution

```
+-----------------------------------------------------------------------------------------------+
|  0:00 - 0:45   | ACT 1: Executive Overview & Problem Statement (Farhad)                      |
|  0:45 - 1:45   | ACT 2: Dataset Architecture, 20 Corporate Docs & Ground Truth Matrix         |
|  1:45 - 3:00   | ACT 3: Dual-Pipeline Live Demo: GenAI Plan Synthesis (Pipeline 1)            |
|  3:00 - 4:15   | ACT 4: Deterministic Python Validation & Scoring Engine (Pipeline 2)         |
|  4:15 - 5:30   | ACT 5: Precedence Conflict Resolution Demo (POL vs FAQ / v2.0 vs v1.0)       |
|  5:30 - 6:45   | ACT 6: Adversarial Security & Zero-Trust Prompt Injection Defense Demo       |
|  6:45 - 7:45   | ACT 7: Export Utilities, Progress Dashboard & Closing Summary               |
+-----------------------------------------------------------------------------------------------+
```

---

## Scene-by-Scene Script & Action Breakdown

### ACT 1: Executive Overview & System Architecture (0:00 – 0:45)

#### Scene 1.1: Title Card & Mission Introduction [0:00 – 0:20]
- **Visual:** Full HD animated title screen featuring the "SkillSprint AI" logo, team credits (Farhad Khan, Anas Khan, Yazdan, Usman), and tagline: *"Zero-Hallucination Enterprise Onboarding Platform"*.
- **Screen Action:** Fade into the modern dark-mode Streamlit web application landing page.
- **Voiceover (Farhad):**
  > *"Welcome to SkillSprint AI. In modern enterprise environments, employee onboarding is broken—fragmented across dozens of conflicting policy PDFs, outdated knowledge base articles, and unverified AI tools that hallucinate compliance rules. Today, our team—Farhad, Anas, Yazdan, and Usman—will demonstrate how SkillSprint AI solves this challenge through a novel Dual-Pipeline Architecture that combines generative AI flexibility with deterministic mathematical verification."*

#### Scene 1.2: System Architecture Diagram Walkthrough [0:20 – 0:45]
- **Visual:** High-resolution architectural diagram displaying Ingestion -> Security Sanitizer -> Pipeline 1 (Gemini GenAI) -> Pipeline 2 (Python Deterministic Rule Engine) -> Streamlit UI.
- **Voiceover (Farhad):**
  > *"Notice our core architectural philosophy: Generative models synthesize, but deterministic Python code validates. No LLM is ever permitted to self-grade its own compliance output."*

---

### ACT 2: Dataset Corpus & Authoritative Master Matrix (0:45 – 1:45)

#### Scene 2.1: Ingesting 20 Corporate SOPs & Policies [0:45 – 1:15]
- **Visual:** Screen switches to the "Document Repository" tab in the application. Directory tree shows 20 structured corporate documents for *Apex Global Solutions Inc.*
- **Screen Action:** User clicks on `POL-HR-03` (Annual Leave Policy v1.2), `POL-SEC-01` (InfoSec Policy v2.1), and `SOP-SUP-01` (Support Escalation Matrix v2.0). Side panel highlights metadata tags: document IDs, version numbers, and quantitative policy caps ($50 gift cap, 14-char password, 15-min Sev-1 escalation).
- **Voiceover (Farhad):**
  > *"Under Farhad's domain, we built a comprehensive, realistic corporate corpus consisting of 20 formal policies and SOPs covering HR, Information Security, Finance, Software Engineering, DevOps, and Facilities. Crucially, this dataset contains 10 intentional version updates and 10 contradiction cases designed to test edge-case resilience."*

#### Scene 2.2: Master Ground-Truth Matrix (200 Requirements) [1:15 – 1:45]
- **Visual:** User opens the "Ground-Truth Requirement Matrix" tab. A searchable data grid displays 200 requirement items mapped across 10 job roles.
- **Screen Action:** Filter by role `ROLE-CSR-01` (Customer Support Executive) and highlight `is_mandatory: true` badges, priority tags, and source citations.
- **Voiceover (Farhad):**
  > *"Our master matrix contains 200 strictly audited requirement objects across 10 canonical job roles, including 175 mandatory compliance checkpoints. This static JSON dataset serves as the immutable ground truth for Pipeline 2."*

---

### ACT 3: Pipeline 1 Live Demo: GenAI Plan Synthesis (1:45 – 3:00)

#### Scene 3.1: Role Selection & Document Parsing [1:45 – 2:15]
- **Visual:** Streamlit UI "Generate Onboarding Plan" view.
- **Screen Action:** Dropdown selects `Software Support Engineer (ROLE-SWE-03)`. User clicks **"Parse & Analyze SOPs"**.
- **Visual Cue:** Real-time progress bar demonstrates text extraction and 500-token semantic chunking with metadata tagging (`doc_id`, `section_id`, `page_number`).
- **Voiceover (Farhad / Anas):**
  > *"Yazdan's chunking engine processes the corporate corpus, attaching cryptographic metadata to each chunk. Next, Anas's GenAI pipeline invokes the Google Gemini API with controlled prompt templates and negative constraints against hallucination."*

#### Scene 3.2: Structured Pydantic Plan Generation [2:15 – 3:00]
- **Visual:** The AI generates a structured 4-phase onboarding plan displayed in glassmorphic cards: Day 1 (Hardware MFA & Repo Access), Week 1 (Secure SDLC 2-Peer Review & DOMPurify XSS Rules), Month 1 (GDPR 30-day Erasure & Vault Key Rotation), and Quarter 1.
- **Screen Action:** Click "View Raw JSON Payload" to reveal strict Pydantic schema adherence with exact `req_id`, `policy_name`, and `source_section` citations.
- **Voiceover (Farhad):**
  > *"Notice how the LLM outputs a clean, schema-enforced JSON curriculum. But can we trust it blindly? Let's send this plan to Pipeline 2 for mathematical validation."*

---

### ACT 4: Pipeline 2: Python Deterministic Rule Engine (3:00 – 4:15)

#### Scene 4.1: Mathematical Coverage & Traceability Scoring [3:00 – 3:40]
- **Visual:** Screen navigates to the "Pipeline 2: Compliance Verification" tab.
- **Screen Action:** User clicks **"Run Deterministic Verification"**. In less than 50 milliseconds, three large telemetry gauge cards render:
  - **Mandatory Coverage Score: 100%** (15/15 mandatory requirements satisfied)
  - **Citation Traceability Score: 98.5%** (Accurate Doc ID, Section, and Version refs)
  - **Hallucination Rate: 0.0%** (0 unmapped claims detected)
- **Voiceover (Farhad / Yazdan):**
  > *"Pipeline 2 executes purely in Python—zero LLMs involved. It runs set-theoretic intersections against `role_matrix.json` to calculate exact mathematical coverage and citation traceability scores using our published formulas."*

#### Scene 4.2: Simulated Hallucination & Omission Detection [3:40 – 4:15]
- **Visual:** User toggles "Inject Synthetic AI Error" (simulating an LLM omitting the 14-character password requirement and inventing a fake $5,000 laptop stipend).
- **Screen Action:** Re-run verification. The UI instantly flashes a Red Warning Banner:
  - `[OMISSION DETECTED]: REQ-001 (POL-SEC-01 v2.1 MFA & 14-char password omitted)`
  - `[HALLUCINATION DETECTED]: Unmapped requirement '$5,000 stipend' has no lineage in corpus`
  - Coverage score drops deterministically from 100% to 93.3%.
- **Voiceover (Farhad):**
  > *"Watch how Pipeline 2 instantly catches the hallucination and missing mandatory requirement. The system pinpoints the exact omitted section ID without ambiguity."*

---

### ACT 5: Precedence Conflict Resolution Demo (4:15 – 5:30)

#### Scene 5.1: Policy vs. FAQ Conflict (`POL-HR-03` vs `FAQ-HR-01`) [4:15 – 4:55]
- **Visual:** User navigates to "Conflict & Version Resolution" panel.
- **Screen Action:** System highlights the Annual Leave Rollover check:
  - `FAQ-HR-01 v1.0` claims 10 days carryover.
  - `POL-HR-03 v1.2` mandates a 5-day carryover cap.
- **Visual Cue:** The Precedence Resolver renders a green resolution pill: `[RESOLVED]: POL-HR-03 v1.2 takes precedence (Policy > FAQ). Rule enforced: 5 Days Max.`
- **Voiceover (Farhad):**
  > *"Here, our Precedence Engine evaluates conflicting documents. Because formal policies legally supersede informal FAQ pages, the system automatically enforces the 5-day rollover rule from POL-HR-03 v1.2, rejecting the outdated 10-day claim."*

#### Scene 5.2: Version Update Override (`POL-SEC-01` v2.1 vs v1.0) [4:55 – 5:30]
- **Visual:** Comparison modal showing `POL-SEC-01 v1.0` (SMS OTP permitted) vs `POL-SEC-01 v2.1` (Hardware MFA required).
- **Voiceover (Farhad):**
  > *"Similarly, for version updates, the engine enforces higher semantic versions, ensuring modern security baselines are strictly preserved."*

---

### ACT 6: Adversarial Security & Prompt Injection Defense (5:30 – 6:45)

#### Scene 6.1: Uploading Adversarial Document (`ADV-01` & `ADV-02`) [5:30 – 6:05]
- **Visual:** Screen switches to the "Security Sanitizer & Threat Telemetry" tab.
- **Screen Action:** User uploads `ADV-01_direct_system_override.txt` and `ADV-02_zero_width_unicode_hiding.txt` into the document ingestion uploader.
- **Screen Action:** User clicks **"Execute Pre-RAG Security Scan"**.
- **Voiceover (Farhad):**
  > *"Now for the security demonstration. What happens when an attacker attempts indirect prompt injection? We upload ADV-01, containing hidden override directives, and ADV-02, which conceals malicious instructions behind invisible zero-width Unicode characters."*

#### Scene 6.2: Real-Time Sanitization & Telemetry Audit Log [6:05 – 6:45]
- **Visual:** Red and Amber security alert cards appear in real time:
  - `[ALERT]: Threat Category: INSTRUCTION_OVERRIDE (Threat Score: 0.95)`
  - `[CLEANED]: 5 Zero-Width Unicode Characters Stripped (\u200B, \u200C, \uFEFF)`
  - `[REDACTION]: Neutralized text to [REDACTED_SECURITY_THREAT_INSTRUCTION_OVERRIDE]`
  - `[ISOLATION]: Data wrapped in [UNTRUSTED_DOCUMENT_START] boundary tags`
- **Screen Action:** View side-by-side diff showing dirty vs sanitized text.
- **Voiceover (Farhad):**
  > *"Farhad's `sanitizer.py` engine strips all invisible Unicode, decodes base64 blobs, redacts override trigger phrases, and wraps untrusted data in XML isolation boundaries. The downstream Gemini pipeline receives a completely neutralized payload, achieving a 100% defense rate across all 10 adversarial benchmark cases."*

---

### ACT 7: Export Utilities, Progress Dashboard & Conclusion (6:45 – 7:45)

#### Scene 7.1: Interactive Onboarding Dashboard & Progress Tracking [6:45 – 7:15]
- **Visual:** User opens the "Employee Onboarding Portal" view designed by Usman.
- **Screen Action:** Interactive checklist allows an employee to mark tasks complete, upload compliance attestations (e.g., Expensify receipts for the $300 remote stipend), and observe the radial completion gauge animate to 100%.
- **Screen Action:** User clicks **"Export Audit Package"** to download a verified PDF and CSV compliance report.
- **Voiceover (Farhad):**
  > *"Usman's intuitive UI provides employees with an interactive, phase-by-phase learning journey, complete with one-click PDF and CSV audit exports for HR and compliance officers."*

#### Scene 7.2: Final Summary & Credits [7:15 – 7:45]
- **Visual:** Split screen highlighting the 4 core achievements:
  1. *20 Enterprise Documents & 200 Ground-Truth Requirements*
  2. *Dual-Pipeline Architecture with 0% Hallucination Tolerance*
  3. *Deterministic Precedence Conflict Resolver*
  4. *Zero-Trust Pre-RAG Adversarial Prompt Injection Defense*
- **Voiceover (Farhad):**
  > *"By uniting generative AI with deterministic Python ground-truth verification and zero-trust security sanitization, SkillSprint AI sets a new benchmark for enterprise AI reliability. Thank you from Farhad, Anas, Yazdan, and Usman."*
- **Visual:** Fade out to SkillSprint AI repository link and MIT License badge.

---

## Production Recording Guidelines for Team

- **Audio Track:** 48kHz, mono/stereo vocal capture with noise suppression filter.
- **Screen Capture:** 1920x1080 resolution, 60fps, cursor highlighting enabled.
- **Terminal Demonstrations:** Run `pytest tests/test_security.py -v` to showcase the automated test suite passing with 100% green checks during the security segment.
