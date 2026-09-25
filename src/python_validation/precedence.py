"""
Pipeline 2 - Policy Precedence & Hierarchy Resolver
Enforces strict document hierarchy (POLICY > SOP > FAQ > Informal)
and version control resolution (v2.0 supersedes v1.0).
Deactivates obsolete/superseded rules deterministically.
"""

import re
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional, Union

logger = logging.getLogger("PrecedenceResolver")


@dataclass
class PrecedenceRule:
    doc_id: str
    doc_type: str  # POLICY, SOP, FAQ, GUIDANCE
    version: str
    effective_date: str
    priority_rank: int  # 1 (POLICY), 2 (SOP), 3 (FAQ), 4 (INFORMAL)
    is_active: bool = True
    superseded_by: Optional[str] = None


class PrecedenceResolver:
    """
    Deterministic Precedence & Hierarchy Resolver.
    Enforces document type hierarchy and version overrides without external AI APIs.
    """

    HIERARCHY_RANK = {
        "POLICY": 1,
        "POL": 1,
        "SOP": 2,
        "PROCEDURE": 2,
        "FAQ": 3,
        "KB": 3,
        "GUIDANCE": 4,
        "INFORMAL": 4
    }

    def parse_version_tuple(self, version_str: str) -> Tuple[int, ...]:
        """
        FIX: Extract integer tuple for semver comparison (e.g., 'v2.10' -> (2, 10), 'v2.2' -> (2, 2)).
        Eliminates float comparison bug where float('2.10') == float('2.1') < float('2.2').
        """
        try:
            from packaging.version import parse as semver_parse  # type: ignore
            parsed = semver_parse(str(version_str).lstrip("vV"))
            # If standard version, use release tuple
            if hasattr(parsed, "release") and parsed.release:
                return parsed.release
        except Exception:
            pass

        # Fallback regex tuple parsing
        match = re.search(r'(\d+(?:\.\d+)*)', str(version_str))
        if match:
            try:
                return tuple(int(part) for part in match.group(1).split('.'))
            except ValueError:
                return (1, 0)
        return (1, 0)

    def get_doc_rank(self, doc_type: str, doc_id: str = "") -> int:
        """Get precedence rank (1 = Highest priority)."""
        dtype = str(doc_type or "").upper()
        if dtype in self.HIERARCHY_RANK:
            return self.HIERARCHY_RANK[dtype]
        
        doc_id_str = str(doc_id or "")
        prefix = doc_id_str.split("-")[0].upper() if "-" in doc_id_str else doc_id_str.upper()
        return self.HIERARCHY_RANK.get(prefix, 4)

    def _get_field(self, item: Any, field_name: str, default: Any = "") -> Any:
        """FIX: Helper to safely extract fields from both dicts and class/dataclass instances."""
        if isinstance(item, dict):
            return item.get(field_name, default)
        return getattr(item, field_name, default)

    def _set_field(self, item: Any, field_name: str, value: Any):
        """FIX: Helper to safely set fields on both dicts and class/dataclass instances."""
        if isinstance(item, dict):
            item[field_name] = value
        elif hasattr(item, field_name):
            setattr(item, field_name, value)

    def resolve_version_conflicts(self, doc_list: List[Any]) -> Dict[str, Any]:
        """
        Groups documents by doc_id (base), finds highest version, and marks older versions as superseded.
        Returns map of active document definitions.
        """
        if not doc_list:
            return {}

        grouped: Dict[str, List[Any]] = {}

        for d in doc_list:
            doc_id = str(self._get_field(d, "doc_id") or self._get_field(d, "source_doc_id") or "DOC-UNKNOWN")
            # FIX: Only strip explicit version tags like _v2.1 or -v1, preserving document serial numbers like -01
            base_id = re.sub(r'[-_]v\d+(?:\.\d+)*$', '', doc_id, flags=re.IGNORECASE)
            grouped.setdefault(base_id, []).append(d)

        resolved_active: Dict[str, Any] = {}

        for base_id, docs in grouped.items():
            # Sort by version tuple descending
            sorted_docs = sorted(
                docs,
                key=lambda x: self.parse_version_tuple(self._get_field(x, "version") or self._get_field(x, "doc_version") or "1.0"),
                reverse=True
            )

            active_doc = sorted_docs[0]
            self._set_field(active_doc, "is_active", True)
            self._set_field(active_doc, "status", "ACTIVE")
            resolved_active[base_id] = active_doc

            # Deactivate older versions
            for old_doc in sorted_docs[1:]:
                self._set_field(old_doc, "is_active", False)
                self._set_field(old_doc, "status", "SUPERSEDED")
                self._set_field(old_doc, "superseded_by", self._get_field(active_doc, "doc_id"))

        return resolved_active

    def resolve_hierarchy_conflict(
        self,
        doc_a: Any,
        doc_b: Any
    ) -> Tuple[Any, Any, str]:
        """
        Compares two conflicting documents/rules.
        Returns (winner_doc, loser_doc, resolution_reason).
        """
        doc_a_id = str(self._get_field(doc_a, "doc_id") or self._get_field(doc_a, "source_doc_id") or "")
        doc_b_id = str(self._get_field(doc_b, "doc_id") or self._get_field(doc_b, "source_doc_id") or "")

        type_a = self._get_field(doc_a, "doc_type") or doc_a_id[:3]
        type_b = self._get_field(doc_b, "doc_type") or doc_b_id[:3]

        rank_a = self.get_doc_rank(type_a, doc_a_id)
        rank_b = self.get_doc_rank(type_b, doc_b_id)

        if rank_a < rank_b:
            reason = f"Document type precedence: {type_a} (Rank {rank_a}) supersedes {type_b} (Rank {rank_b}). Hierarchy: Policy > SOP > FAQ."
            return doc_a, doc_b, reason
        elif rank_b < rank_a:
            reason = f"Document type precedence: {type_b} (Rank {rank_b}) supersedes {type_a} (Rank {rank_a}). Hierarchy: Policy > SOP > FAQ."
            return doc_b, doc_a, reason

        # Equal document type, resolve by semver tuple
        ver_tuple_a = self.parse_version_tuple(self._get_field(doc_a, "version") or self._get_field(doc_a, "doc_version") or "1.0")
        ver_tuple_b = self.parse_version_tuple(self._get_field(doc_b, "version") or self._get_field(doc_b, "doc_version") or "1.0")

        if ver_tuple_a >= ver_tuple_b:
            reason = f"Version control precedence: {ver_tuple_a} supersedes obsolete {ver_tuple_b}."
            return doc_a, doc_b, reason
        else:
            reason = f"Version control precedence: {ver_tuple_b} supersedes obsolete {ver_tuple_a}."
            return doc_b, doc_a, reason
