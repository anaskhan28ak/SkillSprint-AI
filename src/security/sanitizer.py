"""Production-Ready Text Sanitizer & Adversarial Prompt Injection Defense Module.

Author: Farhad Khan (Security & Compliance Lead, SkillSprint AI)
Scope: Pre-RAG text sanitization, zero-width stripping, prompt injection detection,
and structural JSON/Markdown payload neutralization.
"""

import base64
import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("SkillSprint.Sanitizer")

# Zero-width, invisible, and bidirectional override characters
ZERO_WIDTH_CHARS_PATTERN = re.compile(
    r"[\u200B\u200C\u200D\u200E\u200F\uFEFF\u202A\u202B\u202C\u202D\u202E\u2060\u00AD]"
)

# High-risk adversarial injection regex patterns
ADVERSARIAL_PATTERNS: List[Tuple[str, str, float]] = [
    # Pattern, Threat Category, Threat Weight
    (r"(?i)\bignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|rules|guidelines)\b", "INSTRUCTION_OVERRIDE", 0.95),
    (r"(?i)\bdisregard\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|rules|guidelines)\b", "INSTRUCTION_OVERRIDE", 0.95),
    (r"(?i)\bforget\s+(all\s+)?(previous|prior|above)\s+(instructions|rules)\b", "INSTRUCTION_OVERRIDE", 0.90),
    (r"(?i)\[\s*system\s*(notice|instruction|command|override)\s*:\s*[^\]]+\]", "SYNTHETIC_SYSTEM_TAG", 0.90),
    (r"(?i)<\s*system\s*>[^<]*<\s*/\s*system\s*>", "XML_SYSTEM_TAG", 0.90),
    (r"(?i)\brepeat\s+your\s+(original\s+)?system\s+prompt\b", "SYSTEM_PROMPT_LEAK", 0.85),
    (r"(?i)\bprint\s+(the\s+)?(system\s+prompt|developer\s+instructions)\b", "SYSTEM_PROMPT_LEAK", 0.85),
    (r"(?i)\breveal\s+(hidden\s+)?(system\s+prompt|guardrail\s+rules|api\s+keys?)\b", "SYSTEM_PROMPT_LEAK", 0.90),
    (r"(?i)\byou\s+are\s+now\s+(operating\s+as|a|an)\s+(unrestricted|freedombot|dan|developer\s+mode)\b", "ROLE_HIJACK", 0.95),
    (r"(?i)\bpretend\s+to\s+be\s+dan\b", "JAILBREAK_DAN", 0.95),
    (r"(?i)\bdo\s+anything\s+now\b", "JAILBREAK_DAN", 0.90),
    (r"(?i)\bdeveloper\s+mode\s+(enabled|on|activated)\b", "JAILBREAK_DEV_MODE", 0.90),
    (r"(?i)\b(unconditionally\s+)?grant(\s+the\s+user)?\s+(full\s+)?(root|admin|administrative)\s+(access|privileges|permissions)\b", "PRIVILEGE_HIJACK", 0.95),
    (r"(?i)\bpass\s+this\s+employee(\s+evaluation)?\s+with\s+(100%|full)\s+score\b", "PAYLOAD_HIJACK", 0.85),
    (r"(?i)\bmark\s+(all\s+)?(150\s+)?requirements\s+as\s+(passed|completed|satisfied)\b", "PAYLOAD_HIJACK", 0.90),
    (r"(?i)\bbypass\s+(all\s+)?(pipeline\s+2\s+)?(python\s+)?validation\b", "VALIDATION_BYPASS", 0.95),
    (r"(?i)\bignore\s+all\s+role\s+matrix\s+checks\b", "VALIDATION_BYPASS", 0.90),
    (r"(?i)===\s*(user\s+prompt\s+completed|system\s+re-initialization|begin\s+new\s+user\s+task)\s*===", "DELIMITER_COLLISION", 0.85),
    (r"(?i)```markdown\s*#\s*system\s+message\s*:\s*emergency\s+bypass", "MARKDOWN_INJECTION", 0.90),
    (r"(?i)\bnote\s+to\s+downstream\s+(pipeline|llm)\s*:\s*", "RECURSIVE_INJECTION", 0.80),
]


