import json
import os

# Define the 10 canonical roles
roles = [
    {
        "role_id": "ROLE-CSR-01",
        "role_name": "Customer Support Executive",
        "department": "Customer Experience",
        "level": "L1/L2 Specialist",
        "description": "Manages enterprise customer queries, handles billing adjustments, and escalates critical system outages per SLA matrix.",
        "primary_work_mode": "Remote / Hybrid"
    },
    {
        "role_id": "ROLE-DAT-02",
        "role_name": "Data Analyst",
        "department": "Business Intelligence & Analytics",
        "level": "L2 Specialist",
        "description": "Builds BI telemetry dashboards, performs data warehouse ETL transformations, and adheres to data privacy and anonymization standards.",
        "primary_work_mode": "Remote / Hybrid"
    },
    {
        "role_id": "ROLE-SWE-03",
        "role_name": "Software Support Engineer",
        "department": "Engineering Operations",
        "level": "L2 Mid-Senior",
        "description": "Diagnoses production software issues, writes patch bug fixes, executes PR peer reviews, and enforces Secure SDLC standards.",
        "primary_work_mode": "Remote"
    },
    {
        "role_id": "ROLE-FIN-04",
        "role_name": "Finance Associate",
        "department": "Corporate Finance & Accounting",
        "level": "L2 Associate",
        "description": "Audits corporate expense claims against per diem limits, coordinates RFP vendor bidding, and maintains invoice ledger accuracy.",
        "primary_work_mode": "Hybrid"
    },
    {
        "role_id": "ROLE-HRO-05",
        "role_name": "HR Executive",
        "department": "People & Culture",
        "level": "L2 Executive",
        "description": "Oversees new hire onboarding curricula, leave balances, performance review calibration, and employee offboarding logistics.",
        "primary_work_mode": "Hybrid"
    },
    {
        "role_id": "ROLE-OPS-06",
        "role_name": "Workplace Operations Lead",
        "department": "Workplace Operations & Facilities",
        "level": "L3 Lead",
        "description": "Oversees physical access security, visitor registration and badging, facility health and safety, and hardware asset recovery.",
        "primary_work_mode": "On-site"
    },
    {
        "role_id": "ROLE-QAE-07",
        "role_name": "Quality Assurance Lead",
        "department": "Quality Assurance",
        "level": "L3 Lead",
        "description": "Enforces 80% automated test coverage gates, manages regression testing cycles, and governs production release blockers.",
        "primary_work_mode": "Remote"
    },
    {
        "role_id": "ROLE-DVO-08",
        "role_name": "DevOps Engineer",
        "department": "Cloud Platform & Infrastructure",
        "level": "L2/L3 Senior",
        "description": "Manages Kubernetes infrastructure, Blue-Green zero-downtime deployment pipelines, and automated secret rotation via HashiCorp Vault.",
        "primary_work_mode": "Remote"
    },
    {
        "role_id": "ROLE-SEC-09",
        "role_name": "Information Security Analyst",
        "department": "Security & Compliance (SecOps)",
        "level": "L3 Specialist",
        "description": "Monitors SIEM telemetry, investigates security breach alerts within 24h SLA, audits IAM hardware MFA enforcement, and validates encryption standards.",
        "primary_work_mode": "Remote / Hybrid"
    },
    {
        "role_id": "ROLE-PRM-10",
        "role_name": "Product Manager",
        "department": "Product Management",
        "level": "L3 Lead",
        "description": "Defines product roadmaps, validates compliance requirements with stakeholders, prioritizes feature backlogs, and coordinates quarterly OKRs.",
        "primary_work_mode": "Hybrid"
    }
]

# Write roles_list.json
with open("dataset/roles/roles_list.json", "w", encoding="utf-8") as f:
    json.dump(roles, f, indent=2)

