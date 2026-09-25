"""
Pipeline 2 - Main Pipeline 2 Orchestration Engine
Deterministic Document Ingestion, Parsing, Chunking, Policy Precedence, and Ground-Truth Validation Facade.

STRICT DETERMINISTIC EXECUTION - ZERO EXTERNAL AI API CALLS.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Union
from src.document_processing.pdf_parser import PDFParser, ParsedDocument
from src.document_processing.docx_parser import DOCXParser, ParsedDocxDocument
from src.document_processing.chunker import DocumentChunker, DocumentChunk
from src.python_validation.precedence import PrecedenceResolver
from src.python_validation.score_calculator import ScoreCalculator, ValidationScoreMetrics
from src.python_validation.hallucination import HallucinationDetector
from src.python_validation.validator import GroundTruthValidator, FullValidationReport

logger = logging.getLogger("Pipeline2Engine")


class Pipeline2Engine:
    """
    Pipeline 2 Main Facade & Orchestrator.
    Handles document extraction, chunking, policy precedence resolution,
    and ground-truth verification of GenAI onboarding plans against matrix rules.
    """

    def __init__(
        self,
        dataset_dir: Optional[str] = None,
        role_matrix_path: Optional[str] = None,
        conflict_cases_path: Optional[str] = None
    ):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        self.dataset_dir = dataset_dir or os.path.join(base_dir, "dataset")
        self.role_matrix_path = role_matrix_path or os.path.join(self.dataset_dir, "role_matrix.json")
        self.conflict_cases_path = conflict_cases_path or os.path.join(self.dataset_dir, "conflict_cases.json")
        self.raw_docs_dir = os.path.join(self.dataset_dir, "raw_documents")

        self.pdf_parser = PDFParser()
        self.docx_parser = DOCXParser()
        self.chunker = DocumentChunker(target_chunk_tokens=500, overlap_tokens=50)
        self.precedence_resolver = PrecedenceResolver()
        self.validator = GroundTruthValidator(self.role_matrix_path, self.conflict_cases_path)

        self.ingested_documents: List[Union[ParsedDocument, ParsedDocxDocument, Dict[str, Any]]] = []
        self.document_chunks: List[DocumentChunk] = []
        self.active_docs_map: Dict[str, Dict[str, Any]] = {}

    def ingest_documents(self, source_path: Optional[str] = None) -> List[Any]:
        """
        Parses all PDF, DOCX, and TXT documents in target directory or file.
        Attaches metadata (doc_id, version, effective_date, page/section refs).
        """
        path = source_path or self.raw_docs_dir
        if not path or not os.path.exists(path):
            logger.warning(f"Ingestion path does not exist: {path}")
            return []

        files_to_parse = []
        if os.path.isdir(path):
            for fname in os.listdir(path):
                if not fname.startswith("."):
                    files_to_parse.append(os.path.join(path, fname))
        else:
            files_to_parse.append(path)

        self.ingested_documents = []
        raw_doc_dicts = []

        for fpath in files_to_parse:
            ext = os.path.splitext(fpath)[1].lower()
            try:
                if ext == ".pdf":
                    doc = self.pdf_parser.parse(fpath)
                    self.ingested_documents.append(doc)
                    raw_doc_dicts.append(doc.metadata)
                elif ext in [".docx", ".doc"]:
                    doc = self.docx_parser.parse(fpath)
                    self.ingested_documents.append(doc)
                    raw_doc_dicts.append(doc.metadata)
                elif ext in [".txt", ".md"]:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                    file_name = os.path.basename(fpath)
                    meta = self.pdf_parser._extract_metadata(file_name, text)
                    doc_dict = {
                        "doc_id": meta["doc_id"],
                        "title": meta["title"],
                        "doc_type": meta["doc_type"],
                        "version": meta["version"],
                        "effective_date": meta["effective_date"],
                        "file_path": fpath,
                        "full_text": text
                    }
                    self.ingested_documents.append(doc_dict)
                    raw_doc_dicts.append(meta)
            except Exception as e:
                logger.error(f"Error parsing document '{fpath}': {e}")

        # Resolve version overrides & precedence across ingested docs
        self.active_docs_map = self.precedence_resolver.resolve_version_conflicts(raw_doc_dicts)
        return self.ingested_documents

    def create_chunks(self) -> List[DocumentChunk]:
        """
        Generates 500-token chunks with 50-token overlap for all ingested documents.
        """
        self.document_chunks = []
        for doc in self.ingested_documents:
            chunks = self.chunker.chunk_document(doc)
            self.document_chunks.extend(chunks)
        return self.document_chunks

    def validate_onboarding_plan(self, plan_data: Union[Dict[str, Any], str, Any]) -> FullValidationReport:
        """
        Validates a Pipeline 1 GenAI onboarding plan against the Role Requirement Matrix.
        Returns FullValidationReport containing Coverage Score, Traceability Score,
        Hallucinations, Contradictions, and Requirement-level comparisons.
        """
        if isinstance(plan_data, str):
            if os.path.exists(plan_data):
                with open(plan_data, "r", encoding="utf-8") as f:
                    plan_dict = json.load(f)
            else:
                try:
                    plan_dict = json.loads(plan_data)
                except Exception:
                    plan_dict = {}
        elif hasattr(plan_data, "model_dump"):
            plan_dict = plan_data.model_dump()
        elif hasattr(plan_data, "dict"):
            plan_dict = plan_data.dict()
        elif isinstance(plan_data, dict):
            plan_dict = plan_data
        else:
            plan_dict = {}

        active_docs_list = list(self.active_docs_map.values())
        return self.validator.validate_plan(plan_dict, active_docs_list)

    def generate_comparison_report(self, report: FullValidationReport) -> Dict[str, Any]:
        """
        Formats validation results into structured comparison report dict.
        """
        req_comparisons = []
        for c in report.requirement_comparisons:
            req_comparisons.append({
                "requirement_id": c.req_id,
                "role": c.role_name,
                "policy_name": c.policy_name,
                "source_doc_id": c.source_doc_id,
                "source_section": c.source_section,
                "is_mandatory": c.is_mandatory,
                "genai_covered": c.genai_covered,
                "status": c.status,
                "genai_task_id": c.genai_task_id,
                "notes": c.notes
            })

        hallucination_items = []
        for h in report.hallucinations:
            hallucination_items.append({
                "item_id": h.item_id,
                "item_type": h.item_type,
                "flag_type": h.flag_type,
                "severity": h.severity,
                "description": h.description,
                "source_ref_cited": h.source_ref_cited,
                "ground_truth_status": h.ground_truth_status
            })

        return {
            "plan_id": report.plan_id,
            "target_role": report.target_role,
            "role_id": report.role_id,
            "verification_status": report.metrics.final_status,
            "metrics": {
                "coverage_score": report.metrics.coverage_score,
                "traceability_score": report.metrics.traceability_score,
                "consistency_score": report.metrics.consistency_score,
                "total_mandatory_requirements": report.metrics.total_mandatory,
                "covered_mandatory_requirements": report.metrics.covered_mandatory,
                "missing_mandatory_requirements": report.metrics.missing_mandatory,
                "total_optional_requirements": report.metrics.total_optional,
                "covered_optional_requirements": report.metrics.covered_optional,
                "total_generated_items": report.metrics.total_generated_items,
                "source_grounded_items": report.metrics.source_grounded_items,
                "unsupported_items": report.metrics.unsupported_items,
                "contradiction_count": report.metrics.contradiction_count,
                "hallucination_count": report.metrics.hallucination_count
            },
            "requirement_comparisons": req_comparisons,
            "hallucinations": hallucination_items,
            "contradictions": report.contradictions,
            "sequence_warnings": report.sequence_warnings
        }