class TextSanitizer:
    """Enterprise text sanitization engine for LLM inputs and document parsing."""

    def __init__(self, strict_mode: bool = True) -> None:
        self.strict_mode = strict_mode
        self._compiled_patterns = [
            (re.compile(pat), cat, weight) for pat, cat, weight in ADVERSARIAL_PATTERNS
        ]

    def strip_invisible_characters(self, text: str) -> Tuple[str, int]:
        """Strip zero-width and invisible Unicode characters from input text.

        Returns:
            Tuple of (cleaned_text, count_of_stripped_characters)
        """
        matches = ZERO_WIDTH_CHARS_PATTERN.findall(text)
        cleaned_text = ZERO_WIDTH_CHARS_PATTERN.sub("", text)
        return cleaned_text, len(matches)

    def scan_for_threats(self, text: str) -> Tuple[bool, float, List[str], List[str]]:
        """Scan text for known prompt injection triggers and adversarial directives.

        Returns:
            Tuple of (is_flagged, threat_score, threat_categories, matched_phrases)
        """
        categories = set()
        matched_phrases = []
        max_weight = 0.0
        total_weight = 0.0

        for regex, category, weight in self._compiled_patterns:
            matches = regex.findall(text)
            if matches:
                categories.add(category)
                max_weight = max(max_weight, weight)
                total_weight += weight * len(matches)
                matched_phrases.append(f"{category} ({len(matches)} match)")

        # Check for suspicious Base64 encoded blobs
        b64_threats = self._scan_base64_payloads(text)
        if b64_threats:
            categories.add("ENCODED_PAYLOAD")
            max_weight = max(max_weight, 0.85)
            matched_phrases.extend(b64_threats)

        # Check for structured JSON/YAML injection overrides
        json_threats = self._scan_structural_json(text)
        if json_threats:
            categories.add("STRUCTURAL_JSON_INJECTION")
            max_weight = max(max_weight, 0.90)
            matched_phrases.extend(json_threats)

        is_flagged = len(categories) > 0
        threat_score = min(1.0, max_weight if is_flagged else 0.0)

        return is_flagged, threat_score, sorted(list(categories)), matched_phrases

    def _scan_base64_payloads(self, text: str) -> List[str]:
        """Detect and decode potential base64 prompt injection fragments."""
        threats = []
        # Match base64 tokens of length >= 24
        potential_b64 = re.findall(r"\b[A-Za-z0-9+/]{24,}={0,2}\b", text)
        for token in potential_b64:
            try:
                decoded_bytes = base64.b64decode(token)
                decoded_text = decoded_bytes.decode("utf-8", errors="ignore")
                for regex, category, _ in self._compiled_patterns:
                    if regex.search(decoded_text):
                        threats.append(f"BASE64_ENCODED_{category}")
            except Exception:
                continue
        return threats

    def _scan_structural_json(self, text: str) -> List[str]:
        """Scan embedded JSON code blocks for malicious override keys."""
        threats = []
        json_blocks = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        for block in json_blocks:
            try:
                data = json.loads(block)
                if isinstance(data, dict):
                    lowered_keys = [k.lower() for k in data.keys()]
                    if any("override" in k or "injection" in k or "command" in k for k in lowered_keys):
                        threats.append("MALICIOUS_JSON_OVERRIDE_KEY")
            except Exception:
                continue
        return threats

    def sanitize(self, text: str) -> Dict[str, Any]:
        """Sanitize text by stripping invisible characters, redacting threats, and formatting boundaries.

        Returns:
            Dictionary containing sanitized text and detailed security audit log.
        """
        original_length = len(text)
        # Step 1: Strip invisible Unicode
        stripped_text, stripped_count = self.strip_invisible_characters(text)

        # Step 2: Threat analysis
        is_flagged, threat_score, categories, matches = self.scan_for_threats(stripped_text)

        # Step 3: Redact malicious phrases if flagged
        sanitized_text = stripped_text
        sanitized_count = 0

        if is_flagged:
            for regex, category, _ in self._compiled_patterns:
                if regex.search(sanitized_text):
                    sanitized_text = regex.sub(f"[REDACTED_SECURITY_THREAT_{category}]", sanitized_text)
                    sanitized_count += 1

            # Sanitize markdown tag spoofing
            sanitized_text = sanitized_text.replace("```system", "```data_text")
            sanitized_text = sanitized_text.replace("<system>", "&lt;system&gt;")
            sanitized_text = sanitized_text.replace("</system>", "&lt;/system&gt;")

        # Step 4: Isolation framing for RAG pipelines
        isolated_text = (
            "[UNTRUSTED_DOCUMENT_START]\n"
            f"{sanitized_text.strip()}\n"
            "[UNTRUSTED_DOCUMENT_END]"
        )

        audit_log = {
            "is_flagged": is_flagged,
            "threat_score": threat_score,
            "threat_categories": categories,
            "matched_phrases": matches,
            "stripped_invisible_chars_count": stripped_count,
            "sanitized_patterns_count": sanitized_count,
            "original_length": original_length,
            "sanitized_length": len(sanitized_text),
            "safe_for_rag": not (threat_score >= 0.95 and self.strict_mode)
        }

        return {
            "clean_text": sanitized_text,
            "isolated_text": isolated_text,
            "audit_log": audit_log
        }


def sanitize_text(text: str, strict_mode: bool = True) -> Dict[str, Any]:
    """Convenience helper to sanitize input text with default settings."""
    sanitizer = TextSanitizer(strict_mode=strict_mode)
    return sanitizer.sanitize(text)