# Generate 150+ Requirements Matrix
# Base company-wide requirements (15 items applied to each role = 150 items) + role-specific items (5 per role = 50 items) = 200 items total!
company_wide_templates = [
    {
        "base_id": "SEC-01",
        "category": "Security & Access",
        "policy_name": "Information Security Policy",
        "source_doc_id": "POL-SEC-01",
        "source_section": "Section 2.1 - Authentication Standards",
        "doc_version": "v2.1",
        "is_mandatory": True,
        "priority": "Critical",
        "due_stage": "Day 1",
        "assessment_topic": "Hardware MFA & Password Security",
        "task_description": "Configure single sign-on (SSO) with mandatory hardware-based MFA (FIDO2 / YubiKey token) and a minimum 14-character alphanumeric passphrase. Legacy SMS-based OTP is explicitly prohibited.",
        "conflict_flag": True,
        "conflict_notes": "Overrides POL-SEC-01 v1.0 which permitted SMS OTP and 10-char passwords. Precedence: v2.1 takes precedence."
    },
    {
        "base_id": "SEC-02",
        "category": "Endpoint Security",
        "policy_name": "Information Security Policy",
        "source_doc_id": "POL-SEC-01",
        "source_section": "Section 3.1 - Workstation Auto-Lock",
        "doc_version": "v2.1",
        "is_mandatory": True,
        "priority": "High",
        "due_stage": "Day 1",
        "assessment_topic": "Workstation Inactivity Lockout",
        "task_description": "Verify endpoint operating system lock screen timer is set to a maximum of 5 minutes of inactivity with BitLocker/FileVault full-disk encryption active.",
        "conflict_flag": True,
        "conflict_notes": "Supersedes deprecated physical lockbox rules from obsolete POL-SEC-04 v1.0."
    },
    {
        "base_id": "HR-01",
        "category": "Corporate Ethics & Governance",
        "policy_name": "Global Code of Conduct",
        "source_doc_id": "POL-HR-01",
        "source_section": "Section 4.2 - Gifts and Anti-Bribery Compliance",
        "doc_version": "v1.0",
        "is_mandatory": True,
        "priority": "High",
        "due_stage": "Week 1",
        "assessment_topic": "Anti-Bribery & Gift Declarations",
        "task_description": "Complete Code of Conduct attestation acknowledging that any business gift, hospitality, or favor exceeding $50 USD fair market value must be declared within 5 business days. Cash gifts of any value are prohibited.",
        "conflict_flag": False,
        "conflict_notes": None
    },
    {
        "base_id": "HR-02",
        "category": "Workplace Policy",
        "policy_name": "Remote and Hybrid Work Policy",
        "source_doc_id": "POL-HR-02",
        "source_section": "Section 2.1 - Core Collaboration Hours",
        "doc_version": "v2.0",
        "is_mandatory": True,
        "priority": "Medium",
        "due_stage": "Day 1",
        "assessment_topic": "Remote Core Working Hours",
        "task_description": "Acknowledge remote core collaboration availability window between 10:00 AM and 4:00 PM PKT on Slack and email channels.",
        "conflict_flag": True,
        "conflict_notes": "Supersedes POL-HR-02 v1.0 which specified 9:00 AM to 6:00 PM PKT."
    },
    {
        "base_id": "HR-03",
        "category": "Workplace Policy",
        "policy_name": "Remote and Hybrid Work Policy",
        "source_doc_id": "POL-HR-02",
        "source_section": "Section 3.1 - Workstation Ergonomics Stipend",
        "doc_version": "v2.0",
        "is_mandatory": False,
        "priority": "Medium",
        "due_stage": "Month 1",
        "assessment_topic": "Home Ergonomics Allowance",
        "task_description": "Submit receipts for the one-time $300 USD home workstation ergonomic allowance via Expensify within 60 days of onboarding.",
        "conflict_flag": True,
        "conflict_notes": "Supersedes POL-HR-02 v1.0 allowance of $200 USD."
    },
    {
        "base_id": "HR-04",
        "category": "HR & Leave Policy",
        "policy_name": "Annual Paid Time Off and Leave Policy",
        "source_doc_id": "POL-HR-03",
        "source_section": "Section 3.1 - Leave Carryover Limits",
        "doc_version": "v1.2",
        "is_mandatory": True,
        "priority": "High",
        "due_stage": "Month 1",
        "assessment_topic": "Annual Leave Rollover Cap",
        "task_description": "Review and acknowledge the 20 days annual PTO policy and strict maximum 5-day carryover limit into the next calendar year. Excess unused leave expires on Dec 31st.",
        "conflict_flag": True,
        "conflict_notes": "Direct conflict with FAQ-HR-01 v1.0 (which claims 10 days). Formal policy POL-HR-03 v1.2 strictly overrides FAQ."
    },
    {
        "base_id": "HR-05",
        "category": "Talent & Performance",
        "policy_name": "Employee Performance Management Policy",
        "source_doc_id": "POL-HR-04",
        "source_section": "Section 3.1 - PIP Criteria and Duration",
        "doc_version": "v1.0",
        "is_mandatory": False,
        "priority": "Medium",
        "due_stage": "Quarter 1",
        "assessment_topic": "Performance Reviews & Remedial Plans",
        "task_description": "Participate in quarterly OKR performance evaluations. Maintain minimum 2.5/5.0 rating to avoid mandatory 60-day Performance Improvement Plan (PIP).",
        "conflict_flag": False,
        "conflict_notes": None
    },
    {
        "base_id": "SEC-03",
        "category": "Data Security & Compliance",
        "policy_name": "Data Privacy and Encryption Policy",
        "source_doc_id": "POL-SEC-02",
        "source_section": "Section 2.1 - Encryption at Rest and in Transit",
        "doc_version": "v1.0",
        "is_mandatory": True,
        "priority": "Critical",
        "due_stage": "Week 1",
        "assessment_topic": "Data Protection & Encryption Controls",
        "task_description": "Adhere to AES-256 encryption at rest and TLS 1.3 in transit standards for all customer and confidential company data assets.",
        "conflict_flag": False,
        "conflict_notes": None
    },
    {
        "base_id": "SEC-04",
        "category": "Data Privacy Compliance",
        "policy_name": "Data Privacy and Encryption Policy",
        "source_doc_id": "POL-SEC-02",
        "source_section": "Section 3.1 - Data Subject Erasure SLA",
        "doc_version": "v1.0",
        "is_mandatory": True,
        "priority": "High",
        "due_stage": "Month 1",
        "assessment_topic": "GDPR / CCPA Erasure Compliance",
        "task_description": "Ensure customer Right-to-be-Forgotten / Data Deletion requests are processed and purged from all storage tiers within the strict 30-day statutory SLA.",
        "conflict_flag": False,
        "conflict_notes": None
    },
    {
        "base_id": "SEC-05",
        "category": "Incident Management",
        "policy_name": "Incident Response and Breach Notification Policy",
        "source_doc_id": "POL-SEC-03",
        "source_section": "Section 2.1 - Breach Notification Timeline",
        "doc_version": "v1.1",
        "is_mandatory": True,
        "priority": "Critical",
        "due_stage": "Day 1",
        "assessment_topic": "Security Incident Reporting SLA",
        "task_description": "Immediately report any suspected credential compromise or PII data exposure to SecOps via `#security-emergency`. Acknowledge 24-hour mandatory statutory notification SLA.",
        "conflict_flag": True,
        "conflict_notes": "Supersedes POL-SEC-03 v1.0 which allowed 72 hours."
    },
    {
        "base_id": "FIN-01",
        "category": "Financial Compliance",
        "policy_name": "Employee Travel & Expense Reimbursement SOP",
        "source_doc_id": "SOP-FIN-01",
        "source_section": "Section 2.1 - Meal Per Diem Limits",
        "doc_version": "v1.0",
        "is_mandatory": True,
        "priority": "Medium",
        "due_stage": "Week 1",
        "assessment_topic": "Expense Claims & Per Diem Guidelines",
        "task_description": "Adhere to the $75 USD daily meal per diem cap for business travel and retain itemized receipts for any individual expense over $25 USD.",
        "conflict_flag": False,
        "conflict_notes": None
    },
    {
        "base_id": "FIN-02",
        "category": "Financial Governance",
        "policy_name": "Employee Travel & Expense Reimbursement SOP",
        "source_doc_id": "SOP-FIN-01",
        "source_section": "Section 3.2 - Management Approval Thresholds",
        "doc_version": "v1.0",
        "is_mandatory": True,
        "priority": "High",
        "due_stage": "Week 1",
        "assessment_topic": "High-Value Expenditure Approvals",
        "task_description": "Ensure any individual expense or cumulative monthly claim exceeding $1,000 USD receives prior formal approval from the Department VP and Finance Controller.",
        "conflict_flag": False,
        "conflict_notes": None
    },
    {
        "base_id": "OPS-01",
        "category": "Workplace Safety & Security",
        "policy_name": "Physical Workplace Security & Visitor Access SOP",
        "source_doc_id": "SOP-OPS-01",
        "source_section": "Section 1.1 - Access Badges & Anti-Tailgating",
        "doc_version": "v1.0",
        "is_mandatory": True,
        "priority": "High",
        "due_stage": "Day 1",
        "assessment_topic": "Physical Access Badges",
        "task_description": "Wear and visibly display active corporate RFID access badges at all physical office locations. Never permit unauthorized tailgating.",
        "conflict_flag": False,
        "conflict_notes": None
    },
    {
        "base_id": "OPS-02",
        "category": "Workplace Security",
        "policy_name": "Physical Workplace Security & Visitor Access SOP",
        "source_doc_id": "SOP-OPS-01",
        "source_section": "Section 2.2 - Visitor Escort Mandate",
        "doc_version": "v1.0",
        "is_mandatory": True,
        "priority": "Medium",
        "due_stage": "Day 1",
        "assessment_topic": "Visitor Escort Protocols",
        "task_description": "Ensure all registered external guests, vendors, and interviewees are continuously escorted by an authorized employee in non-public office zones.",
        "conflict_flag": False,
        "conflict_notes": None
    },
    {
        "base_id": "OPS-03",
        "category": "Asset Governance",
        "policy_name": "Employee Offboarding & Hardware Asset Recovery SOP",
        "source_doc_id": "SOP-OPS-02",
        "source_section": "Section 2.1 - Hardware Asset Return SLA",
        "doc_version": "v1.0",
        "is_mandatory": True,
        "priority": "High",
        "due_stage": "Continuous",
        "assessment_topic": "Hardware Asset Custody & Recovery",
        "task_description": "Acknowledge obligation to return all company laptops, security tokens, and hardware equipment within 48 hours of separation.",
        "conflict_flag": False,
        "conflict_notes": None
    }
]

