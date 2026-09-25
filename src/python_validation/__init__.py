"""
Pipeline 2 - Ground-Truth Validation Package
Provides precedence resolution, score calculation, hallucination detection,
and ground-truth comparison engine.
"""

from src.python_validation.precedence import PrecedenceResolver, PrecedenceRule
from src.python_validation.score_calculator import ScoreCalculator, ValidationScoreMetrics
from src.python_validation.hallucination import HallucinationDetector, HallucinationFlag
from src.python_validation.validator import GroundTruthValidator, FullValidationReport, RequirementComparisonResult
from src.python_validation.pipeline2_engine import Pipeline2Engine

__all__ = [
    "PrecedenceResolver",
    "PrecedenceRule",
    "ScoreCalculator",
    "ValidationScoreMetrics",
    "HallucinationDetector",
    "HallucinationFlag",
    "GroundTruthValidator",
    "FullValidationReport",
    "RequirementComparisonResult",
    "Pipeline2Engine"
]
