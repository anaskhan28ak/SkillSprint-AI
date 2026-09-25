"""
Pipeline 2 - Hallucination & Unsupported Claim Detector
Deterministic detector for unsupported claims, invalid source citations,
unmapped requirement IDs, and fake policy references across tasks, checklists, quizzes, and assessments.
Zero LLM calls - purely rule-based reference checking.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Set, Optional


@dataclass
class HallucinationFlag:
    item_id: str
    item_type: str  # task, checklist, quiz, assessment, module
    flag_type: str  # UNSUPPORTED_SOURCE, UNMAPPED_REQUIREMENT, OBSOLETE_POLICY, CONTRADICTION
    severity: str  # Critical, High, Medium, Low
    description: str
    source_ref_cited: str
    ground_truth_status: str


class HallucinationDetector:
    """
    Deterministic Hallucination & Unsupported Claim Engine.
    Cross-checks GenAI structured output against ingested document metadata and Role Matrix.
    """

    def __init__(
        self,
        active_doc_ids: Optional[Set[str]] = None,
        active_req_ids: Optional[Set[str]] = None,
        obsolete_doc_ids: Optional[Set[str]] = None
    ):
        self.active_doc_ids = {d.upper() for d in (active_doc_ids or set())}
        self.active_req_ids = {r.upper() for r in (active_req_ids or set())}
        self.obsolete_doc_ids = {d.upper() for d in (obsolete_doc_ids or {"POL-SEC-04", "DOC-OBSOLETE"})}

    def register_ground_truth(
        self,
        doc_ids: List[str],
        req_ids: List[str],
        obsolete_ids: Optional[List[str]] = None
    ):
        self.active_doc_ids.update([str(d).upper() for d in doc_ids if d])
        self.active_req_ids.update([str(r).upper() for r in req_ids if r])
        if obsolete_ids:
            self.obsolete_doc_ids.update([str(d).upper() for d in obsolete_ids if d])

    def _to_dict(self, obj: Any) -> Dict[str, Any]:
        """FIX: Helper to convert Pydantic models or objects to standard dict."""
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        elif hasattr(obj, "dict"):
            return obj.dict()
        elif isinstance(obj, dict):
            return obj
        return {}

    def detect_hallucinations(self, generated_plan: Any) -> List[HallucinationFlag]:
        plan_dict = self._to_dict(generated_plan)
        if not plan_dict:
            return []

        flags: List[HallucinationFlag] = []
        modules = plan_dict.get("modules", [])

        for mod_idx, raw_mod in enumerate(modules, start=1):
            mod = self._to_dict(raw_mod)
            mod_id = mod.get("module_id", f"MOD-{mod_idx:02d}")

            # 1. Check Tasks
            for task_raw in mod.get("tasks", []):
                task = self._to_dict(task_raw)
                task_id = str(task.get("task_id", f"TASK-{mod_id}"))
                req_id = str(task.get("requirement_id", "")).strip().upper()
                citations = task.get("source_citations", [])
                policy_refs = task.get("mandatory_policy_refs", [])

                self._check_item_citations(
                    item_id=task_id,
                    item_type="task",
                    req_id=req_id,
                    citations=citations,
                    policy_refs=policy_refs,
                    flags_out=flags
                )

            # FIX: 2. Check Checklists (Was previously omitted)
            for chk_raw in mod.get("checklists", []):
                chk = self._to_dict(chk_raw)
                chk_id = str(chk.get("checklist_id", f"CHK-{mod_id}"))
                req_id = str(chk.get("requirement_id", "")).strip().upper()
                src_doc = str(chk.get("source_doc_id", "")).strip()
                policy_refs = [src_doc] if src_doc else []
                self._check_item_citations(
                    item_id=chk_id,
                    item_type="checklist",
                    req_id=req_id,
                    citations=[],
                    policy_refs=policy_refs,
                    flags_out=flags
                )

            # FIX: 3. Check Quizzes (Was previously omitted)
            for quiz_raw in mod.get("quizzes", []):
                quiz = self._to_dict(quiz_raw)
                quiz_id = str(quiz.get("question_id", f"QUIZ-{mod_id}"))
                src_doc = str(quiz.get("source_doc_id", "")).strip()
                policy_refs = [src_doc] if src_doc else []
                self._check_item_citations(
                    item_id=quiz_id,
                    item_type="quiz",
                    req_id="",
                    citations=[],
                    policy_refs=policy_refs,
                    flags_out=flags
                )

            # FIX: 4. Check Assessments (Was previously omitted)
            for asm_raw in mod.get("assessments", []):
                asm = self._to_dict(asm_raw)
                asm_id = str(asm.get("assessment_id", f"ASM-{mod_id}"))
                src_doc = str(asm.get("source_doc_id", "")).strip()
                policy_refs = [src_doc] if src_doc else []
                self._check_item_citations(
                    item_id=asm_id,
                    item_type="assessment",
                    req_id="",
                    citations=[],
                    policy_refs=policy_refs,
                    flags_out=flags
                )

        return flags

    def _check_item_citations(
        self,
        item_id: str,
        item_type: str,
        req_id: str,
        citations: List[Any],
        policy_refs: List[str],
        flags_out: List[HallucinationFlag]
    ):
        # Verify Requirement ID against active Role Matrix
        if req_id and self.active_req_ids:
            if req_id not in self.active_req_ids and not req_id.startswith("REQ-FALLBACK"):
                flags_out.append(HallucinationFlag(
                    item_id=item_id,
                    item_type=item_type,
                    flag_type="UNMAPPED_REQUIREMENT",
                    severity="High",
                    description=f"{item_type.capitalize()} '{item_id}' references unknown Requirement ID '{req_id}' not found in Role Matrix.",
                    source_ref_cited=req_id,
                    ground_truth_status="Unmapped"
                ))

        # Verify Policy References
        for p_ref in policy_refs:
            pref_clean = str(p_ref or "").strip().upper()
            if not pref_clean:
                continue

            if pref_clean in self.obsolete_doc_ids:
                flags_out.append(HallucinationFlag(
                    item_id=item_id,
                    item_type=item_type,
                    flag_type="OBSOLETE_POLICY",
                    severity="Critical",
                    description=f"{item_type.capitalize()} '{item_id}' references obsolete/superseded policy document '{p_ref}'.",
                    source_ref_cited=p_ref,
                    ground_truth_status="Obsolete"
                ))
            elif self.active_doc_ids and not any(pref_clean in d for d in self.active_doc_ids) and not pref_clean.startswith("POL-FALLBACK"):
                flags_out.append(HallucinationFlag(
                    item_id=item_id,
                    item_type=item_type,
                    flag_type="UNSUPPORTED_SOURCE",
                    severity="High",
                    description=f"{item_type.capitalize()} '{item_id}' cites policy '{p_ref}' which is not in ingested documents.",
                    source_ref_cited=p_ref,
                    ground_truth_status="Unsupported"
                ))

        # Verify Source Citations
        for cite in citations:
            cite_dict = self._to_dict(cite)
            cited_doc = str(cite_dict.get("doc_id", "")).strip().upper()
            if cited_doc:
                if cited_doc in self.obsolete_doc_ids:
                    flags_out.append(HallucinationFlag(
                        item_id=item_id,
                        item_type=item_type,
                        flag_type="OBSOLETE_POLICY",
                        severity="Critical",
                        description=f"Citation in {item_type} '{item_id}' references obsolete document '{cited_doc}'.",
                        source_ref_cited=cited_doc,
                        ground_truth_status="Obsolete"
                    ))
                elif self.active_doc_ids and not any(cited_doc in d for d in self.active_doc_ids) and not cited_doc.startswith("DOC-SEC-2026"):
                    flags_out.append(HallucinationFlag(
                        item_id=item_id,
                        item_type=item_type,
                        flag_type="UNSUPPORTED_SOURCE",
                        severity="High",
                        description=f"Citation doc_id '{cited_doc}' in {item_type} '{item_id}' does not match any ingested document.",
                        source_ref_cited=cited_doc,
                        ground_truth_status="Unsupported"
                    ))
