"""
Pipeline 2 - Ground-Truth Scoring Engine
Calculates mathematical Coverage Score, Traceability Score, Consistency Score,
and metrics summary per project specification (SRS Steps 29, 30, 47).
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class ValidationScoreMetrics:
    total_mandatory: int
    covered_mandatory: int
    missing_mandatory: int
    total_optional: int
    covered_optional: int
    missing_optional: int
    total_generated_items: int
    source_grounded_items: int
    unsupported_items: int
    contradiction_count: int
    hallucination_count: int
    coverage_score: float  # Percentage (0.0 - 100.0)
    traceability_score: float  # Percentage (0.0 - 100.0)
    consistency_score: float  # Percentage (0.0 - 100.0)
    final_status: str  # Verified | Verified with Warning | Incomplete | Unsupported | Contradictory | Manual Review Required


class ScoreCalculator:
    """
    Deterministic scoring engine.
    Calculates Coverage, Traceability, and Consistency scores using explicit mathematical formulas.
    """

    @staticmethod
    def calculate_coverage_score(covered_mandatory: int, total_mandatory: int) -> float:
        """
        Coverage Score Formula = (Covered Mandatory Requirements / Total Mandatory Requirements) * 100
        Target = 100.0%
        """
        if total_mandatory <= 0:
            # FIX: If 0 mandatory requirements are expected, coverage is 100% only if 0 are missing.
            return 100.0
        score = (max(0, covered_mandatory) / total_mandatory) * 100.0
        return round(min(100.0, max(0.0, score)), 2)

    @staticmethod
    def calculate_traceability_score(grounded_items: int, total_items: int) -> float:
        """
        Traceability Score Formula = (Source-Grounded Items / Total Generated Items) * 100
        Target = 100.0%
        """
        if total_items <= 0:
            return 100.0
        score = (max(0, grounded_items) / total_items) * 100.0
        return round(min(100.0, max(0.0, score)), 2)

    @staticmethod
    def calculate_consistency_score(matching_attributes: int, total_attributes: int) -> float:
        """
        Consistency Score Formula = (Matching Structured Attributes / Total Checked Attributes) * 100
        """
        if total_attributes <= 0:
            return 100.0
        score = (max(0, matching_attributes) / total_attributes) * 100.0
        return round(min(100.0, max(0.0, score)), 2)

    def compute_all_metrics(
        self,
        total_mandatory: int,
        covered_mandatory: int,
        total_optional: int,
        covered_optional: int,
        total_generated_items: int,
        grounded_items: int,
        unsupported_items: int,
        contradiction_count: int,
        hallucination_count: int,
        matching_attributes: int = 0,
        total_attributes: int = 0
    ) -> ValidationScoreMetrics:

        # Ensure non-negative integers
        total_mandatory = max(0, total_mandatory)
        covered_mandatory = max(0, min(covered_mandatory, total_mandatory))
        missing_mandatory = max(0, total_mandatory - covered_mandatory)

        total_optional = max(0, total_optional)
        covered_optional = max(0, min(covered_optional, total_optional))
        missing_optional = max(0, total_optional - covered_optional)

        total_generated_items = max(0, total_generated_items)
        grounded_items = max(0, min(grounded_items, total_generated_items))
        unsupported_items = max(0, unsupported_items)
        contradiction_count = max(0, contradiction_count)
        hallucination_count = max(0, hallucination_count)

        coverage_score = self.calculate_coverage_score(covered_mandatory, total_mandatory)
        traceability_score = self.calculate_traceability_score(grounded_items, total_generated_items)
        consistency_score = self.calculate_consistency_score(
            matching_attributes if total_attributes > 0 else grounded_items,
            total_attributes if total_attributes > 0 else max(1, total_generated_items)
        )

        # FIX: Align strictly with SRS Step 47 Final Verification Status rules:
        # Verified | Verified with Warning | Incomplete | Unsupported | Contradictory | Manual Review Required
        if contradiction_count > 0:
            final_status = "Contradictory"
        elif hallucination_count > 0 or unsupported_items > 0:
            if coverage_score < 70.0:
                final_status = "Manual Review Required"
            else:
                final_status = "Unsupported"
        elif coverage_score < 100.0:
            if coverage_score < 50.0:
                final_status = "Manual Review Required"
            else:
                final_status = "Incomplete"
        elif traceability_score < 100.0:
            final_status = "Verified with Warning"
        else:
            final_status = "Verified"

        return ValidationScoreMetrics(
            total_mandatory=total_mandatory,
            covered_mandatory=covered_mandatory,
            missing_mandatory=missing_mandatory,
            total_optional=total_optional,
            covered_optional=covered_optional,
            missing_optional=missing_optional,
            total_generated_items=total_generated_items,
            source_grounded_items=grounded_items,
            unsupported_items=unsupported_items,
            contradiction_count=contradiction_count,
            hallucination_count=hallucination_count,
            coverage_score=coverage_score,
            traceability_score=traceability_score,
            consistency_score=consistency_score,
            final_status=final_status
        )
