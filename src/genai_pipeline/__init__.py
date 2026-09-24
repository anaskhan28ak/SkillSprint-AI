"""GenAI pipeline package for SkillSprint AI."""

from src.genai_pipeline.gemini_client import GeminiPipelineEngine
from src.genai_pipeline.prompt_templates import (
    PROMPT_VERSION,
    build_onboarding_plan_prompt,
    build_selective_module_regeneration_prompt,
    format_document_chunks,
)
from src.genai_pipeline.schemas import (
    Assessment,
    AssessmentRubric,
    AssessmentType,
    ChecklistItem,
    DifficultyLevel,
    GenerationMetadata,
    LearningTask,
    OnboardingModule,
    OnboardingPlanResponse,
    OnboardingStage,
    QuestionType,
    QuizQuestion,
    ScenarioActivity,
    SourceCitation,
)

__all__ = [
    "GeminiPipelineEngine",
    "PROMPT_VERSION",
    "build_onboarding_plan_prompt",
    "build_selective_module_regeneration_prompt",
    "format_document_chunks",
    "OnboardingStage",
    "DifficultyLevel",
    "QuestionType",
    "AssessmentType",
    "GenerationMetadata",
    "SourceCitation",
    "ChecklistItem",
    "QuizQuestion",
    "LearningTask",
    "ScenarioActivity",
    "AssessmentRubric",
    "Assessment",
    "OnboardingModule",
    "OnboardingPlanResponse",
]
