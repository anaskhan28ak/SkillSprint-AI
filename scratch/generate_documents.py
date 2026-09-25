import os
import json

# Ensure target directories
os.makedirs("dataset/raw_documents", exist_ok=True)
os.makedirs("dataset/roles", exist_ok=True)

# ==============================================================================
# 20 CORPORATE DOCUMENTS FOR APEX GLOBAL SOLUTIONS
# ==============================================================================
documents = {
    "POL-HR-01_Global_Code_of_Conduct_v1.0.txt": """APEX GLOBAL SOLUTIONS
POLICY DOCUMENT: POL-HR-01
TITLE: Global Code of Conduct & Corporate Ethics
VERSION: 1.0
EFFECTIVE DATE: January 1, 2024
CLASSIFICATION: Internal - Mandatory for All Employees

1. PURPOSE & APPLICABILITY
Apex Global Solutions ("Apex") is committed to upholding the highest standards of integrity, transparency, and ethical conduct. This policy applies to all full-time, part-time, temporary personnel, contractors, and executive leadership across all subsidiaries.

2. EQUAL OPPORTUNITY & NON-HARASSMENT
2.1 Apex provides equal opportunity employment regardless of race, gender, religion, national origin, disability, or age.
2.2 Zero tolerance for discrimination, workplace harassment, bullying, or retaliatory behaviors. All incidents must be reported directly to HR or via the Anonymous Ethics Hotline.

3. CONFLICTS OF INTEREST & OUTSIDE EMPLOYMENT
3.1 Employees must avoid any activity, investment, or association that interferes with their ability to exercise independent judgment in the best interests of Apex.
3.2 Secondary employment or freelance consulting with direct competitors, suppliers, or client organizations is strictly prohibited without prior written approval from the Chief Legal Officer.

4. GIFTS, ENTERTAINMENT & ANTI-BRIBERY
4.1 Apex strictly complies with the Foreign Corrupt Practices Act (FCPA) and international anti-bribery regulations. Bribes, kickbacks, or facilitation payments are unconditionally prohibited.
4.2 Permissible Business Gifts: Employees may accept or give customary business gifts of nominal value. Any gift, entertainment, or hospitality exceeding a fair market value of $50 USD must be formally reported and registered with the Corporate Ethics & Compliance Committee within 5 business days of receipt.
4.3 Cash or cash-equivalent gifts (e.g., gift cards, prepaid debit cards) of any amount are strictly prohibited.

5. PROTECTION OF COMPANY ASSETS & CONFIDENTIALITY
5.1 Company intellectual property, trade secrets, software codebases, and customer lists must remain strictly confidential during and after employment tenure.
5.2 Company computing equipment is provided for business purposes. Incidental personal use is permitted provided it does not violate security standards.

6. COMPLIANCE VIOLATIONS
Failure to comply with this policy will result in disciplinary action up to and including immediate termination of employment and civil or criminal prosecution.
""",

    "POL-HR-02_Remote_and_Hybrid_Work_Policy_v2.0.txt": """APEX GLOBAL SOLUTIONS
POLICY DOCUMENT: POL-HR-02
TITLE: Remote and Hybrid Work Policy
VERSION: 2.0 (SUPERSEDES VERSION 1.0)
EFFECTIVE DATE: March 15, 2024
CLASSIFICATION: Internal - Mandatory for Remote & Hybrid Personnel

1. PURPOSE & SCOPE
Apex Global Solutions embraces a modern, flexible distributed workforce model. This policy defines the operational guidelines, equipment allowances, and core collaboration expectations for hybrid and fully remote team members.

2. CORE OPERATING HOURS & AVAILABILITY
2.1 Collaboration Window: All remote personnel across regional timezones must maintain active presence on official communication channels (Slack, Microsoft Teams, and email) during the mandatory Core Operating Hours of 10:00 AM to 4:00 PM PKT (Pakistan Standard Time) / UTC+5.
2.2 Scheduled Synchronous Meetings: Team standups, cross-functional sprints, and customer escalation calls are scheduled within core operating hours to ensure rapid coordination.
2.3 Version Update Note: This version supersedes Policy v1.0, which previously defined core availability hours as 9:00 AM to 6:00 PM PKT.

3. HOME WORKSTATION & ERGONOMIC ALLOWANCE
3.1 Stipend Allocation: Active full-time remote employees are eligible for a one-time home-office setup stipend of $300 USD upon onboarding.
3.2 Reimbursable Items: The stipend may be applied toward ergonomic chairs, external monitors, keyboards, desk lighting, and surge protectors. Itemized purchase receipts must be submitted via the Expensify portal within 60 days of hire.
3.3 Version Update Note: This version supersedes Policy v1.0, which provided an allowance of $200 USD.

4. NETWORK SECURITY & WORKSPACE ENVIRONMENT
4.1 Remote employees must connect to corporate infrastructure exclusively using company-managed laptops configured with enterprise VPN and endpoint protection.
4.2 Use of public, unencrypted Wi-Fi networks without an active VPN tunnel is strictly forbidden.
4.3 Screen privacy filters must be used when working in shared co-working spaces or public environments.
""",

    "POL-HR-03_Annual_Paid_Time_Off_and_Leave_Policy_v1.2.txt": """APEX GLOBAL SOLUTIONS
POLICY DOCUMENT: POL-HR-03
TITLE: Annual Paid Time Off (PTO) and Leave Policy
VERSION: 1.2
EFFECTIVE DATE: February 1, 2024
CLASSIFICATION: Internal - Formal Corporate Policy

1. OVERVIEW & ACCRUAL
Apex Global Solutions provides competitive annual leave benefits to support employee health, well-being, and work-life harmony.

2. ANNUAL LEAVE ALLOCATION
2.1 All full-time employees accrue 20 business days of paid time off (PTO) per calendar year, accrued pro-rata at 1.67 days per completed month of service.
2.2 Leave must be requested via the HRIS portal with at least 5 business days advance notice for planned absences exceeding 3 consecutive days.

3. ANNUAL CARRY-OVER RESTRICTIONS & EXPIRATION
3.1 Maximum Carry-Over Cap: An employee may carry over a maximum of 5 unused leave days into the subsequent calendar year.
3.2 Forfeiture of Excess Leave: Any accumulated leave balance exceeding the 5-day carry-over threshold as of December 31st 23:59 PKT will be automatically forfeited without financial compensation or buyout options.
3.3 Carry-over days must be utilized within the first quarter (Q1 - January 1 to March 31) of the new calendar year.
3.4 Policy Hierarchy Precedence Note: This formal policy document (POL-HR-03 v1.2) represents the sole binding corporate standard and strictly overrides any conflicting departmental FAQ pages, intranet articles, or oral representations (such as outdated statements in FAQ-HR-01).

4. SICK LEAVE & SPECIAL EMERGENCIES
4.1 Employees are allocated 10 days of paid sick leave annually. Absences exceeding 3 consecutive business days require a verified medical certificate.
""",

    "POL-HR-04_Employee_Performance_and_PIP_Policy_v1.0.txt": """APEX GLOBAL SOLUTIONS
POLICY DOCUMENT: POL-HR-04
TITLE: Employee Performance Management & Improvement Policy
VERSION: 1.0
EFFECTIVE DATE: January 1, 2024
CLASSIFICATION: Internal - All Departments

1. PURPOSE
This policy governs the continuous performance evaluation cycle, Objective & Key Result (OKR) reviews, and formal remedial procedures for underperformance.

2. PERFORMANCE REVIEW CADENCE
2.1 Evaluations occur on a quarterly cadence (Q1, Q2, Q3, Q4) with a comprehensive annual performance appraisal.
2.2 Employees are scored on a standardized 1.0 to 5.0 rating scale across Technical Execution, Collaboration, and Core Values.

3. PERFORMANCE IMPROVEMENT PLAN (PIP) CRITERIA
3.1 A formal 60-day Performance Improvement Plan (PIP) is mandatory for any employee who receives an overall performance rating below 2.5 out of 5.0 across two consecutive quarterly cycles.
3.2 PIP Requirements: The People Partner and direct People Manager must establish clear, measurable weekly milestones.
3.3 Outcomes: If the employee successfully meets all milestone benchmarks within 60 days, they return to standard standing. Failure to achieve a minimum 2.5 rating at the conclusion of the 60-day PIP will result in employment termination.
""",

    "POL-SEC-01_Information_Security_Policy_v2.1.txt": """APEX GLOBAL SOLUTIONS
POLICY DOCUMENT: POL-SEC-01
TITLE: Information Security and Access Management Policy
VERSION: 2.1 (SUPERSEDES VERSION 1.0)
EFFECTIVE DATE: April 10, 2024
CLASSIFICATION: Confidential - Mandatory for All Systems & Personnel

1. PURPOSE & PRINCIPLES
Apex enforces a Zero-Trust architecture to safeguard corporate systems, confidential repositories, and customer data assets against cyber threats.

2. AUTHENTICATION STANDARDS & PASSWORD COMPLEXITY
2.1 Multi-Factor Authentication (MFA): Mandatory hardware-based MFA (FIDO2 / YubiKey physical security keys or enterprise WebAuthn authenticators) is required for accessing all corporate SSO systems, VPNs, cloud consoles (AWS/GCP), and internal tools.
2.2 Deprecated Authentication Methods: Legacy SMS-based OTP and unauthenticated email codes are strictly prohibited and disabled at the identity provider tier.
2.3 Password Complexity: Master passphrases must contain a minimum of 14 characters, including at least one uppercase letter, one lowercase letter, one number, and one non-alphanumeric symbol. Passwords must not be reused across the last 12 historical cycles.
2.4 Version Update Note: Supersedes POL-SEC-01 v1.0, which previously allowed 10-character passwords and SMS OTP.

3. WORKSTATION AUTO-LOCK & ENDPOINT SECURITY
3.1 Unattended Workstations: All company laptops and workstations must automatically lock screens with password/biometric lock after a maximum of 5 minutes of inactivity.
3.2 Full Disk Encryption: BitLocker (Windows) or FileVault (macOS) with AES-256 encryption is mandatory on all corporate endpoints.
""",

    "POL-SEC-02_Data_Privacy_and_Encryption_Policy_v1.0.txt": """APEX GLOBAL SOLUTIONS
POLICY DOCUMENT: POL-SEC-02
TITLE: Data Privacy, Protection, and Cryptographic Standards
VERSION: 1.0
EFFECTIVE DATE: January 1, 2024
CLASSIFICATION: Confidential - Compliance & Technical Standard

1. JURISDICTION & COMPLIANCE
Apex complies with the General Data Protection Regulation (GDPR), California Consumer Privacy Act (CCPA), and SOC 2 Type II data privacy trust principles.

2. CRYPTOGRAPHIC ENCRYPTION STANDARDS
2.1 Data at Rest: All structured databases, relational stores, object storage (S3/GCS buckets), and persistent disks storing customer or PII data must be encrypted using AES-256 encryption.
2.2 Data in Transit: All external and internal service-to-service communications must be encrypted using Transport Layer Security (TLS) version 1.3. TLS 1.0 and 1.1 are explicitly disabled.

3. DATA SUBJECT RIGHTS & ERASURE SLA
3.1 Right to Erasure / Deletion: When a verified customer data subject request (DSR) or "Right to be Forgotten" ticket is logged, all associated customer PII across production and staging databases must be irreversibly purged within a strict 30-day SLA window.
3.2 Audit Log Retention: Audit and access logs must be retained in immutable append-only storage for a minimum duration of 365 days.
""",

    "POL-SEC-03_Incident_Response_and_Breach_Notification_v1.1.txt": """APEX GLOBAL SOLUTIONS
POLICY DOCUMENT: POL-SEC-03
TITLE: Incident Response and Mandatory Breach Notification Policy
VERSION: 1.1 (SUPERSEDES VERSION 1.0)
EFFECTIVE DATE: March 1, 2024
CLASSIFICATION: Confidential - Security Operations Standard

1. INCIDENT CLASSIFICATION
Security incidents are triaged into Severity Levels:
- Severity 1 (Critical): Active data exfiltration, ransomware, or compromise of production credential stores.
- Severity 2 (High): Unauthorized lateral movement, compromised non-privileged account.
- Severity 3 (Medium): Malware contained on isolated endpoint.

2. MANDATORY DATA BREACH REPORTING SLA
2.1 Statutory Breach Notification: In the event of a confirmed breach involving Personal Identifiable Information (PII) or customer credential compromise, the Security Operations Lead and CISO must formally notify relevant regulatory authorities and affected customers within 24 hours of confirmation.
2.2 Version Update Note: Supersedes POL-SEC-03 v1.0, which previously allowed a 72-hour notification window.
2.3 Internal Escalation: Any employee discovering suspected compromise must page the SecOps on-call team via the `#security-emergency` channel within 15 minutes.
""",

    "POL-SEC-04_Physical_Clean_Desk_Policy_v1.0_OBSOLETE.txt": """APEX GLOBAL SOLUTIONS
POLICY DOCUMENT: POL-SEC-04
TITLE: Physical Clean Desk and Printed Document Storage Policy
VERSION: 1.0 [STATUS: OBSOLETE / DEPRECATED]
EFFECTIVE DATE: January 1, 2021
DEPRECATION DATE: January 1, 2024
CLASSIFICATION: Archived - Historical Reference Only

[NOTICE OF DEPRECATION]
This policy (POL-SEC-04 v1.0) has been declared OBSOLETE and fully superseded by POL-SEC-01 v2.1 and POL-SEC-02 v1.0. All Apex offices operate on 100% paperless digital workflows. Physical key lockboxes for paper files are discontinued. Workstation digital auto-lock (5 minutes) and BitLocker disk encryption govern modern workplace endpoint security.
""",

    "POL-SEC-05_Key_Management_and_Secret_Rotation_SOP_v2.0.txt": """APEX GLOBAL SOLUTIONS
SOP DOCUMENT: POL-SEC-05 / SOP-SEC-05
TITLE: Cryptographic Key Management & Secret Rotation SOP
VERSION: 2.0 (SUPERSEDES VERSION 1.0)
EFFECTIVE DATE: April 1, 2024
CLASSIFICATION: Confidential - DevOps & SecOps Standard

1. PURPOSE
Defines lifecycle management, custody, and automated rotation for cryptographic keys, API credentials, and database passwords.

2. SECRET REPOSITORY & CUSTODY
2.1 HashiCorp Vault is the exclusive enterprise secrets management repository. Committing credentials, tokens, or private keys to source control (Git) is strictly prohibited and monitored via automated pre-commit scanning hooks.

3. ROTATION FREQUENCY & AUTOMATION
3.1 Automated 90-Day Rotation: All production database master passwords, service-to-service API tokens, SSH root keys, and TLS certificates must be automatically rotated every 90 days via Vault automated secret engines.
3.2 Emergency Revocation: Any suspected token leakage requires immediate revocation within 15 minutes and issuance of rotated credentials.
3.3 Precedence Note: This SOP overrides outdated portal FAQ (FAQ-SEC-01) references suggesting annual manual secret rotations.
""",

    "SOP-SUP-01_Customer_Ticket_Escalation_Matrix_v2.0.txt": """APEX GLOBAL SOLUTIONS
SOP DOCUMENT: SOP-SUP-01
TITLE: Customer Support Ticket Escalation & Incident Matrix
VERSION: 2.0 (SUPERSEDES VERSION 1.0)
EFFECTIVE DATE: March 1, 2024
CLASSIFICATION: Internal - Customer Support & Engineering

1. SEVERITY DEFINITIONS & RESPONSE THRESHOLDS
1.1 Severity 1 (Sev-1: Critical Platform Outage): Core platform down, payment processing failing, or multiple enterprise tenants unable to authenticate.
1.2 Severity 2 (Sev-2: Major Degradation): Major feature unavailable with no immediate workaround.
1.3 Severity 3 (Sev-3: Minor Issue / General Inquiry): Non-blocking bug or configuration question.

2. MANDATORY ESCALATION SLA THRESHOLDS
2.1 Sev-1 Escalation Window: Any unacknowledged Severity 1 customer ticket must be escalated to the On-Call Engineering Incident Commander within exactly 15 minutes of ticket creation.
2.2 Automated Executive Paging: Breaching the 15-minute threshold automatically alerts the VP of Customer Experience and Director of Platform Engineering.
2.3 Version Update Note: Supersedes SOP-SUP-01 v1.0, which previously allowed a 30-minute escalation threshold.
""",

    "SOP-SUP-02_Customer_Refund_and_Credit_Authorization_SOP_v1.1.txt": """APEX GLOBAL SOLUTIONS
SOP DOCUMENT: SOP-SUP-02
TITLE: Customer Billing Dispute & Refund Authorization SOP
VERSION: 1.1
EFFECTIVE DATE: February 15, 2024
CLASSIFICATION: Internal - Customer Support & Billing

1. PURPOSE
Establishes clear financial authorization limits for customer billing adjustments, service credits, and invoice refunds.

2. TIERED REFUND APPROVAL LIMITS
2.1 Tier 1 (Support Representative / L1): Authorized to issue goodwill billing credits up to $100 USD per customer account per billing quarter.
2.2 Tier 2 (Senior Support / L2 Specialist): Authorized to issue customer refunds or credits up to a maximum cap of $500 USD per ticket without prior management escalation.
2.3 Tier 3 (Support Manager / Lead): Required for refund amounts exceeding $500 USD up to $2,500 USD.
2.4 Tier 4 (VP / Finance Director): Required for refund amounts exceeding $2,500 USD.
2.5 Precedence Note: This SOP governs customer dispute compensation and supersedes general company expense procedures (SOP-FIN-01) for external customer adjustments.
""",

    "SOP-FIN-01_Employee_Travel_and_Expense_Reimbursement_SOP_v1.0.txt": """APEX GLOBAL SOLUTIONS
SOP DOCUMENT: SOP-FIN-01
TITLE: Employee Travel & Expense Reimbursement SOP
VERSION: 1.0
EFFECTIVE DATE: January 1, 2024
CLASSIFICATION: Internal - Finance & All Employees

1. EXPENSE REIMBURSEMENT POLICY
Apex reimburses employees for reasonable, necessary business travel and operational expenditures incurred during approved company activities.

2. MEAL PER DIEM & CAPS
2.1 Daily Meal Cap: Business travel meal expenditures are capped at a strict maximum of $75 USD per diem. Alcohol is non-reimbursable unless part of an authorized client entertainment dinner.
2.2 Receipt Requirements: Itemized receipts are mandatory for all individual expense claims exceeding $25 USD.

3. MANAGEMENT APPROVAL THRESHOLDS
3.1 Standard Claims: Expense reports under $1,000 USD require direct Manager approval.
3.2 High-Value Claims: Any single expense line item or cumulative monthly report exceeding $1,000 USD requires formal secondary approval from the Department Vice President and Finance Controller.
""",

    "SOP-FIN-02_Vendor_Procurement_and_Bidding_SOP_v1.0.txt": """APEX GLOBAL SOLUTIONS
SOP DOCUMENT: SOP-FIN-02
TITLE: Vendor Procurement, Bidding, and Contracting SOP
VERSION: 1.0
EFFECTIVE DATE: January 1, 2024
CLASSIFICATION: Internal - Procurement & Department Leads

1. PURPOSE
Governs competitive procurement, vendor evaluation, and commercial contract commitments for software, hardware, and professional services.

2. COMPETITIVE BIDDING MANDATES
2.1 Purchase Thresholds: Any software subscription, SaaS tooling, infrastructure contract, or professional service engagement exceeding $25,000 USD in annual contract value (ACV) requires a formal Request for Proposal (RFP) process with a minimum of 3 independent, competitive vendor bids.
2.2 Sole Source Justification: Sole-source contracts above $25,000 USD require written justification and sign-off by the Chief Financial Officer.
2.3 Vendor Risk Assessment: All prospective technology vendors must pass a Security & Privacy Vendor Assessment before contract execution.
""",

    "SOP-DEV-01_Secure_Software_Development_Lifecycle_SOP_v2.0.txt": """APEX GLOBAL SOLUTIONS
SOP DOCUMENT: SOP-DEV-01
TITLE: Secure Software Development Lifecycle (SSDLC) SOP
VERSION: 2.0 (SUPERSEDES VERSION 1.0)
EFFECTIVE DATE: April 1, 2024
CLASSIFICATION: Confidential - Engineering & Security

1. SECURE CODE REVIEW PROTOCOL
1.1 Pull Request Peer Reviews: All pull requests targeting protected branches (`main`, `master`, `release/*`) must receive mandatory code reviews and approvals from at least 2 independent peer engineers. Single-engineer approvals are blocked by repository rule sets.
1.2 Version Update Note: Supersedes SOP-DEV-01 v1.0, which previously required only 1 peer reviewer.

2. AUTOMATED SECURITY GATES & SAST/DAST
2.1 Static Analysis (SAST): SonarQube scans must pass with zero Blocker or Critical vulnerabilities.
2.2 Software Composition Analysis (SCA): Dependabot / Snyk scans must report zero known High/Critical CVEs in open-source dependencies.
2.3 Dynamic Analysis (DAST): Automated OWASP ZAP API scans must execute in staging prior to production deployment.
2.4 Client-Side Input Sanitization: All user-supplied DOM input must be sanitized via DOMPurify to eliminate Cross-Site Scripting (XSS).
""",

    "SOP-DEV-02_Cloud_Production_Deployment_and_Rollback_SOP_v1.0.txt": """APEX GLOBAL SOLUTIONS
SOP DOCUMENT: SOP-DEV-02
TITLE: Cloud Production Deployment & Automated Rollback SOP
VERSION: 1.0
EFFECTIVE DATE: January 1, 2024
CLASSIFICATION: Confidential - DevOps & Platform Engineering

1. DEPLOYMENT ARCHITECTURE
1.1 Zero-Downtime Blue-Green: All production releases must execute via automated Kubernetes Blue-Green or progressive Canary deployment pipelines. Direct in-place server updates are prohibited.

2. AUTOMATED ROLLBACK GATES
2.1 Error Rate Metric: Real-time Prometheus/Datadog monitoring evaluates HTTP 5xx error rates across the Canary/Green environment for 15 minutes post-traffic shift.
2.2 Rollback Trigger: If the HTTP 5xx error rate exceeds 2.0% of total request volume over any 5-minute rolling window, the deployment automation must trigger an immediate, automated zero-downtime rollback to the stable Blue environment.
2.3 Post-Mortem Requirement: Any deployment rollback mandates an internal blameless post-mortem published within 48 hours.
""",

    "SOP-OPS-01_Workplace_Security_and_Visitor_Access_SOP_v1.0.txt": """APEX GLOBAL SOLUTIONS
SOP DOCUMENT: SOP-OPS-01
TITLE: Physical Workplace Security & Visitor Access SOP
VERSION: 1.0
EFFECTIVE DATE: January 1, 2024
CLASSIFICATION: Internal - Workplace Operations & Facilities

1. FACILITY ACCESS CONTROL
1.1 All employees must display active RFID corporate access badges at all times within facility premises. Tailgating is strictly prohibited.

2. VISITOR MANAGEMENT PROTOCOL
2.1 Visitor Registration: All external visitors, contractors, and guests must present government-issued photo ID, sign the digital Visitor NDA, and receive a color-coded Visitor Badge at the reception desk.
2.2 Mandatory Escort: Visitors must remain accompanied by an authorized Apex employee escort at all times while present in non-public office zones and engineering floors.
""",

    "SOP-OPS-02_Employee_Asset_Recovery_and_Offboarding_SOP_v1.0.txt": """APEX GLOBAL SOLUTIONS
SOP DOCUMENT: SOP-OPS-02
TITLE: Employee Offboarding & Hardware Asset Recovery SOP
VERSION: 1.0
EFFECTIVE DATE: January 1, 2024
CLASSIFICATION: Confidential - HR, IT & Operations

1. SYSTEM ACCESS REVOCATION
1.1 Immediate SSO De-provisioning: Upon receipt of formal employee separation notice or immediate termination notice, IT SecOps must execute automated Okta/Google SSO account revocation within exactly 15 minutes.

2. HARDWARE RECOVERY PROTOCOL
2.1 48-Hour Return Window: Departing employees must return all company-issued laptops, YubiKeys, monitors, and corporate assets to the IT Operations department within 48 hours of their final working day.
2.2 Remote Return Kits: Prepaid secure courier boxes are dispatched to remote personnel on their final week. Unreturned equipment is subject to legal recovery.
""",

    "FAQ-HR-01_Leave_and_Benefits_Knowledge_Base_FAQ_v1.0.txt": """APEX GLOBAL SOLUTIONS
KNOWLEDGE BASE FAQ: FAQ-HR-01
TITLE: Employee Leave & Benefits Portal FAQ
VERSION: 1.0 (OUTDATED / INFORMAL GUIDE)
DATE: August 15, 2022
CLASSIFICATION: Internal - General Knowledge Base

[CONTRADICTION & OBSOLESCENCE WARNING]
Question: How many unused annual leave days can I roll over into next year?
Answer: Employees can roll over up to 10 days of unused leave to the following calendar year.

[LEGAL NOTE / CONFLICT PRECEDENCE RULE]
Note: This FAQ document is an informal employee intranet summary. Per company governance standards, formal Policy Document POL-HR-03 v1.2 takes legal precedence. POL-HR-03 v1.2 strictly limits annual leave rollover to a maximum of 5 days.
""",

    "FAQ-SEC-01_Remote_Access_and_VPN_Troubleshooting_FAQ_v1.0.txt": """APEX GLOBAL SOLUTIONS
KNOWLEDGE BASE FAQ: FAQ-SEC-01
TITLE: Remote Access, Hardware Tokens & VPN Troubleshooting FAQ
VERSION: 1.0 (INFORMAL KB GUIDE)
DATE: January 10, 2023
CLASSIFICATION: Internal - IT Helpdesk FAQ

Question: What should I do if my YubiKey hardware token is not recognized by the laptop?
Answer: 1. Unplug and re-insert into a direct USB-C port (avoid unpowered USB hubs). 2. Ensure Chrome WebAuthn permissions are granted. 3. If the token remains unresponsive, contact SecOps on Slack `#it-helpdesk` for emergency session bypass.

[SECRET ROTATION NOTE / CONFLICT WARNING]
Question: How often do developers need to change database secrets?
Answer: We recommend manually changing passwords roughly once every year.
[PRECEDENCE NOTE]: Overridden by POL-SEC-05 v2.0 which mandates automated 90-day secret rotation via HashiCorp Vault.
""",

    "SOP-QA-01_Quality_Assurance_and_Release_Signoff_SOP_v1.0.txt": """APEX GLOBAL SOLUTIONS
SOP DOCUMENT: SOP-QA-01
TITLE: Quality Assurance Gating & Release Signoff SOP
VERSION: 1.0
EFFECTIVE DATE: January 1, 2024
CLASSIFICATION: Internal - QA & Software Engineering

1. CODE COVERAGE GATES
1.1 Minimum Test Coverage: Automated unit, integration, and API test coverage must achieve a minimum threshold of 80.0% code line coverage across all newly committed code before a release candidate can be certified.

2. RELEASE BLOCKER CRITERIA
2.1 Zero Severity 1 Defect Tolerance: A production release build will be unconditionally blocked from deployment if there is even a single (1) open, unmitigated Severity 1 (Critical) bug or data corruption issue.
2.2 QA Lead Signoff: Formal written sign-off from the QA Lead in Jira Release Hub is mandatory prior to production traffic cutover.
"""
}

# Write all 20 documents
for filename, content in documents.items():
    path = os.path.join("dataset/raw_documents", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print(f"Successfully generated {len(documents)} raw policy/SOP documents in dataset/raw_documents/")