# Role-specific tailored requirement templates (5 per role = 50 total)
role_specific_templates = {
    "ROLE-CSR-01": [
        {
            "spec_id": "SUP-01",
            "category": "Customer Support Operations",
            "policy_name": "Customer Support Ticket Escalation Matrix",
            "source_doc_id": "SOP-SUP-01",
            "source_section": "Section 2.1 - Sev-1 Escalation SLA",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Sev-1 Incident Escalation SLA",
            "task_description": "Escalate all unacknowledged Severity 1 customer support tickets to the On-Call Engineering Incident Commander within 15 minutes of ticket creation.",
            "conflict_flag": True,
            "conflict_notes": "Supersedes SOP-SUP-01 v1.0 30-minute escalation threshold."
        },
        {
            "spec_id": "SUP-02",
            "category": "Customer Support Billing",
            "policy_name": "Customer Billing Dispute & Refund Authorization SOP",
            "source_doc_id": "SOP-SUP-02",
            "source_section": "Section 2.2 - L2 Refund Discretion Cap",
            "doc_version": "v1.1",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Week 1",
            "assessment_topic": "Customer Refund Authorization Limits",
            "task_description": "Apply customer billing dispute credits or refunds within the Level 2 discretionary authorization cap of $500 USD per ticket. Escalate higher amounts to Tier 3.",
            "conflict_flag": True,
            "conflict_notes": "Domain SOP-SUP-02 takes precedence over general finance reimbursement rules in SOP-FIN-01."
        },
        {
            "spec_id": "SUP-03",
            "category": "Customer Data Privacy",
            "policy_name": "Data Privacy and Encryption Policy",
            "source_doc_id": "POL-SEC-02",
            "source_section": "Section 3.1 - Redaction of Customer PII",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "PII Masking in Support Tickets",
            "task_description": "Ensure credit card numbers, passwords, and government IDs pasted by users in support tickets are immediately masked and scrubbed using Zendesk PII redaction tools.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "SUP-04",
            "category": "Support Knowledge Base",
            "policy_name": "Remote Access Troubleshooting FAQ",
            "source_doc_id": "FAQ-SEC-01",
            "source_section": "Section 1.0 - Hardware Token Triage",
            "doc_version": "v1.0",
            "is_mandatory": False,
            "priority": "Low",
            "due_stage": "Week 1",
            "assessment_topic": "Customer Portal SSO Troubleshooting",
            "task_description": "Follow standard troubleshooting workflows for customer SSO and hardware token authentication errors before raising engineering tickets.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "SUP-05",
            "category": "Customer SLA Reporting",
            "policy_name": "Customer Support Ticket Escalation Matrix",
            "source_doc_id": "SOP-SUP-01",
            "source_section": "Section 1.3 - Sev-2 and Sev-3 Response Times",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Week 1",
            "assessment_topic": "Tiered Support Response Metrics",
            "task_description": "Maintain 2-hour initial response SLA for Severity 2 tickets and 8-hour SLA for general Severity 3 customer inquiries.",
            "conflict_flag": False,
            "conflict_notes": None
        }
    ],
    "ROLE-DAT-02": [
        {
            "spec_id": "DAT-01",
            "category": "Data Governance",
            "policy_name": "Data Privacy and Encryption Policy",
            "source_doc_id": "POL-SEC-02",
            "source_section": "Section 2.1 - Database Encryption Standards",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Data Warehouse Cryptographic Controls",
            "task_description": "Validate that Snowflake and BigQuery data warehouse tables containing customer PII enforce AES-256 column-level encryption and dynamic data masking.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "DAT-02",
            "category": "Data Compliance",
            "policy_name": "Data Privacy and Encryption Policy",
            "source_doc_id": "POL-SEC-02",
            "source_section": "Section 3.1 - Automated Right to Erasure Pipelines",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Month 1",
            "assessment_topic": "GDPR Analytics Tombstone Processing",
            "task_description": "Implement automated tombstoning scripts in analytics data pipelines to propagate 30-day GDPR user deletion requests across derived BI tables.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "DAT-03",
            "category": "Business Intelligence Governance",
            "policy_name": "Global Code of Conduct",
            "source_doc_id": "POL-HR-01",
            "source_section": "Section 5.1 - Confidentiality of Financial Metrics",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Week 1",
            "assessment_topic": "Material Non-Public Information (MNPI)",
            "task_description": "Safeguard pre-release quarterly revenue dashboards and customer churn models from unauthorized internal dissemination or external leakage.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "DAT-04",
            "category": "Analytics Tooling Procurement",
            "policy_name": "Vendor Procurement, Bidding, and Contracting SOP",
            "source_doc_id": "SOP-FIN-02",
            "source_section": "Section 2.1 - 3-Bid Requirement for SaaS Tools",
            "doc_version": "v1.0",
            "is_mandatory": False,
            "priority": "Medium",
            "due_stage": "Quarter 1",
            "assessment_topic": "BI Software Procurement Protocol",
            "task_description": "Comply with procurement RFP mandates requiring 3 competitive vendor bids for any new data analytics, ETL, or ML tooling exceeding $25k ACV.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "DAT-05",
            "category": "Secret & Credential Management",
            "policy_name": "Cryptographic Key Management & Secret Rotation SOP",
            "source_doc_id": "POL-SEC-05",
            "source_section": "Section 2.1 - Database Credential Isolation",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Week 1",
            "assessment_topic": "ETL Service Account Vault Integration",
            "task_description": "Connect all automated Airflow ETL pipelines to HashiCorp Vault for dynamic credential leasing rather than hardcoding static database passwords.",
            "conflict_flag": False,
            "conflict_notes": None
        }
    ],
    "ROLE-SWE-03": [
        {
            "spec_id": "SWE-01",
            "category": "Secure Software Development",
            "policy_name": "Secure Software Development Lifecycle (SSDLC) SOP",
            "source_doc_id": "SOP-DEV-01",
            "source_section": "Section 1.1 - 2-Peer Review Mandate",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Branch Protection & Code Reviews",
            "task_description": "Obtain mandatory code review approvals from at least 2 independent peer engineers for every PR targeting `main` or `release/*` branches.",
            "conflict_flag": True,
            "conflict_notes": "Supersedes SOP-DEV-01 v1.0 single-reviewer rule."
        },
        {
            "spec_id": "SWE-02",
            "category": "Automated Code Security",
            "policy_name": "Secure Software Development Lifecycle (SSDLC) SOP",
            "source_doc_id": "SOP-DEV-01",
            "source_section": "Section 2.1 - Static Analysis & Vulnerability Gates",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "SAST & SCA Automated Gates",
            "task_description": "Ensure CI pipeline SonarQube SAST scans pass with zero Blocker/Critical issues and Dependabot reports zero High/Critical CVEs.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "SWE-03",
            "category": "Frontend Security",
            "policy_name": "Secure Software Development Lifecycle (SSDLC) SOP",
            "source_doc_id": "SOP-DEV-01",
            "source_section": "Section 2.4 - Client-Side DOM Sanitization",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Week 1",
            "assessment_topic": "XSS Sanitization via DOMPurify",
            "task_description": "Sanitize all dynamically rendered user HTML/DOM elements using DOMPurify and configure strict Content Security Policy (CSP) headers.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "SWE-04",
            "category": "Secret Protection",
            "policy_name": "Cryptographic Key Management & Secret Rotation SOP",
            "source_doc_id": "POL-SEC-05",
            "source_section": "Section 2.1 - Pre-Commit Secret Scanning",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Git Secret Leak Prevention",
            "task_description": "Install and maintain local `gitleaks` pre-commit hooks to block accidental commits of API keys, private certificates, or database credentials.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "SWE-05",
            "category": "Bug Fix Verification",
            "policy_name": "Quality Assurance Gating & Release Signoff SOP",
            "source_doc_id": "SOP-QA-01",
            "source_section": "Section 1.1 - Unit Test Coverage on Bug Fixes",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Week 1",
            "assessment_topic": "Regression Test Coverage",
            "task_description": "Accompany all production hotfix PRs with automated unit regression tests demonstrating at least 80% coverage on new/modified code.",
            "conflict_flag": False,
            "conflict_notes": None
        }
    ],
    "ROLE-FIN-04": [
        {
            "spec_id": "FIN-03",
            "category": "Procurement Audit",
            "policy_name": "Vendor Procurement, Bidding, and Contracting SOP",
            "source_doc_id": "SOP-FIN-02",
            "source_section": "Section 2.1 - 3-Bid RFP Verification",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Day 1",
            "assessment_topic": "Competitive Vendor RFP Audits",
            "task_description": "Audit and verify that purchase requisitions exceeding $25,000 USD ACV have attached documentation for 3 independent competitive vendor bids.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "FIN-04",
            "category": "Expense Auditing",
            "policy_name": "Employee Travel & Expense Reimbursement SOP",
            "source_doc_id": "SOP-FIN-01",
            "source_section": "Section 2.1 - Per Diem Audit Rules",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Week 1",
            "assessment_topic": "Travel Reimbursement Audit Compliance",
            "task_description": "Reject expense reimbursement claims where daily meal expenses exceed $75 USD per diem or receipts over $25 USD lack itemized breakdowns.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "FIN-05",
            "category": "Executive Expense Approvals",
            "policy_name": "Employee Travel & Expense Reimbursement SOP",
            "source_doc_id": "SOP-FIN-01",
            "source_section": "Section 3.2 - Secondary Sign-Off Routing",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Week 1",
            "assessment_topic": "Expense Approvals >$1,000",
            "task_description": "Route all employee expense claims with single or cumulative values exceeding $1,000 USD to the Department VP and Controller for digital sign-off.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "FIN-06",
            "category": "Anti-Bribery Ledger Checks",
            "policy_name": "Global Code of Conduct",
            "source_doc_id": "POL-HR-01",
            "source_section": "Section 4.3 - Cash Gift Prohibitions",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Month 1",
            "assessment_topic": "Anti-Bribery Accounting Controls",
            "task_description": "Flag and investigate any vendor or customer transaction categorized as discretionary cash disbursements or unitemized gift allowances.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "FIN-07",
            "category": "Customer Credit Auditing",
            "policy_name": "Customer Billing Dispute & Refund Authorization SOP",
            "source_doc_id": "SOP-SUP-02",
            "source_section": "Section 2.3 - High-Value Customer Refund Approvals",
            "doc_version": "v1.1",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Month 1",
            "assessment_topic": "Customer Refund Ledger Reconciliation",
            "task_description": "Reconcile monthly customer refund ledgers and verify Tier 3 managerial approval records for all refund issuances exceeding $500 USD.",
            "conflict_flag": False,
            "conflict_notes": None
        }
    ],
    "ROLE-HRO-05": [
        {
            "spec_id": "HRO-01",
            "category": "Leave Administration",
            "policy_name": "Annual Paid Time Off and Leave Policy",
            "source_doc_id": "POL-HR-03",
            "source_section": "Section 3.1 - HRIS Leave Carryover Cap",
            "doc_version": "v1.2",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Leave Balance HRIS Calibration",
            "task_description": "Configure HRIS system rules to automatically cap employee annual leave rollover at exactly 5 days and purge excess unapproved balances on Dec 31st.",
            "conflict_flag": True,
            "conflict_notes": "Enforces POL-HR-03 v1.2 over contradictory FAQ-HR-01 (10-day claim)."
        },
        {
            "spec_id": "HRO-02",
            "category": "Performance Management",
            "policy_name": "Employee Performance Management Policy",
            "source_doc_id": "POL-HR-04",
            "source_section": "Section 3.1 - 60-Day PIP Initiation",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Month 1",
            "assessment_topic": "PIP Milestone Structuring",
            "task_description": "Facilitate formal 60-day Performance Improvement Plans (PIPs) for employees rated under 2.5 across two consecutive review cycles.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "HRO-03",
            "category": "Remote Work Onboarding",
            "policy_name": "Remote and Hybrid Work Policy",
            "source_doc_id": "POL-HR-02",
            "source_section": "Section 3.1 - Onboarding Stipend Allocation",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "Medium",
            "due_stage": "Week 1",
            "assessment_topic": "Remote Onboarding Setup Stipend",
            "task_description": "Process the $300 USD home workstation ergonomic stipend for eligible remote new hires in their initial payroll cycle.",
            "conflict_flag": True,
            "conflict_notes": "Updated stipend from v1.0 ($200)."
        },
        {
            "spec_id": "HRO-04",
            "category": "Employee Offboarding",
            "policy_name": "Employee Offboarding & Hardware Asset Recovery SOP",
            "source_doc_id": "SOP-OPS-02",
            "source_section": "Section 1.1 - 15-Minute IAM Revocation Dispatch",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Offboarding Coordination & IT Ticketing",
            "task_description": "Trigger automated offboarding workflows notifying SecOps to revoke SSO access within 15 minutes of an employee's final separation hour.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "HRO-05",
            "category": "Workplace Ethics Compliance",
            "policy_name": "Global Code of Conduct",
            "source_doc_id": "POL-HR-01",
            "source_section": "Section 4.2 - Gift Register Maintenance",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Month 1",
            "assessment_topic": "Corporate Gift Register Auditing",
            "task_description": "Maintain and review the quarterly Corporate Gift & Entertainment Register for employee gift declarations exceeding $50 USD fair market value.",
            "conflict_flag": False,
            "conflict_notes": None
        }
    ],
    "ROLE-OPS-06": [
        {
            "spec_id": "OPS-04",
            "category": "Physical Access Security",
            "policy_name": "Physical Workplace Security & Visitor Access SOP",
            "source_doc_id": "SOP-OPS-01",
            "source_section": "Section 2.1 - Visitor ID & Badge Issuance",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Day 1",
            "assessment_topic": "Visitor Reception Management",
            "task_description": "Verify government-issued photo IDs, execute digital NDA forms, and issue temporary visitor badges for all external office guests.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "OPS-05",
            "category": "Asset Recovery",
            "policy_name": "Employee Offboarding & Hardware Asset Recovery SOP",
            "source_doc_id": "SOP-OPS-02",
            "source_section": "Section 2.1 - 48-Hour Laptop Collection SLA",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "IT Asset Physical Recovery",
            "task_description": "Track and log return of company-issued laptops, YubiKeys, and access badges within 48 hours of employee departure; dispatch secure courier kits for remote staff.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "OPS-06",
            "category": "Workplace Policy Transition",
            "policy_name": "Physical Clean Desk Policy",
            "source_doc_id": "POL-SEC-04",
            "source_section": "Section 1.0 - Clean Desk Policy Deprecation Notice",
            "doc_version": "v1.0",
            "is_mandatory": False,
            "priority": "Low",
            "due_stage": "Week 1",
            "assessment_topic": "Paperless Office Standard",
            "task_description": "Acknowledge retirement of POL-SEC-04 clean desk paper locker audits in favor of digital workstation auto-lock controls.",
            "conflict_flag": True,
            "conflict_notes": "Policy marked OBSOLETE."
        },
        {
            "spec_id": "OPS-07",
            "category": "Vendor Access Management",
            "policy_name": "Physical Workplace Security & Visitor Access SOP",
            "source_doc_id": "SOP-OPS-01",
            "source_section": "Section 2.2 - Facilities Contractor Escort",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Day 1",
            "assessment_topic": "Contractor Physical Escorts",
            "task_description": "Provide direct escort and supervision for third-party facilities contractors working in server rooms, electrical closets, and executive suites.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "OPS-08",
            "category": "Workplace Health & Ergonomics",
            "policy_name": "Remote and Hybrid Work Policy",
            "source_doc_id": "POL-HR-02",
            "source_section": "Section 3.2 - Office Ergonomic Standards",
            "doc_version": "v2.0",
            "is_mandatory": False,
            "priority": "Medium",
            "due_stage": "Month 1",
            "assessment_topic": "On-Premises Workstation Standards",
            "task_description": "Conduct quarterly ergonomic assessments for on-site hot desks and collaborative workspace areas.",
            "conflict_flag": False,
            "conflict_notes": None
        }
    ],
    "ROLE-QAE-07": [
        {
            "spec_id": "QAE-01",
            "category": "Quality Assurance Standards",
            "policy_name": "Quality Assurance Gating & Release Signoff SOP",
            "source_doc_id": "SOP-QA-01",
            "source_section": "Section 1.1 - 80% Automated Code Coverage Gate",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Test Coverage Release Gating",
            "task_description": "Enforce mandatory 80.0% code line coverage threshold in automated test suites prior to certifying any release candidate branch.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "QAE-02",
            "category": "Release Signoff Gating",
            "policy_name": "Quality Assurance Gating & Release Signoff SOP",
            "source_doc_id": "SOP-QA-01",
            "source_section": "Section 2.1 - Zero Sev-1 Open Bug Gate",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Production Blocker Defect Policy",
            "task_description": "Block production deployments unconditionally if any unmitigated Severity 1 bug or data corruption issue remains open.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "QAE-03",
            "category": "Automated Security Gating",
            "policy_name": "Secure Software Development Lifecycle (SSDLC) SOP",
            "source_doc_id": "SOP-DEV-01",
            "source_section": "Section 2.3 - DAST Automated API Scans",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Week 1",
            "assessment_topic": "DAST Staging Security Scans",
            "task_description": "Execute automated OWASP ZAP dynamic API security test suites against staging builds prior to production release approval.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "QAE-04",
            "category": "Canary Verification",
            "policy_name": "Cloud Production Deployment & Automated Rollback SOP",
            "source_doc_id": "SOP-DEV-02",
            "source_section": "Section 2.1 - Synthetic Smoke Test Validation",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Week 1",
            "assessment_topic": "Canary Smoke Testing",
            "task_description": "Run automated synthetic end-to-end smoke tests during the 15-minute Canary deployment window to detect early functional regressions.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "QAE-05",
            "category": "Test Data Privacy",
            "policy_name": "Data Privacy and Encryption Policy",
            "source_doc_id": "POL-SEC-02",
            "source_section": "Section 2.1 - Synthetic Data Generation in Staging",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Non-Production PII Masking",
            "task_description": "Ensure QA staging test suites strictly utilize synthetic or anonymized datasets; cloning production customer PII to QA environments is strictly forbidden.",
            "conflict_flag": False,
            "conflict_notes": None
        }
    ],
    "ROLE-DVO-08": [
        {
            "spec_id": "DVO-01",
            "category": "Deployment Operations",
            "policy_name": "Cloud Production Deployment & Automated Rollback SOP",
            "source_doc_id": "SOP-DEV-02",
            "source_section": "Section 1.1 - Blue-Green Kubernetes Deployments",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Zero-Downtime Deployment Pipelines",
            "task_description": "Maintain Kubernetes Blue-Green deployment pipelines to ensure seamless, zero-downtime releases with automated canary traffic routing.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "DVO-02",
            "category": "Deployment Safety",
            "policy_name": "Cloud Production Deployment & Automated Rollback SOP",
            "source_doc_id": "SOP-DEV-02",
            "source_section": "Section 2.2 - 2% Error Rate Automated Rollback Gate",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Automated Canary Rollback Triggers",
            "task_description": "Configure Prometheus metrics triggers to automatically execute zero-downtime rollbacks if HTTP 5xx error rate exceeds 2.0% across a 5-minute rolling window.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "DVO-03",
            "category": "Secret Lifecycle Management",
            "policy_name": "Cryptographic Key Management & Secret Rotation SOP",
            "source_doc_id": "POL-SEC-05",
            "source_section": "Section 3.1 - 90-Day Vault Automated Secret Rotation",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Week 1",
            "assessment_topic": "HashiCorp Vault Dynamic Secrets",
            "task_description": "Configure HashiCorp Vault engines to enforce automated 90-day secret rotations across database credentials, API tokens, and TLS certificates.",
            "conflict_flag": True,
            "conflict_notes": "Overrides FAQ-SEC-01 manual annual rotation guidance."
        },
        {
            "spec_id": "DVO-04",
            "category": "Infrastructure Encryption",
            "policy_name": "Data Privacy and Encryption Policy",
            "source_doc_id": "POL-SEC-02",
            "source_section": "Section 2.2 - TLS 1.3 In-Transit Enforcement",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Ingress TLS Protocol Hardening",
            "task_description": "Enforce TLS 1.3 across all Kubernetes ingress controllers, CloudFront distributions, and API gateways, explicitly disabling legacy TLS 1.0 and 1.1.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "DVO-05",
            "category": "IAM Access Revocation Automation",
            "policy_name": "Employee Offboarding & Hardware Asset Recovery SOP",
            "source_doc_id": "SOP-OPS-02",
            "source_section": "Section 1.1 - Automated SSO SCIM De-provisioning",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Week 1",
            "assessment_topic": "Automated IAM Offboarding Webhooks",
            "task_description": "Maintain automated SCIM/Terraform pipelines to instantly revoke cloud IAM and Kubernetes cluster credentials within 15 minutes of offboarding events.",
            "conflict_flag": False,
            "conflict_notes": None
        }
    ],
    "ROLE-SEC-09": [
        {
            "spec_id": "SEC-06",
            "category": "Incident Response",
            "policy_name": "Incident Response and Breach Notification Policy",
            "source_doc_id": "POL-SEC-03",
            "source_section": "Section 2.1 - 24-Hour Statutory Breach Notification",
            "doc_version": "v1.1",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Statutory Data Breach Timelines",
            "task_description": "Lead incident triage and ensure formal regulatory and customer breach notifications execute within the statutory 24-hour SLA.",
            "conflict_flag": True,
            "conflict_notes": "Supersedes POL-SEC-03 v1.0 72-hour window."
        },
        {
            "spec_id": "SEC-07",
            "category": "Authentication Security",
            "policy_name": "Information Security Policy",
            "source_doc_id": "POL-SEC-01",
            "source_section": "Section 2.2 - Prohibition of SMS OTP",
            "doc_version": "v2.1",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Hardware MFA Enforcement & Audit",
            "task_description": "Audit identity provider logs to ensure 100% hardware MFA (FIDO2/YubiKey) compliance and verify complete deprecation of SMS-based OTP.",
            "conflict_flag": True,
            "conflict_notes": "Supersedes POL-SEC-01 v1.0."
        },
        {
            "spec_id": "SEC-08",
            "category": "Vulnerability Management",
            "policy_name": "Secure Software Development Lifecycle (SSDLC) SOP",
            "source_doc_id": "SOP-DEV-01",
            "source_section": "Section 2.1 - SAST / DAST Policy Enforcement",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Week 1",
            "assessment_topic": "Pipeline Security Policy Enforcement",
            "task_description": "Maintain SonarQube quality profiles and block any software release containing unresolved Critical/Blocker CVEs.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "SEC-09",
            "category": "Vendor Security Assessment",
            "policy_name": "Vendor Procurement, Bidding, and Contracting SOP",
            "source_doc_id": "SOP-FIN-02",
            "source_section": "Section 2.3 - Third-Party Vendor Security Audits",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Month 1",
            "assessment_topic": "Vendor SOC 2 & Security Reviews",
            "task_description": "Review SOC 2 Type II reports and run third-party vendor risk assessments for all proposed software vendors before commercial contract execution.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "SEC-10",
            "category": "Secret Hygiene Audit",
            "policy_name": "Cryptographic Key Management & Secret Rotation SOP",
            "source_doc_id": "POL-SEC-05",
            "source_section": "Section 3.1 - 90-Day Key Rotation Compliance",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Month 1",
            "assessment_topic": "Vault Cryptographic Rotation Audits",
            "task_description": "Conduct automated monthly audits of HashiCorp Vault lease expirations to ensure no active secret exceeds the 90-day lifecycle limit.",
            "conflict_flag": False,
            "conflict_notes": None
        }
    ],
    "ROLE-PRM-10": [
        {
            "spec_id": "PRM-01",
            "category": "Product Compliance",
            "policy_name": "Data Privacy and Encryption Policy",
            "source_doc_id": "POL-SEC-02",
            "source_section": "Section 3.1 - Privacy by Design & 30-Day Erasure",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Day 1",
            "assessment_topic": "Privacy-by-Design Feature Specs",
            "task_description": "Incorporate GDPR/CCPA Privacy-by-Design specifications and automated 30-day customer data erasure workflows into all new product PRDs.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "PRM-02",
            "category": "Product Release Gating",
            "policy_name": "Quality Assurance Gating & Release Signoff SOP",
            "source_doc_id": "SOP-QA-01",
            "source_section": "Section 2.1 - Zero Sev-1 Defect Signoff",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "Critical",
            "due_stage": "Week 1",
            "assessment_topic": "Feature Acceptance & Release Criteria",
            "task_description": "Ensure feature launch sign-off adheres strictly to zero Sev-1 open bugs and 80% automated test coverage gates.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "PRM-03",
            "category": "Third-Party Tool Procurement",
            "policy_name": "Vendor Procurement, Bidding, and Contracting SOP",
            "source_doc_id": "SOP-FIN-02",
            "source_section": "Section 2.1 - Product Analytics Tooling RFP",
            "doc_version": "v1.0",
            "is_mandatory": False,
            "priority": "Medium",
            "due_stage": "Quarter 1",
            "assessment_topic": "Product SaaS RFP Bidding",
            "task_description": "Execute 3-vendor competitive RFP evaluations for third-party product telemetry, feature-flagging, or customer survey tooling exceeding $25k ACV.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "PRM-04",
            "category": "Performance Reviews & OKRs",
            "policy_name": "Employee Performance Management Policy",
            "source_doc_id": "POL-HR-04",
            "source_section": "Section 2.1 - Quarterly OKR Alignment",
            "doc_version": "v1.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Quarter 1",
            "assessment_topic": "Quarterly Product OKR Cadence",
            "task_description": "Define and align quarterly cross-functional Product OKRs in accordance with corporate performance management cycles.",
            "conflict_flag": False,
            "conflict_notes": None
        },
        {
            "spec_id": "PRM-05",
            "category": "Customer Outage Communication",
            "policy_name": "Customer Support Ticket Escalation Matrix",
            "source_doc_id": "SOP-SUP-01",
            "source_section": "Section 1.1 - Sev-1 Product Communications",
            "doc_version": "v2.0",
            "is_mandatory": True,
            "priority": "High",
            "due_stage": "Day 1",
            "assessment_topic": "Major Incident Status Page Management",
            "task_description": "Coordinate customer-facing status page updates and post-incident communications during Severity 1 platform outages with Support and Engineering.",
            "conflict_flag": False,
            "conflict_notes": None
        }
    ]
}

