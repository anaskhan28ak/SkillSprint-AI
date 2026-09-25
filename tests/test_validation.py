"""
Unit tests for Pipeline 2 Ground-Truth Validation & Scoring Engine
Exhaustive test suite covering Happy Path, Boundary Cases, Negative Scenarios,
and Contradiction/Override Cases.
"""

import unittest
import os
import json
from src.python_validation.precedence import PrecedenceResolver
from src.python_validation.score_calculator import ScoreCalculator
from src.python_validation.hallucination import HallucinationDetector
from src.python_validation.validator import GroundTruthValidator
from src.python_validation.pipeline2_engine import Pipeline2Engine


class TestPipeline2Validation(unittest.TestCase):

    def setUp(self):
        self.precedence = PrecedenceResolver()
        self.score_calc = ScoreCalculator()
        self.detector = HallucinationDetector()
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        role_matrix_path = os.path.join(base_dir, "dataset", "role_matrix.json")
        conflict_cases_path = os.path.join(base_dir, "dataset", "conflict_cases.json")
        
        self.validator = GroundTruthValidator(role_matrix_path, conflict_cases_path)
        self.engine = Pipeline2Engine(dataset_dir=os.path.join(base_dir, "dataset"))

    # 1. Happy Path & Standard Scenarios
    def test_precedence_hierarchy_and_version(self):
        # Policy vs FAQ hierarchy
        policy_doc = {"doc_id": "POL-HR-03", "doc_type": "POLICY", "version": "v1.2"}
        faq_doc = {"doc_id": "FAQ-HR-01", "doc_type": "FAQ", "version": "v1.0"}

        winner, loser, reason = self.precedence.resolve_hierarchy_conflict(policy_doc, faq_doc)
        self.assertEqual(winner["doc_id"], "POL-HR-03")
        self.assertIn("Hierarchy: Policy > SOP > FAQ", reason)

        # Version v2.1 vs v1.0
        docs = [
            {"doc_id": "POL-SEC-01", "version": "1.0"},
            {"doc_id": "POL-SEC-01", "version": "2.1"}
        ]
        active_map = self.precedence.resolve_version_conflicts(docs)
        self.assertEqual(active_map["POL-SEC-01"]["version"], "2.1")
        self.assertEqual(active_map["POL-SEC-01"]["status"], "ACTIVE")

    def test_semver_tuple_precedence(self):
        # Ensure v2.10 is strictly greater than v2.2
        tuple_2_10 = self.precedence.parse_version_tuple("v2.10")
        tuple_2_2 = self.precedence.parse_version_tuple("v2.2")
        self.assertGreater(tuple_2_10, tuple_2_2)

    def test_score_calculator_perfect_and_partial(self):
        # 10 out of 10 mandatory requirements = 100%
        coverage = self.score_calc.calculate_coverage_score(10, 10)
        self.assertEqual(coverage, 100.0)

        # 8 out of 10 mandatory requirements = 80%
        coverage_partial = self.score_calc.calculate_coverage_score(8, 10)
        self.assertEqual(coverage_partial, 80.0)

        # Traceability = 5 out of 5 grounded = 100%
        traceability = self.score_calc.calculate_traceability_score(5, 5)
        self.assertEqual(traceability, 100.0)

        metrics = self.score_calc.compute_all_metrics(
            total_mandatory=10,
            covered_mandatory=10,
            total_optional=2,
            covered_optional=2,
            total_generated_items=5,
            grounded_items=5,
            unsupported_items=0,
            contradiction_count=0,
            hallucination_count=0
        )
        self.assertEqual(metrics.coverage_score, 100.0)
        self.assertEqual(metrics.traceability_score, 100.0)
        self.assertEqual(metrics.final_status, "Verified")

    # 2. Edge & Boundary Scenarios
    def test_score_calculator_zero_and_negative_bounds(self):
        # 0 total requirements
        self.assertEqual(self.score_calc.calculate_coverage_score(0, 0), 100.0)
        self.assertEqual(self.score_calc.calculate_traceability_score(0, 0), 100.0)

        # Negative covered counts are clamped to 0
        self.assertEqual(self.score_calc.calculate_coverage_score(-5, 10), 0.0)

        # Overflow covered count clamped to 100.0%
        self.assertEqual(self.score_calc.calculate_coverage_score(15, 10), 100.0)

    # 3. Negative & Failure Scenarios
    def test_hallucination_detection_comprehensive(self):
        self.detector.register_ground_truth(
            doc_ids=["POL-SEC-01", "POL-HR-01"],
            req_ids=["REQ-001", "REQ-002"],
            obsolete_ids=["POL-SEC-04"]
        )

        fake_plan = {
            "modules": [
                {
                    "module_id": "MOD-01",
                    "tasks": [
                        {
                            "task_id": "TASK-FAKE-1",
                            "requirement_id": "REQ-INVALID-999",
                            "mandatory_policy_refs": ["POL-SEC-04"],
                            "source_citations": [{"doc_id": "NON_EXISTENT_DOC"}]
                        }
                    ],
                    "checklists": [
                        {
                            "checklist_id": "CHK-FAKE-1",
                            "source_doc_id": "UNAPPROVED_DOC"
                        }
                    ],
                    "quizzes": [
                        {
                            "question_id": "QUIZ-FAKE-1",
                            "source_doc_id": "POL-SEC-04"
                        }
                    ]
                }
            ]
        }

        flags = self.detector.detect_hallucinations(fake_plan)
        self.assertTrue(len(flags) >= 3)
        flag_types = [f.flag_type for f in flags]
        self.assertIn("UNMAPPED_REQUIREMENT", flag_types)
        self.assertIn("OBSOLETE_POLICY", flag_types)
        self.assertIn("UNSUPPORTED_SOURCE", flag_types)

    # 4. Contradiction & Override Scenarios
    def test_contradiction_detection_hierarchy_and_version(self):
        contradictory_plan = {
            "role": "Customer Support Executive",
            "modules": [
                {
                    "module_id": "MOD-01",
                    "tasks": [
                        {
                            "task_id": "TASK-OUTDATED",
                            "title": "Escalation standard",
                            "description": "Tickets must be escalated within 30 minutes legacy SLA.",
                            "mandatory_policy_refs": ["SOP-SUP-01"]
                        }
                    ]
                }
            ]
        }

        report = self.validator.validate_plan(contradictory_plan)
        self.assertTrue(len(report.contradictions) > 0)
        self.assertEqual(report.metrics.final_status, "Contradictory")

    # 5. Facade End-to-End Execution
    def test_pipeline2_engine_facade(self):
        docs = self.engine.ingest_documents()
        self.assertTrue(len(docs) > 0)

        chunks = self.engine.create_chunks()
        self.assertTrue(len(chunks) > 0)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        demo_plan_path = os.path.join(base_dir, "demo_output_plan.json")
        
        if os.path.exists(demo_plan_path):
            report = self.engine.validate_onboarding_plan(demo_plan_path)
            self.assertIsNotNone(report.metrics)
            formatted = self.engine.generate_comparison_report(report)
            self.assertIn("verification_status", formatted)
            self.assertIn("metrics", formatted)
            self.assertIn("requirement_comparisons", formatted)


if __name__ == "__main__":
    unittest.main()
