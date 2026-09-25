"""
Unit tests for Pipeline 2 Document Parsing & Chunking Engine
Exhaustive test suite covering happy paths, edge cases, and corrupt inputs.
"""

import unittest
import os
import tempfile
from src.document_processing.pdf_parser import PDFParser
from src.document_processing.docx_parser import DOCXParser
from src.document_processing.chunker import DocumentChunker


class TestPipeline2Parsing(unittest.TestCase):

    def setUp(self):
        self.pdf_parser = PDFParser()
        self.docx_parser = DOCXParser()
        self.chunker = DocumentChunker(target_chunk_tokens=500, overlap_tokens=50)

    def test_pdf_parsing_standard_and_metadata(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".pdf.txt", delete=False) as f:
            f.write("POL-SEC-01: Information Security Policy v2.1\nEffective Date: 2026-01-01\n\nSection 1: IAM\nAll users must configure hardware MFA.")
            temp_path = f.name

        try:
            parsed = self.pdf_parser.parse(temp_path, doc_id_override="POL-SEC-01")
            self.assertEqual(parsed.doc_id, "POL-SEC-01")
            self.assertEqual(parsed.version, "v2.1")
            self.assertEqual(parsed.doc_type, "POLICY")
            self.assertTrue(len(parsed.pages) > 0)
            self.assertIn("hardware MFA", parsed.full_text)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_docx_parsing_standard_and_metadata(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".docx.txt", delete=False) as f:
            f.write("SOP-SUP-01: Escalation Procedures v2.0\nEffective Date: 2026-02-01\n\nHeading 1: Overview\nSeverity 1 tickets escalate in 15 mins.")
            temp_path = f.name

        try:
            parsed = self.docx_parser.parse(temp_path, doc_id_override="SOP-SUP-01")
            self.assertEqual(parsed.doc_id, "SOP-SUP-01")
            self.assertEqual(parsed.version, "v2.0")
            self.assertEqual(parsed.doc_type, "SOP")
            self.assertTrue(len(parsed.sections) > 0)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_metadata_preserving_chunking_standard(self):
        dummy_text = "Word " * 1200  # 1200 words
        doc_dict = {
            "doc_id": "POL-HR-01",
            "doc_type": "POLICY",
            "version": "v1.0",
            "effective_date": "2026-01-01",
            "text": dummy_text,
            "location_ref": "Page 1",
            "heading": "Leave Policy"
        }

        chunks = self.chunker.chunk_document(doc_dict)
        self.assertTrue(len(chunks) > 1)
        for chunk in chunks:
            self.assertEqual(chunk.doc_id, "POL-HR-01")
            self.assertEqual(chunk.version, "v1.0")
            self.assertEqual(chunk.doc_type, "POLICY")
            self.assertIn("CHUNK-POL-HR-01-", chunk.chunk_id)
            self.assertTrue(chunk.token_count <= 500)

    # Edge & Boundary Test Cases
    def test_empty_and_null_chunking(self):
        # Null document
        self.assertEqual(self.chunker.chunk_document(None), [])
        # Empty text
        self.assertEqual(self.chunker.chunk_document({"text": ""}), [])
        # Non-string text
        self.assertEqual(self.chunker.chunk_document({"text": None}), [])

    def test_single_word_chunking(self):
        doc = {"doc_id": "POL-MIN", "text": "SingleWord", "version": "v1.0"}
        chunks = self.chunker.chunk_document(doc)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].token_count, 1)

    def test_nonexistent_file_handling(self):
        with self.assertRaises(FileNotFoundError):
            self.pdf_parser.parse("non_existent_file_path_12345.pdf")

        with self.assertRaises(FileNotFoundError):
            self.docx_parser.parse("non_existent_file_path_12345.docx")


if __name__ == "__main__":
    unittest.main()
