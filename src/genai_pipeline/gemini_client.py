"""Gemini generation engine wrapper for the SkillSprint AI pipeline.

Provides enterprise-grade reliability, exponential backoff with random jitter retry mechanisms,
Pydantic v2 structured output enforcement, latency calculation, audit telemetry,
selective module regeneration, and generation consistency evaluation.
(SRS Steps 39, 41, 44, 45, 57-59, 63-65).
"""

from datetime import datetime, timezone
import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args: Any, **kwargs: Any) -> bool:
        return False

from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel, ValidationError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from src.genai_pipeline.prompt_templates import (
    PROMPT_VERSION,
    build_onboarding_plan_prompt,
    build_selective_module_regeneration_prompt,
)
from src.genai_pipeline.schemas import (
    ChecklistItem,
    DifficultyLevel,
    GenerationMetadata,
    LearningTask,
    OnboardingModule,
    OnboardingPlanResponse,
    OnboardingStage,
    QuizQuestion,
    SourceCitation,
)

# Initialize structured logger
logger = logging.getLogger("SkillSprint.GenAIPipeline")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def _clean_schema_for_gemini(schema: Any) -> Any:
    """Recursively strip unsupported metadata keys from JSON schema dict for Gemini Developer API compatibility."""
    UNSUPPORTED_KEYS = {"additionalProperties", "examples", "title", "$defs", "$ref"}
    if isinstance(schema, dict):
        cleaned = {}
        for key, value in schema.items():
            if key in UNSUPPORTED_KEYS:
                continue
            cleaned[key] = _clean_schema_for_gemini(value)
        return cleaned
    elif isinstance(schema, list):
        return [_clean_schema_for_gemini(item) for item in schema]
    return schema


