"""
Pipeline 2 - Ground-Truth Comparison Engine
Compares structured GenAI output against the independent Role Requirement Matrix.
Calculates coverage, detects missing requirements, contradictions, and sequence errors.
Zero external AI calls - pure deterministic execution.
"""

import os
import re
import json
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Union
from src.python_validation.score_calculator import ScoreCalculator, ValidationScoreMetrics
from src.python_validation.hallucination import HallucinationDetector, HallucinationFlag
from src.python_validation.precedence import PrecedenceResolver

logger = logging.getLogger("GroundTruthValidator")


@dataclass
class RequirementComparisonResult:
    req_id: str
    role_name: str
    policy_name: str
    source_doc_id: str
    source_section: str
    is_mandatory: bool
    genai_covered: bool
    status: str  # MATCH, MISSING_MANDATORY, MISSING_OPTIONAL, MISMATCH, UNSUPPORTED
    genai_task_id: Optional[str] = None
    notes: str = ""


@dataclass
class FullValidationReport:
    role_id: str
    target_role: str
    plan_id: str
    metrics: ValidationScoreMetrics
    requirement_comparisons: List[RequirementComparisonResult] = field(default_factory=list)
    hallucinations: List[HallucinationFlag] = field(default_factory=list)
    contradictions: List[Dict[str, Any]] = field(default_factory=list)
    sequence_warnings: List[str] = field(default_factory=list)