# Build Master Matrix
all_requirements = []
req_counter = 1

for role_obj in roles:
    r_id = role_obj["role_id"]
    r_name = role_obj["role_name"]

    # 1. Add 15 company-wide baseline requirements for this role
    for base in company_wide_templates:
        req_item = {
            "req_id": f"REQ-{req_counter:03d}",
            "role_id": r_id,
            "role_name": r_name,
            "category": base["category"],
            "policy_name": base["policy_name"],
            "source_doc_id": base["source_doc_id"],
            "source_section": base["source_section"],
            "doc_version": base["doc_version"],
            "is_mandatory": base["is_mandatory"],
            "priority": base["priority"],
            "due_stage": base["due_stage"],
            "assessment_topic": base["assessment_topic"],
            "task_description": base["task_description"],
            "conflict_flag": base["conflict_flag"],
            "conflict_notes": base["conflict_notes"]
        }
        all_requirements.append(req_item)
        req_counter += 1

    # 2. Add 5 role-specific requirements for this role
    for spec in role_specific_templates[r_id]:
        req_item = {
            "req_id": f"REQ-{req_counter:03d}",
            "role_id": r_id,
            "role_name": r_name,
            "category": spec["category"],
            "policy_name": spec["policy_name"],
            "source_doc_id": spec["source_doc_id"],
            "source_section": spec["source_section"],
            "doc_version": spec["doc_version"],
            "is_mandatory": spec["is_mandatory"],
            "priority": spec["priority"],
            "due_stage": spec["due_stage"],
            "assessment_topic": spec["assessment_topic"],
            "task_description": spec["task_description"],
            "conflict_flag": spec["conflict_flag"],
            "conflict_notes": spec["conflict_notes"]
        }
        all_requirements.append(req_item)
        req_counter += 1

# Save dataset/role_matrix.json and dataset/role_requirement_matrix.json
with open("dataset/role_matrix.json", "w", encoding="utf-8") as f:
    json.dump(all_requirements, f, indent=2)

with open("dataset/role_requirement_matrix.json", "w", encoding="utf-8") as f:
    json.dump(all_requirements, f, indent=2)

# Count metrics
total_reqs = len(all_requirements)
mandatory_count = sum(1 for r in all_requirements if r["is_mandatory"])
conflict_count = sum(1 for r in all_requirements if r["conflict_flag"])

print(f"Generated Master Requirement Matrix:")
print(f"- Total Requirement Objects: {total_reqs}")
print(f"- Total Mandatory Requirements: {mandatory_count}")
print(f"- Total Conflict Flagged Items: {conflict_count}")
print(f"- Distinct Roles Covered: {len(roles)}")
