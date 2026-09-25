"""Security module for SkillSprint AI (Farhad Khan's Domain)."""

from .sanitizer import TextSanitizer, sanitize_text

try:
    from .prompt_injection_defense import PromptInjectionDefense, SanitizedChunk, sanitize_document_chunks
    __all__ = [
        "TextSanitizer",
        "sanitize_text",
        "PromptInjectionDefense",
        "SanitizedChunk",
        "sanitize_document_chunks",
    ]
except ImportError:
    __all__ = [
        "TextSanitizer",
        "sanitize_text",
    ]