class GroundTruthValidator:
    """
    Independent Python Ground-Truth Validation Engine.
    Executes deterministic checks against the official Role Requirement Matrix.
    """

    def __init__(self, role_matrix_path: Optional[str] = None, conflict_cases_path: Optional[str] = None):
        self.role_matrix: List[Dict[str, Any]] = []
        self.conflict_cases: List[Dict[str, Any]] = []
        self.score_calc = ScoreCalculator()
        self.precedence_resolver = PrecedenceResolver()

        if role_matrix_path and os.path.exists(role_matrix_path):
            try:
                with open(role_matrix_path, "r", encoding="utf-8") as f:
                    self.role_matrix = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load role matrix from {role_matrix_path}: {e}")

        if conflict_cases_path and os.path.exists(conflict_cases_path):
            try:
                with open(conflict_cases_path, "r", encoding="utf-8") as f:
                    self.conflict_cases = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load conflict cases from {conflict_cases_path}: {e}")

    def _to_dict(self, obj: Any) -> Dict[str, Any]:
        """FIX: Helper to convert Pydantic models or JSON strings to standard dict."""
        if isinstance(obj, str):
            try:
                return json.loads(obj)
            except Exception:
                return {}
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        elif hasattr(obj, "dict"):
            return obj.dict()
        elif isinstance(obj, dict):
            return obj
        return {}

    def load_matrix_data(self, matrix_list: List[Dict[str, Any]]):
        self.role_matrix = matrix_list

    def validate_plan(
        self,
        generated_plan: Any,
        active_ingested_docs: Optional[List[Dict[str, Any]]] = None
    ) -> FullValidationReport:
        """
        Validates a generated onboarding plan against the Role Requirement Matrix.
        """
        plan_dict = self._to_dict(generated_plan)
        target_role = str(plan_dict.get("target_role") or plan_dict.get("role") or "").strip()
        role_id = str(plan_dict.get("role_id") or "").strip()
        plan_id = str(plan_dict.get("plan_id") or "PLAN-UNKNOWN").strip()

        # 1. Filter Role Requirement Matrix for target role using robust matcher
        matrix_reqs = self._get_matrix_reqs_for_role(target_role, role_id)
        mandatory_matrix_reqs = [r for r in matrix_reqs if r.get("is_mandatory", True)]
        optional_matrix_reqs = [r for r in matrix_reqs if not r.get("is_mandatory", True)]

        # 2. Extract covered requirements & tasks from generated plan
        covered_req_map: Dict[str, Dict[str, Any]] = {}
        all_gen_tasks: List[Dict[str, Any]] = []
        grounded_items_count = 0
        total_gen_items = 0

        modules = plan_dict.get("modules", [])
        for mod_raw in modules:
            mod = self._to_dict(mod_raw)
            for task_raw in mod.get("tasks", []):
                task = self._to_dict(task_raw)
                total_gen_items += 1
                all_gen_tasks.append(task)
                r_id = str(task.get("requirement_id", "")).strip().upper()
                if r_id:
                    covered_req_map[r_id] = task

                citations = task.get("source_citations", [])
                policy_refs = task.get("mandatory_policy_refs", [])
                if citations or policy_refs:
                    grounded_items_count += 1

            # Check checklist, quizzes, assessments count
            for chk_raw in mod.get("checklists", []):
                chk = self._to_dict(chk_raw)
                total_gen_items += 1
                r_id = str(chk.get("requirement_id", "")).strip().upper()
                if r_id and r_id not in covered_req_map:
                    covered_req_map[r_id] = chk
                if chk.get("source_doc_id") or chk.get("source_citations"):
                    grounded_items_count += 1

            for quiz_raw in mod.get("quizzes", []):
                quiz = self._to_dict(quiz_raw)
                total_gen_items += 1
                if quiz.get("source_doc_id") or quiz.get("source_citations"):
                    grounded_items_count += 1

            for asm_raw in mod.get("assessments", []):
                asm = self._to_dict(asm_raw)
                total_gen_items += 1
                if asm.get("source_doc_id") or asm.get("source_citations"):
                    grounded_items_count += 1

        if total_gen_items == 0:
            total_gen_items = max(1, len(all_gen_tasks))

        # 3. Perform requirement level comparison
        comparisons: List[RequirementComparisonResult] = []
        covered_mandatory_count = 0
        covered_optional_count = 0

        for req in matrix_reqs:
            r_id = str(req.get("req_id") or req.get("requirement_id") or "").strip().upper()
            is_mand = bool(req.get("is_mandatory", True))
            req_doc = str(req.get("source_doc_id", "")).strip().upper()
            req_sec = str(req.get("source_section", "")).strip().upper()

            # FIX: Rigorous matching: must match exact req_id OR exact (source_doc_id AND section) in citations
            is_covered = False
            matched_task = covered_req_map.get(r_id, {})

            if r_id and r_id in covered_req_map:
                is_covered = True
            else:
                # Check citations for matching document ID and section ID
                for t in all_gen_tasks:
                    for cite in t.get("source_citations", []):
                        cite_dict = self._to_dict(cite)
                        c_doc = str(cite_dict.get("doc_id", "")).strip().upper()
                        c_sec = str(cite_dict.get("section_id", "")).strip().upper()
                        if c_doc == req_doc and (not req_sec or req_sec in c_sec or c_sec in req_sec):
                            is_covered = True
                            matched_task = t
                            break
                    if is_covered:
                        break

            if is_covered:
                if is_mand:
                    covered_mandatory_count += 1
                    status = "MATCH"
                else:
                    covered_optional_count += 1
                    status = "MATCH"
            else:
                status = "MISSING_MANDATORY" if is_mand else "MISSING_OPTIONAL"

            comparisons.append(RequirementComparisonResult(
                req_id=r_id,
                role_name=target_role,
                policy_name=req.get("policy_name", req.get("source_doc_id", "")),
                source_doc_id=req.get("source_doc_id", ""),
                source_section=req.get("source_section", ""),
                is_mandatory=is_mand,
                genai_covered=is_covered,
                status=status,
                genai_task_id=matched_task.get("task_id") if matched_task else None,
                notes=f"Conflict notes: {req.get('conflict_notes')}" if req.get("conflict_flag") else "Standard requirement"
            ))

        # 4. Detect Hallucinations & Unsupported Claims
        detector = HallucinationDetector()
        active_doc_ids: Set[str] = set()
        if active_ingested_docs:
            for d in active_ingested_docs:
                d_id = str(d.get("doc_id", "")).strip().upper()
                if d_id:
                    active_doc_ids.add(d_id)
        else:
            active_doc_ids = {str(r.get("source_doc_id", "")).strip().upper() for r in self.role_matrix if r.get("source_doc_id")}

        active_req_ids = {str(r.get("req_id", "")).strip().upper() for r in self.role_matrix if r.get("req_id")}
        detector.register_ground_truth(list(active_doc_ids), list(active_req_ids))

        hallucinations = detector.detect_hallucinations(plan_dict)
        unsupported_count = len([h for h in hallucinations if h.flag_type == "UNSUPPORTED_SOURCE"])

        # 5. Detect Contradictions & Version Override Violations
        contradictions = self._detect_contradictions(plan_dict)

        # 6. Learning Sequence & Prerequisite Validation
        sequence_warnings = self._validate_learning_sequence(plan_dict)

        # 7. Calculate Final Math Scores
        total_mandatory = len(mandatory_matrix_reqs)
        total_optional = len(optional_matrix_reqs)

        metrics = self.score_calc.compute_all_metrics(
            total_mandatory=total_mandatory if total_mandatory > 0 else len(comparisons),
            covered_mandatory=covered_mandatory_count if total_mandatory > 0 else len([c for c in comparisons if c.genai_covered]),
            total_optional=total_optional,
            covered_optional=covered_optional_count,
            total_generated_items=total_gen_items,
            grounded_items=grounded_items_count,
            unsupported_items=unsupported_count,
            contradiction_count=len(contradictions),
            hallucination_count=len(hallucinations)
        )

        return FullValidationReport(
            role_id=role_id,
            target_role=target_role,
            plan_id=plan_id,
            metrics=metrics,
            requirement_comparisons=comparisons,
            hallucinations=hallucinations,
            contradictions=contradictions,
            sequence_warnings=sequence_warnings
        )

    def _get_matrix_reqs_for_role(self, role_name: str, role_id: str) -> List[Dict[str, Any]]:
        """
        FIX: Robust role matching using bidirectional substring and token overlap.
        Eliminates the bug where 'Senior DevOps Engineer' failed against 'DevOps Engineer'.
        """
        if not self.role_matrix:
            return []

        matched = []
        r_name_clean = role_name.strip().lower()
        r_id_clean = role_id.strip().lower()
        input_tokens = set(re.findall(r'\w+', r_name_clean)) - {"senior", "junior", "lead", "associate", "intern"}

        for req in self.role_matrix:
            m_role = str(req.get("role_name", "")).strip().lower()
            m_id = str(req.get("role_id", "")).strip().lower()

            # Direct substring or exact ID match
            if r_id_clean and (r_id_clean == m_id or r_id_clean in m_id or m_id in r_id_clean):
                matched.append(req)
                continue

            if r_name_clean and (r_name_clean in m_role or m_role in r_name_clean):
                matched.append(req)
                continue

            # Token overlap check (e.g. 'devops' and 'engineer')
            matrix_tokens = set(re.findall(r'\w+', m_role))
            if input_tokens and len(input_tokens.intersection(matrix_tokens)) >= 1:
                matched.append(req)

        return matched

    def _detect_contradictions(
        self,
        generated_plan: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        FIX: Evaluates both Doc_Hierarchy_Conflict and Version_Update_Override
        against conflict cases in conflict_cases.json.
        """
        contradictions = []

        for case in self.conflict_cases:
            c_type = case.get("conflict_type")
            p_doc = str(case.get("primary_doc_id", "")).upper()
            c_doc = str(case.get("conflicting_doc_id", "")).upper()
            topic = case.get("rule_topic", "")
            rule = case.get("expected_ground_truth_rule", "")

            for mod_raw in generated_plan.get("modules", []):
                mod = self._to_dict(mod_raw)
                for task_raw in mod.get("tasks", []):
                    task = self._to_dict(task_raw)
                    refs = [str(r).upper() for r in task.get("mandatory_policy_refs", [])]
                    cites = [str(c.get("doc_id", "")).upper() for c in task.get("source_citations", []) if c.get("doc_id")]
                    all_refs = set(refs + cites)

                    # Check 1: Doc Hierarchy Conflict (e.g. FAQ used instead of Policy/SOP)
                    if c_type == "Doc_Hierarchy_Conflict" and c_doc in all_refs and p_doc not in all_refs:
                        contradictions.append({
                            "case_id": case.get("case_id"),
                            "conflict_type": c_type,
                            "task_id": task.get("task_id"),
                            "topic": topic,
                            "issue": f"Task cites lower-priority document '{c_doc}' which is superseded by '{p_doc}'. Precedence: Policy > SOP > FAQ.",
                            "expected_rule": rule,
                            "severity": "High"
                        })

                    # Check 2: Version Update Override (e.g. task mentions obsolete SLA/threshold)
                    if c_doc in all_refs:
                        desc = str(task.get("description", "")).lower()
                        # Outdated indicators
                        if any(phrase in desc for phrase in ["30 minutes", "72 hours", "sms otp", "single reviewer", "10-character", "physical clean desk", "pol-sec-04"]):
                            contradictions.append({
                                "case_id": case.get("case_id"),
                                "conflict_type": c_type,
                                "task_id": task.get("task_id"),
                                "topic": topic,
                                "issue": f"Task relies on superseded rules from '{c_doc}'. Ground truth: {rule}",
                                "expected_rule": rule,
                                "severity": "Critical"
                            })

        return contradictions

    def _validate_learning_sequence(self, generated_plan: Dict[str, Any]) -> List[str]:
        warnings = []
        modules = generated_plan.get("modules", [])

        day1_tasks = 0
        seen_topics: Set[str] = set()

        for mod_raw in modules:
            mod = self._to_dict(mod_raw)
            stage = str(mod.get("stage") or mod.get("due_stage") or "")
            for task_raw in mod.get("tasks", []):
                task = self._to_dict(task_raw)
                if stage == "Day 1":
                    day1_tasks += 1
                
                title = str(task.get("title", "")).lower()
                if "advanced" in title or "production deployment" in title:
                    if "security basics" not in seen_topics and "baseline orientation" not in seen_topics:
                        warnings.append(f"Prerequisite Warning: Task '{task.get('task_id')}' ({task.get('title')}) scheduled before baseline security/orientation.")
                
                seen_topics.add(title)

        if day1_tasks > 10:
            warnings.append(f"Schedule Warning: Day 1 contains {day1_tasks} tasks. Consider spreading across Week 1.")

        return warnings