class GeminiPipelineEngine:
    """Production-grade GenAI generation engine using official google-genai SDK and Pydantic v2."""

    FALLBACK_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
    ) -> None:
        """Initialize the GeminiPipelineEngine.

        Args:
            api_key: Optional API key. If omitted, resolves GEMINI_API_KEY from environment.
            model_name: Default Gemini model name (defaults to 'gemini-2.5-flash').

        Raises:
            ValueError: If no valid API key is found.
        """
        load_dotenv()
        resolved_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )
        if not resolved_key or not resolved_key.strip():
            logger.error(
                "Gemini API key is missing. Set GEMINI_API_KEY in your .env file or pass api_key."
            )
            raise ValueError(
                "Missing Gemini API Key. Please configure GEMINI_API_KEY in your .env file "
                "or pass it directly as `api_key` to GeminiPipelineEngine."
            )

        self.model_name = model_name
        self.client = genai.Client(api_key=resolved_key.strip())
        logger.info(
            "Initialized GeminiPipelineEngine with model: %s (Prompt Version: %s)",
            self.model_name,
            PROMPT_VERSION,
        )

    @retry(
        retry=retry_if_exception_type(
            (APIError, ConnectionError, TimeoutError, json.JSONDecodeError, ValidationError, ValueError)
        ),
        wait=wait_random_exponential(min=2, max=16),
        stop=stop_after_attempt(3),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def _execute_api_and_validate(
        self,
        prompt: str,
        response_schema: Any = OnboardingPlanResponse,
    ) -> Tuple[Any, float, Optional[Any]]:
        """Call Gemini API with Structured Outputs, exponential backoff + jitter, and schema validation.

        Args:
            prompt: Formatted grounded prompt text.
            response_schema: Target Pydantic schema class.

        Returns:
            Tuple of (validated_pydantic_instance, latency_seconds, usage_metadata)
        """
        logger.debug("Dispatching request to Gemini API (model: %s)", self.model_name)
        start_time = time.perf_counter()

        # Clean schema dict if Pydantic model passed
        cleaned_schema = None
        if hasattr(response_schema, "model_json_schema"):
            try:
                raw_schema_dict = response_schema.model_json_schema()
                cleaned_schema = _clean_schema_for_gemini(raw_schema_dict)
            except Exception:
                cleaned_schema = None

        config_kwargs: Dict[str, Any] = {
            "response_mime_type": "application/json",
            "temperature": 0.1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        if cleaned_schema:
            config_kwargs["response_schema"] = cleaned_schema

        models_to_try = [self.model_name] + [m for m in self.FALLBACK_MODELS if m != self.model_name]
        response = None
        last_error = None

        for target_model in models_to_try:
            try:
                response = self.client.models.generate_content(
                    model=target_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(**config_kwargs),
                )
                self.model_name = target_model
                break
            except Exception as api_err:
                last_error = api_err
                err_str = str(api_err)
                if "404" in err_str or "NOT_FOUND" in err_str or "no longer available" in err_str:
                    logger.warning("Model '%s' returned 404 NOT_FOUND. Trying fallback model...", target_model)
                    continue
                elif any(term in err_str for term in ["additionalProperties", "response_schema", "400", "INVALID_ARGUMENT"]):
                    logger.warning("Gemini Developer API mode rejected schema config (%s). Retrying JSON mode.", api_err)
                    try:
                        response = self.client.models.generate_content(
                            model=target_model,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                temperature=0.1,
                                top_p=0.95,
                                top_k=40,
                                max_output_tokens=8192,
                            ),
                        )
                        self.model_name = target_model
                        break
                    except Exception as inner_err:
                        last_error = inner_err
                        if "404" in str(inner_err) or "NOT_FOUND" in str(inner_err):
                            continue
                        raise inner_err
                else:
                    raise api_err

        if response is None:
            raise last_error or RuntimeError("Failed to generate content with available Gemini models.")

        latency_seconds = round(time.perf_counter() - start_time, 3)

        # Check candidate output tokens and finish reason
        if hasattr(response, "candidates") and response.candidates:
            finish_reason = getattr(response.candidates[0], "finish_reason", None)
            if str(finish_reason).upper() == "MAX_TOKENS":
                logger.warning("Gemini output was truncated due to MAX_TOKENS limit! Triggering retry.")
                raise ValueError("Response truncated due to token limit.")

        response_text = response.text
        if not response_text or not response_text.strip():
            logger.warning("Empty response received from Gemini. Triggering retry.")
            raise ValueError("Received empty or blank response text from Gemini API.")

        # Parse and Validate JSON using Pydantic v2
        try:
            parsed_json = json.loads(response_text)
            if issubclass(response_schema, OnboardingPlanResponse):
                validated_obj = OnboardingPlanResponse.model_validate(parsed_json)
            elif issubclass(response_schema, OnboardingModule):
                validated_obj = OnboardingModule.model_validate(parsed_json)
            elif issubclass(response_schema, BaseModel):
                validated_obj = response_schema.model_validate(parsed_json)
            else:
                validated_obj = parsed_json
        except (json.JSONDecodeError, ValidationError) as parse_err:
            logger.error("Response validation failed against schema %s: %s", response_schema.__name__, parse_err)
            raise parse_err

        usage = getattr(response, "usage_metadata", None)
        return validated_obj, latency_seconds, usage

    def generate_onboarding_plan(
        self,
        role_name: str,
        role_id: str,
        mandatory_requirements: List[str],
        document_chunks: List[Dict[str, Any]],
        department: str = "Engineering",
        experience_level: str = "Mid-Level",
    ) -> OnboardingPlanResponse:
        """Generate, validate, and track a full role-specific onboarding plan with telemetry.

        Args:
            role_name: Title of the target role (e.g. 'DevOps Engineer').
            role_id: Unique identifier for the role (e.g. 'ROLE-DEVOPS-01').
            mandatory_requirements: List of mandatory requirement statements.
            document_chunks: Ground-truth document chunks with metadata citations.
            department: Department name.
            experience_level: Target employee experience level.

        Returns:
            Validated OnboardingPlanResponse instance populated with full telemetry.
        """
        prompt = build_onboarding_plan_prompt(
            role_name=role_name,
            mandatory_requirements=mandatory_requirements,
            document_chunks=document_chunks,
            department=department,
            experience_level=experience_level,
        )

        logger.info(
            "Generating onboarding plan for role '%s' (ID: %s) using prompt version %s",
            role_name,
            role_id,
            PROMPT_VERSION,
        )

        timestamp_iso = datetime.now(timezone.utc).isoformat()

        # Extract document versions for telemetry
        doc_versions = {}
        for chunk in document_chunks:
            doc_id = str(chunk.get("doc_id", "UNKNOWN")).strip()
            ver = str(chunk.get("version", "1.0")).strip()
            doc_versions[doc_id] = ver

        try:
            plan_response, latency_seconds, usage = self._execute_api_and_validate(
                prompt=prompt,
                response_schema=OnboardingPlanResponse,
            )

            # Telemetry metadata
            prompt_tokens = getattr(usage, "prompt_token_count", None) if usage else None
            candidates_tokens = getattr(usage, "candidates_token_count", None) if usage else None
            total_tokens = getattr(usage, "total_token_count", None) if usage else None

            plan_response.raw_generation_metadata = GenerationMetadata(
                model_name=self.model_name,
                prompt_version=PROMPT_VERSION,
                timestamp=timestamp_iso,
                latency_seconds=latency_seconds,
                prompt_token_count=prompt_tokens,
                candidates_token_count=candidates_tokens,
                total_token_count=total_tokens,
                document_chunks_count=len(document_chunks),
                requirements_count=len(mandatory_requirements),
                source_document_versions=doc_versions,
                temperature=0.1,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
            )

            if not plan_response.role_id:
                plan_response.role_id = role_id
            if not plan_response.target_role:
                plan_response.target_role = role_name

            logger.info(
                "Successfully generated onboarding plan in %.3fs for role '%s' (%d modules)",
                latency_seconds,
                role_name,
                len(plan_response.modules),
            )
            return plan_response

        except Exception as exc:
            logger.error("Generation pipeline failed for role '%s' after retries: %s. Generating fallback plan.", role_name, exc)
            return self._generate_fallback_plan(role_name, role_id, mandatory_requirements, document_chunks, exc)

    def selective_regenerate_module(
        self,
        module_id: str,
        role_name: str,
        affected_section_ids: List[str],
        updated_document_chunks: List[Dict[str, Any]],
        mandatory_requirements: List[str],
    ) -> OnboardingModule:
        """Regenerate ONLY the specified module affected by a policy update (SRS Steps 57–59).

        Args:
            module_id: ID of the module to selectively re-run (e.g. 'MOD-WK1').
            role_name: Job role title.
            affected_section_ids: Policy section IDs that changed.
            updated_document_chunks: New updated document text chunks.
            mandatory_requirements: Role requirements.

        Returns:
            Regenerated OnboardingModule instance.
        """
        prompt = build_selective_module_regeneration_prompt(
            target_module_id=module_id,
            role_name=role_name,
            affected_section_ids=affected_section_ids,
            updated_document_chunks=updated_document_chunks,
            mandatory_requirements=mandatory_requirements,
        )

        logger.info(
            "Executing selective regeneration for module '%s' (Role: %s) due to policy update in sections: %s",
            module_id,
            role_name,
            affected_section_ids,
        )

        try:
            module_response, latency_seconds, _ = self._execute_api_and_validate(
                prompt=prompt,
                response_schema=OnboardingModule,
            )
            logger.info("Successfully selectively regenerated module '%s' in %.3fs", module_id, latency_seconds)
            return module_response
        except Exception as exc:
            logger.error("Selective module regeneration failed for '%s': %s", module_id, exc)
            raise RuntimeError(f"Selective module regeneration failed for {module_id}: {exc}") from exc

    def evaluate_generation_consistency(
        self,
        role_name: str,
        role_id: str,
        mandatory_requirements: List[str],
        document_chunks: List[Dict[str, Any]],
        runs: int = 3,
    ) -> Dict[str, Any]:
        """Perform automated consistency testing across repeated generation passes (SRS Steps 44–45).

        Args:
            role_name: Target job role.
            role_id: Role identifier.
            mandatory_requirements: Mandatory policy list.
            document_chunks: Ground truth chunks.
            runs: Number of repeated generation passes to execute (default: 3).

        Returns:
            Dict containing consistency_score (0-100), total_runs, variance_detected, and details.
        """
        logger.info("Initiating GenAI consistency evaluation (%d repeated passes) for role '%s'", runs, role_name)
        generated_plans: List[OnboardingPlanResponse] = []

        for run_idx in range(1, runs + 1):
            logger.info("Consistency Pass %d/%d for role '%s'", run_idx, runs, role_name)
            plan = self.generate_onboarding_plan(
                role_name=role_name,
                role_id=role_id,
                mandatory_requirements=mandatory_requirements,
                document_chunks=document_chunks,
            )
            generated_plans.append(plan)

        if not generated_plans:
            return {"consistency_score": 0.0, "error": "No plans generated"}

        # Calculate consistency metrics across runs
        module_counts = [len(p.modules) for p in generated_plans]
        task_counts = [sum(len(m.tasks) for m in p.modules) for p in generated_plans]
        citation_counts = [
            sum(sum(len(t.source_citations) for t in m.tasks) for m in p.modules)
            for p in generated_plans
        ]

        module_count_match = len(set(module_counts)) == 1
        task_count_diff = max(task_counts) - min(task_counts)
        citation_count_diff = max(citation_counts) - min(citation_counts)

        # Base score starts at 100
        score = 100.0
        variances = []

        if not module_count_match:
            score -= 20.0
            variances.append(f"Module count variance across runs: {module_counts}")

        if task_count_diff > 2:
            score -= (task_count_diff * 5.0)
            variances.append(f"Task count variance across runs: {task_counts}")

        if citation_count_diff > 3:
            score -= (citation_count_diff * 3.0)
            variances.append(f"Citation count variance across runs: {citation_counts}")

        final_consistency_score = max(0.0, min(100.0, score))

        logger.info(
            "Consistency evaluation complete! Score: %.1f/100 (Variances: %d)",
            final_consistency_score,
            len(variances),
        )

        return {
            "role_id": role_id,
            "role_name": role_name,
            "runs_executed": runs,
            "consistency_score": round(final_consistency_score, 2),
            "is_highly_consistent": final_consistency_score >= 85.0,
            "variances": variances,
            "metrics_summary": {
                "module_counts": module_counts,
                "task_counts": task_counts,
                "citation_counts": citation_counts,
            },
        }

    def _generate_fallback_plan(
        self,
        role_name: str,
        role_id: str,
        mandatory_requirements: List[str],
        document_chunks: List[Dict[str, Any]],
        error: Exception,
    ) -> OnboardingPlanResponse:
        """Structured error recovery fallback generator when API retries are exhausted (SRS Step 63)."""
        doc_id = document_chunks[0].get("doc_id", "DOC-FALLBACK-01") if document_chunks else "DOC-FALLBACK-01"
        sec_id = document_chunks[0].get("section_id", "Sec 1.0") if document_chunks else "Sec 1.0"

        citation = SourceCitation(
            requirement_id="REQ-FALLBACK-01",
            doc_id=doc_id,
            section_id=sec_id,
            page_number=1,
        )

        fallback_task = LearningTask(
            task_id="TASK-FALLBACK-101",
            title=f"Review Corporate Onboarding Policy ({role_name})",
            description=f"Automated fallback task generated due to API execution notice: {str(error)[:100]}",
            expected_outcome="Manual review of baseline corporate policies.",
            completion_criteria="Acknowledge policy review with reporting manager.",
            difficulty=DifficultyLevel.BEGINNER,
            due_stage=OnboardingStage.DAY_1,
            estimated_hours=2.0,
            requirement_id="REQ-FALLBACK-01",
            mandatory_policy_refs=["POL-FALLBACK-01"],
            source_citations=[citation],
        )

        fallback_module = OnboardingModule(
            module_id="MOD-FALLBACK-WK1",
            week_number=1,
            stage=OnboardingStage.DAY_1,
            title="Week 1: Baseline Orientation & Compliance (Fallback)",
            purpose="Emergency fallback orientation module",
            tasks=[fallback_task],
        )

        return OnboardingPlanResponse(
            plan_id="PLAN-FALLBACK-RECOVERY",
            role_id=role_id,
            target_role=role_name,
            total_duration_days=30,
            stages_included=[OnboardingStage.DAY_1],
            modules=[fallback_module],
            raw_generation_metadata=GenerationMetadata(
                model_name=self.model_name,
                prompt_version=PROMPT_VERSION,
                timestamp=datetime.now(timezone.utc).isoformat(),
                latency_seconds=0.0,
            ),
        )
