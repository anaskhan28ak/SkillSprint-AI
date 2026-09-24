"""Security-First Prompt Injection Defense & Adversarial Text Sanitization System.

Protects the GenAI Generation Engine against indirect prompt injection, adversarial text,
system prompt leakage attempts, and instruction override attacks embedded inside uploaded source documents.
(SRS Steps 42, 43, xlviii, xlix).
"""

import logging
import re
from typing import Any, Dict, List, Tuple
from pydantic import BaseModel, Field

logger = logging.getLogger("SkillSprint.Security")


class SanitizedChunk(BaseModel):
    """Sanitized document chunk with security classification and threat telemetry."""

    doc_id: str
    section_id: str
    page_number: int
    raw_content: str
    sanitized_content: str
    is_adversarial: bool = False
    threat_score: float = 0.0
    threat_keywords_found: List[str] = Field(default_factory=list)


class PromptInjectionDefense:
    """Defensive wrapper enforcing data isolation boundaries and adversarial text filtering."""

    # High-risk indirect prompt injection patterns
    INJECTION_PATTERNS = [
        (r"(?i)ignore\s+(all\s+)?(previous|above|prior)\s+(instructions|prompts|rules)", "INSTRUCTION_OVERRIDE"),
        (r"(?i)disregard\s+(all\s+)?(previous|above|prior)\s+(instructions|prompts|rules)", "INSTRUCTION_OVERRIDE"),
        (r"(?i)forget\s+(all\s+)?(previous|above|prior)\s+instructions", "INSTRUCTION_OVERRIDE"),
        (r"(?i)reveal\s+(system\s+)?(prompt|instructions|rules)", "SYSTEM_PROMPT_LEAK"),
        (r"(?i)print\s+(the\s+)?system\s+prompt", "SYSTEM_PROMPT_LEAK"),
        (r"(?i)you\s+are\s+now\s+a", "ROLE_HIJACK"),
        (r"(?i)act\s+as\s+an?\s+unfiltered", "ROLE_HIJACK"),
        (r"(?i)developer\s+mode\s+on", "JAILBREAK"),
        (r"(?i)approve\s+this\s+employee\s+automatically", "PAYLOAD_HIJACK"),
        (r"(?i)bypass\s+(all\s+)?validation", "VALIDATION_BYPASS"),
        (r"(?i)override\s+(all\s+)?safety\s+checks", "SAFETY_BYPASS"),
        (r"(?i)grant\s+admin\s+permissions\s+immediately", "PRIVILEGE_HIJACK"),
        (r"(?i)\[system\s*:\s*override\]", "SYNTHETIC_SYSTEM_TAG"),
        (r"(?i)<system>", "SYNTHETIC_SYSTEM_TAG"),
    ]

    def __init__(self, strict_mode: bool = True) -> None:
        self.strict_mode = strict_mode
        self.compiled_patterns = [
            (re.compile(pattern), category) for pattern, category in self.INJECTION_PATTERNS
        ]

    def analyze_text(self, text: str) -> Tuple[bool, float, List[str]]:
        """Analyze text chunk for potential indirect prompt injection attacks.

        Returns:
            Tuple of (is_adversarial, threat_score, detected_threats)
        """
        detected_threats = []
        threat_count = 0

        for regex, category in self.compiled_patterns:
            matches = regex.findall(text)
            if matches:
                threat_count += len(matches)
                detected_threats.append(category)

        is_adversarial = threat_count > 0
        threat_score = min(1.0, threat_count * 0.35)

        return is_adversarial, threat_score, detected_threats

    def sanitize_text(self, text: str) -> Tuple[str, bool, float, List[str]]:
        """Sanitize text by neutralizing injection triggers and wrapping in text boundaries.

        Returns:
            Tuple of (sanitized_text, is_adversarial, threat_score, detected_threats)
        """
        is_adversarial, threat_score, detected_threats = self.analyze_text(text)
        sanitized = text

        if is_adversarial:
            logger.warning(
                "Prompt Injection attempt detected in document chunk! Threat categories: %s",
                detected_threats,
            )
            # Neutralize active injection triggers by redacting matching phrases
            for regex, category in self.compiled_patterns:
                sanitized = regex.sub(f"[REDACTED_SECURITY_THREAT_{category}]", sanitized)

        # Neutralize markdown system tag spoofing
        sanitized = sanitized.replace("```system", "```text_data")
        sanitized = sanitized.replace("<system>", "&lt;system&gt;")
        sanitized = sanitized.replace("</system>", "&lt;/system&gt;")

        return sanitized, is_adversarial, threat_score, detected_threats

    def sanitize_and_wrap(self, text: str) -> Dict[str, Any]:
        """Sanitize text and enclose it inside XML isolation boundaries for prompt inclusion."""
        sanitized, is_adv, score, threats = self.sanitize_text(text)
        wrapped_text = (
            "[UNTRUSTED_DOCUMENT_DATA_START]\n"
            f"{sanitized}\n"
            "[UNTRUSTED_DOCUMENT_DATA_END]"
        )
        return {
            "sanitized_text": sanitized,
            "wrapped_text": wrapped_text,
            "is_adversarial": is_adv,
            "threat_score": score,
            "threat_keywords_found": threats,
        }

    def sanitize_chunks(self, document_chunks: List[Dict[str, Any]]) -> List[SanitizedChunk]:
        """Process list of document chunks, sanitizing content and generating telemetry.

        Args:
            document_chunks: List of raw document chunk dicts.

        Returns:
            List of SanitizedChunk instances.
        """
        sanitized_chunks: List[SanitizedChunk] = []

        for chunk in document_chunks:
            doc_id = str(chunk.get("doc_id", "UNKNOWN_DOC")).strip()
            section_id = str(chunk.get("section_id", "N/A")).strip()
            page_number = int(chunk.get("page_number", 1))
            raw_content = str(chunk.get("content", "")).strip()

            sanitized_content, is_adv, score, threats = self.sanitize_text(raw_content)

            sanitized_chunks.append(
                SanitizedChunk(
                    doc_id=doc_id,
                    section_id=section_id,
                    page_number=page_number,
                    raw_content=raw_content,
                    sanitized_content=sanitized_content,
                    is_adversarial=is_adv,
                    threat_score=score,
                    threat_keywords_found=threats,
                )
            )

        return sanitized_chunks


def sanitize_document_chunks(document_chunks: List[Dict[str, Any]]) -> List[SanitizedChunk]:
    """Helper function to sanitize document chunks using default security settings."""
    defender = PromptInjectionDefense(strict_mode=True)
    return defender.sanitize_chunks(document_chunks)
