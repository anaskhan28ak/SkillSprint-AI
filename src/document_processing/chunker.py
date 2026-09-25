"""
Pipeline 2 - Metadata-Preserving Chunking Engine
Deterministic 500-token chunker with 50-token overlap.
Attaches full source traceability metadata to every chunk.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Union
from src.document_processing.pdf_parser import ParsedDocument
from src.document_processing.docx_parser import ParsedDocxDocument


@dataclass
class DocumentChunk:
    chunk_id: str
    doc_id: str
    doc_type: str
    version: str
    effective_date: str
    heading: str
    location_ref: str
    text: str
    token_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)


class DocumentChunker:
    """
    Metadata-Preserving Chunking Engine.
    Chunks parsed documents into deterministic 500-token chunks with 50-token overlap.
    """

    def __init__(self, target_chunk_tokens: int = 500, overlap_tokens: int = 50):
        # FIX: Ensure valid chunk and overlap parameters to prevent 0 or negative steps
        self.target_chunk_tokens = max(10, int(target_chunk_tokens))
        self.overlap_tokens = max(0, min(int(overlap_tokens), self.target_chunk_tokens - 1))

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count based on whitespace word count."""
        if not text or not isinstance(text, str):
            return 0
        return len(text.split())

    def chunk_document(self, doc: Union[ParsedDocument, ParsedDocxDocument, Dict[str, Any]]) -> List[DocumentChunk]:
        # FIX: Guard against null document input
        if doc is None:
            return []

        chunks: List[DocumentChunk] = []

        if isinstance(doc, ParsedDocument):
            doc_id = doc.doc_id
            doc_type = doc.doc_type
            version = doc.version
            effective_date = doc.effective_date
            
            chunk_seq = 1
            for page in doc.pages:
                page_chunks = self._chunk_text(
                    text=page.text,
                    doc_id=doc_id,
                    doc_type=doc_type,
                    version=version,
                    effective_date=effective_date,
                    heading=page.headings[0] if page.headings else "General",
                    location_ref=page.location_ref,
                    start_seq=chunk_seq
                )
                chunks.extend(page_chunks)
                chunk_seq += len(page_chunks)

        elif isinstance(doc, ParsedDocxDocument):
            doc_id = doc.doc_id
            doc_type = doc.doc_type
            version = doc.version
            effective_date = doc.effective_date

            chunk_seq = 1
            for sec in doc.sections:
                sec_chunks = self._chunk_text(
                    text=sec.content,
                    doc_id=doc_id,
                    doc_type=doc_type,
                    version=version,
                    effective_date=effective_date,
                    heading=sec.heading,
                    location_ref=sec.location_ref,
                    start_seq=chunk_seq
                )
                chunks.extend(sec_chunks)
                chunk_seq += len(sec_chunks)

        elif isinstance(doc, dict):
            doc_id = str(doc.get("doc_id", "DOC-UNKNOWN"))
            doc_type = str(doc.get("doc_type", "POLICY"))
            version = str(doc.get("version", "v1.0"))
            effective_date = str(doc.get("effective_date", "2026-01-01"))
            content = doc.get("text") or doc.get("full_text") or ""
            location_ref = str(doc.get("location_ref", "Page 1"))
            heading = str(doc.get("heading", "General"))

            chunks = self._chunk_text(
                text=str(content),
                doc_id=doc_id,
                doc_type=doc_type,
                version=version,
                effective_date=effective_date,
                heading=heading,
                location_ref=location_ref,
                start_seq=1
            )

        return chunks

    def _chunk_text(
        self,
        text: str,
        doc_id: str,
        doc_type: str,
        version: str,
        effective_date: str,
        heading: str,
        location_ref: str,
        start_seq: int
    ) -> List[DocumentChunk]:
        # FIX: Guard against null, non-string, or whitespace-only text
        if not text or not isinstance(text, str):
            return []

        words = text.split()
        if not words:
            return []

        chunks: List[DocumentChunk] = []
        # FIX: Guarantee positive progress step to eliminate infinite loops
        step = max(1, self.target_chunk_tokens - self.overlap_tokens)

        seq = start_seq
        for i in range(0, len(words), step):
            chunk_words = words[i:i + self.target_chunk_tokens]
            chunk_text = " ".join(chunk_words)
            chunk_id = f"CHUNK-{doc_id}-{seq:04d}"

            chunks.append(DocumentChunk(
                chunk_id=chunk_id,
                doc_id=doc_id,
                doc_type=doc_type,
                version=version,
                effective_date=effective_date,
                heading=heading,
                location_ref=location_ref,
                text=chunk_text,
                token_count=len(chunk_words),
                metadata={
                    "doc_id": doc_id,
                    "version": version,
                    "doc_type": doc_type,
                    "effective_date": effective_date,
                    "heading": heading,
                    "location_ref": location_ref,
                    "word_offset_start": i,
                    "word_offset_end": i + len(chunk_words)
                }
            ))
            seq += 1

            if i + self.target_chunk_tokens >= len(words):
                break

        return chunks
