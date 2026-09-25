"""
Pipeline 2 - Document Extraction & Parsing Module (PDF)
Deterministic text and metadata parser for PDF documents.
Supports page-level tracking, section heading identification, and metadata tagging.
Tiered extraction: pdfplumber -> pypdf -> safe text fallback.
"""

import os
import re
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

logger = logging.getLogger("PDFParser")


@dataclass
class ParsedPage:
    page_number: int
    text: str
    headings: List[str] = field(default_factory=list)
    location_ref: str = ""


@dataclass
class ParsedDocument:
    doc_id: str
    title: str
    doc_type: str  # POLICY, SOP, FAQ, HANDBOOK, etc.
    version: str
    effective_date: str
    file_path: str
    pages: List[ParsedPage] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    full_text: str = ""


class PDFParser:
    """
    Deterministic PDF Parser using pdfplumber with pypdf and regex text fallbacks.
    Extracts structured pages, headers, document ID, version, and metadata.
    """

    DOC_ID_PATTERN = re.compile(r'\b(POL|SOP|FAQ|MAN|MANUAL|GUIDE|HANDBOOK)-[A-Z0-9]+(?:-[0-9]+)?\b', re.IGNORECASE)
    # FIX: Enhanced version regex to capture versions preceded by underscores, spaces, or hyphens (e.g., _v2.0.txt)
    VERSION_PATTERN = re.compile(r'(?:[_\s-]|^)v?(\d+(?:\.\d+)*)', re.IGNORECASE)
    HEADING_PATTERN = re.compile(r'^(?:[0-9]+\.[0-9.]*|[A-Z][A-Za-z0-9\s]{3,50}:?)$', re.MULTILINE)

    def parse(self, file_path: str, doc_id_override: Optional[str] = None) -> ParsedDocument:
        # FIX: Guard against null or missing file path
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found or invalid: {file_path}")

        file_name = os.path.basename(file_path)
        pages: List[ParsedPage] = []
        raw_text_pages: List[str] = []

        # Tier 1: Attempt extraction via pdfplumber
        extracted = False
        try:
            import pdfplumber  # type: ignore
            with pdfplumber.open(file_path) as pdf:
                if len(pdf.pages) > 0:
                    for idx, page in enumerate(pdf.pages, start=1):
                        p_text = (page.extract_text() or "").strip()
                        raw_text_pages.append(p_text)
                        headings = self._extract_headings(p_text)
                        pages.append(ParsedPage(
                            page_number=idx,
                            text=p_text,
                            headings=headings,
                            location_ref=f"Page {idx}"
                        ))
                    extracted = True
        except Exception as e:
            logger.debug(f"pdfplumber extraction failed on {file_path}, falling back to pypdf: {e}")

        # Tier 2: Attempt extraction via pypdf
        if not extracted:
            try:
                import logging as _logging
                _logging.getLogger("pypdf").setLevel(_logging.ERROR)
                from pypdf import PdfReader  # type: ignore
                reader = PdfReader(file_path)
                if len(reader.pages) > 0:
                    for idx, page in enumerate(reader.pages, start=1):
                        p_text = (page.extract_text() or "").strip()
                        raw_text_pages.append(p_text)
                        headings = self._extract_headings(p_text)
                        pages.append(ParsedPage(
                            page_number=idx,
                            text=p_text,
                            headings=headings,
                            location_ref=f"Page {idx}"
                        ))
                    extracted = True
            except Exception as e:
                logger.debug(f"pypdf extraction failed on {file_path}, falling back to text read: {e}")

        # Tier 3: Safe plain-text fallback (for mock/text-based PDFs)
        if not extracted:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().strip()
                raw_text_pages = [content]
                headings = self._extract_headings(content)
                pages.append(ParsedPage(
                    page_number=1,
                    text=content,
                    headings=headings,
                    location_ref="Page 1"
                ))
            except Exception as e:
                logger.error(f"Text fallback failed for {file_path}: {e}")
                raw_text_pages = [""]
                pages.append(ParsedPage(page_number=1, text="", headings=[], location_ref="Page 1"))

        full_text = "\n\n".join(raw_text_pages)
        metadata = self._extract_metadata(file_name, full_text, doc_id_override)

        return ParsedDocument(
            doc_id=metadata["doc_id"],
            title=metadata["title"],
            doc_type=metadata["doc_type"],
            version=metadata["version"],
            effective_date=metadata["effective_date"],
            file_path=file_path,
            pages=pages,
            metadata=metadata,
            full_text=full_text
        )

    def _extract_headings(self, text: str) -> List[str]:
        # FIX: Guard against None or non-string input
        if not text or not isinstance(text, str):
            return []
        headings = []
        for line in text.splitlines():
            line_str = line.strip()
            if self.HEADING_PATTERN.match(line_str) and len(line_str) <= 80:
                headings.append(line_str)
        return headings

    def _extract_metadata(self, file_name: str, content: str, doc_id_override: Optional[str] = None) -> Dict[str, Any]:
        # Extract Doc ID
        doc_id = doc_id_override or ""
        if not doc_id:
            match = self.DOC_ID_PATTERN.search(file_name) or self.DOC_ID_PATTERN.search(content[:1000])
            if match:
                doc_id = match.group(0).upper()
            else:
                doc_id = os.path.splitext(file_name)[0].upper()

        # Determine Doc Type
        doc_type = "POLICY"
        if doc_id.startswith("SOP"):
            doc_type = "SOP"
        elif doc_id.startswith("FAQ"):
            doc_type = "FAQ"
        elif "GUIDELINE" in doc_id or "MANUAL" in doc_id:
            doc_type = "SOP"

        # FIX: Robust version parsing supporting underscore boundaries, explicit 'vX.Y', and 'Version: X.Y'
        version = "v1.0"
        v_match = (
            re.search(r'(?:[_\s-]|^)v?(\d+(?:\.\d+)+)', file_name, re.IGNORECASE) or
            re.search(r'Version\s*:?\s*v?(\d+(?:\.\d+)*)', content[:1000], re.IGNORECASE) or
            re.search(r'(?:[_\s-]|^)v(\d+(?:\.\d+)*)', content[:1000], re.IGNORECASE)
        )
        if v_match:
            v_val = v_match.group(1)
            if v_val:
                version = f"v{v_val}" if not v_val.startswith("v") else v_val

        # Extract Effective Date
        effective_date = "2026-01-01"
        date_match = re.search(
            r'(?:Effective Date|Date)\s*:?\s*([0-9]{4}-[0-9]{2}-[0-9]{2}|[A-Za-z]+\s+[0-9]{1,2},\s+[0-9]{4})',
            content[:1000],
            re.IGNORECASE
        )
        if date_match:
            effective_date = date_match.group(1)

        # Title extraction with clean sanitization
        title = file_name
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        if lines:
            first_line = lines[0]
            if 5 < len(first_line) < 120 and not first_line.startswith("%PDF"):
                title = first_line

        return {
            "doc_id": doc_id,
            "title": title,
            "doc_type": doc_type,
            "version": version,
            "effective_date": effective_date,
            "file_name": file_name
        }
