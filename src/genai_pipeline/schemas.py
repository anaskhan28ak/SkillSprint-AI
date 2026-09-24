"""Pydantic v2 schemas for the SkillSprint AI GenAI Generation Engine.

These schemas define the structural contracts enforced on the Gemini LLM
via Structured Outputs (`response_schema`), ensuring strict JSON responses,
deterministic typing, validation constraints, and 100% source traceability metadata.
(SRS Steps 12–25, 37–38, 41).
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class OnboardingStage(str, Enum):
    """Configurable multi-stage onboarding timeline periods (SRS Step 13)."""

    DAY_1 = "Day 1"
    WEEK_1 = "Week 1"
    WEEK_2 = "Week 2"
    FIRST_30_DAYS = "First 30 Days"
    FIRST_60_DAYS = "First 60 Days"
    FIRST_90_DAYS = "First 90 Days"


class DifficultyLevel(str, Enum):
    """Competency and task difficulty levels (SRS Step 25)."""

    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class QuestionType(str, Enum):
    """Supported quiz question types (SRS Step 20)."""

    MULTIPLE_CHOICE = "Multiple Choice"
    MULTIPLE_RESPONSE = "Multiple Response"
    TRUE_FALSE = "True/False"
    SCENARIO_BASED = "Scenario-based"


class AssessmentType(str, Enum):
    """Categories of practical and knowledge assessments (SRS Step 23)."""

    KNOWLEDGE = "Knowledge Assessment"
    PRACTICAL = "Practical Assessment"
    SCENARIO = "Scenario Assessment"
    ROLE_SPECIFIC = "Role-Specific Assessment"


class GenerationMetadata(BaseModel):
    """Execution telemetry and audit metadata populated during pipeline generation (SRS Step 41, 65)."""

    model_config = ConfigDict(populate_by_name=True)

    model_name: str = Field(
        default="gemini-2.5-flash",
        description="Name of the generative model used for execution.",
    )
    prompt_version: str = Field(
        default="2.0.0",
        description="Semantic version of the prompt template employed.",
    )
    timestamp: str = Field(
        default="",
        description="ISO-8601 UTC timestamp of the generation event.",
    )
    latency_seconds: float = Field(
        default=0.0,
        description="Total round-trip time in seconds.",
    )
    prompt_token_count: Optional[int] = Field(
        default=None,
        description="Total input prompt tokens consumed.",
    )
    candidates_token_count: Optional[int] = Field(
        default=None,
        description="Total output candidate tokens generated.",
    )
    total_token_count: Optional[int] = Field(
        default=None,
        description="Total combined token usage.",
    )
    document_chunks_count: int = Field(
        default=0,
        description="Number of ground-truth chunks fed into the prompt.",
    )
    requirements_count: int = Field(
        default=0,
        description="Number of mandatory requirements processed.",
    )
    source_document_versions: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of doc_id to document version string.",
    )
    temperature: float = Field(
        default=0.1,
        description="Sampling temperature parameter used.",
    )
    top_p: float = Field(
        default=0.95,
        description="Top-p nucleus sampling parameter used.",
    )
    top_k: int = Field(
        default=40,
        description="Top-k sampling parameter used.",
    )
    max_output_tokens: int = Field(
        default=8192,
        description="Maximum token limit configured for generation.",
    )


class SourceCitation(BaseModel):
    """Exact citation identifying the ground-truth document source and requirement ID (SRS Step 15, 21, 30)."""

    model_config = ConfigDict(populate_by_name=True)

    requirement_id: str = Field(
        default="REQ-GEN-01",
        description="Unique requirement ID from Role Requirement Matrix mapped to this citation (e.g., 'REQ-SEC-01', 'REQ-DEV-04').",
    )
    doc_id: str = Field(
        ...,
        description="Unique identifier of the company policy document (e.g., 'HR-LEAVE-2024-V1').",
    )
    section_id: str = Field(
        default="N/A",
        description="Specific clause, section header, or subsection ID referenced (e.g., 'Sec 4.2', 'Clause 3.1.b').",
    )
    page_number: int = Field(
        default=1,
        ge=1,
        description="1-based page number where the policy condition or fact resides.",
    )


class ChecklistItem(BaseModel):
    """Actionable onboarding checklist item with assigned stage and source (SRS Step 17)."""

    model_config = ConfigDict(populate_by_name=True)

    item_id: str = Field(
        ...,
        description="Unique checklist item ID (e.g., 'CHK-101').",
    )
    activity: str = Field(
        ...,
        description="Specific onboarding activity statement.",
    )
    is_required: bool = Field(
        default=True,
        description="Indicates whether this item is mandatory or optional.",
    )
    due_stage: OnboardingStage = Field(
        default=OnboardingStage.DAY_1,
        description="Target onboarding stage when activity must be completed.",
    )
    completion_status: str = Field(
        default="Pending",
        description="Initial completion status ('Pending', 'In Progress', 'Completed').",
    )
    responsible_person: str = Field(
        default="Employee",
        description="Person responsible for verifying completion (e.g., 'Employee', 'Reporting Manager', 'IT Admin').",
    )
    requirement_id: str = Field(
        default="REQ-CHK-01",
        description="Requirement ID satisfied by this checklist item.",
    )
    source_citation: SourceCitation = Field(
        ...,
        description="Source document citation grounding this checklist item.",
    )


class QuizQuestion(BaseModel):
    """Multiple-choice quiz question derived strictly from cited policy documents (SRS Steps 20-22)."""

    model_config = ConfigDict(populate_by_name=True)

    question_id: str = Field(
        ...,
        description="Unique identifier for the quiz question (e.g., 'QZ-101', 'QZ-WK1-01').",
    )
    question: str = Field(
        ...,
        description="Clear, unambiguous question text based strictly on ground-truth source material.",
    )
    question_type: QuestionType = Field(
        default=QuestionType.MULTIPLE_CHOICE,
        description="Classification of quiz question type.",
    )
    options: List[str] = Field(
        ...,
        min_length=2,
        max_length=6,
        description="Answer options (min 2 for True/False, 4 for Multiple Choice).",
    )
    correct_answer: str = Field(
        ...,
        description="The exact text string corresponding to the correct option.",
    )
    explanation: str = Field(
        ...,
        description="Clear source-grounded explanation explaining why the answer is correct.",
    )
    distractor_notes: Optional[str] = Field(
        default=None,
        description="Plausibility notes ensuring incorrect options do not mislead or contradict source material.",
    )
    difficulty: DifficultyLevel = Field(
        default=DifficultyLevel.BEGINNER,
        description="Assigned difficulty level based on role requirements.",
    )
    requirement_id: str = Field(
        default="REQ-QZ-01",
        description="Requirement ID validated by this quiz question.",
    )
    source_citation: SourceCitation = Field(
        ...,
        description="Precise ground-truth citation supporting the question and correct answer.",
    )


class LearningTask(BaseModel):
    """Actionable onboarding task mapped to organizational policy and role requirements (SRS Step 18, 25)."""

    model_config = ConfigDict(populate_by_name=True)

    task_id: str = Field(
        ...,
        description="Unique task identifier in uppercase hyphenated notation (e.g., 'TASK-101').",
    )
    title: str = Field(
        ...,
        description="Action-oriented concise task title.",
    )
    description: str = Field(
        ...,
        description="Detailed step-by-step instructions and expectations to complete the task.",
    )
    expected_outcome: str = Field(
        default="Task completed according to corporate policy guidelines.",
        description="Measurable deliverable or artifact expected upon completion.",
    )
    completion_criteria: str = Field(
        default="Pass verification test and submit manager sign-off.",
        description="Specific criteria used to confirm task completion.",
    )
    difficulty: DifficultyLevel = Field(
        default=DifficultyLevel.BEGINNER,
        description="Difficulty level of the task.",
    )
    due_stage: OnboardingStage = Field(
        default=OnboardingStage.WEEK_1,
        description="Onboarding stage milestone by which task is due.",
    )
    estimated_hours: float = Field(
        ...,
        ge=0.5,
        le=40.0,
        description="Estimated time required to complete the task in hours (min 0.5, max 40.0).",
    )
    requirement_id: str = Field(
        default="REQ-TSK-01",
        description="Primary requirement ID mapped from Role Requirement Matrix.",
    )
    mandatory_policy_refs: List[str] = Field(
        default_factory=list,
        description="List of relevant policy codes or requirement IDs satisfied by this task.",
    )
    source_citations: List[SourceCitation] = Field(
        default_factory=list,
        description="List of valid source citations supporting this task (minimum 1 required).",
    )


class ScenarioActivity(BaseModel):
    """Interactive scenario-based activity simulating workplace workflows (SRS Step 19)."""

    model_config = ConfigDict(populate_by_name=True)

    scenario_id: str = Field(
        ...,
        description="Unique scenario activity identifier (e.g., 'SCN-101').",
    )
    title: str = Field(
        ...,
        description="Title of the scenario activity.",
    )
    context: str = Field(
        ...,
        description="Realistic workplace background scenario context.",
    )
    problem_statement: str = Field(
        ...,
        description="Specific challenge or issue the employee must resolve.",
    )
    required_actions: List[str] = Field(
        ...,
        description="Step-by-step actions required to execute the scenario.",
    )
    expected_decision: str = Field(
        ...,
        description="Correct policy-compliant decision or solution path.",
    )
    evaluation_rubric: str = Field(
        ...,
        description="Criteria for evaluating employee performance in this scenario.",
    )
    difficulty: DifficultyLevel = Field(
        default=DifficultyLevel.INTERMEDIATE,
        description="Difficulty rating of the scenario.",
    )
    due_stage: OnboardingStage = Field(
        default=OnboardingStage.WEEK_2,
        description="Stage deadline for performing scenario activity.",
    )
    requirement_id: str = Field(
        default="REQ-SCN-01",
        description="Mapped requirement ID.",
    )
    source_citations: List[SourceCitation] = Field(
        default_factory=list,
        description="Citations supporting the scenario process logic.",
    )


class AssessmentRubric(BaseModel):
    """Structured rubric criteria for assessing practical tasks (SRS Step 24)."""

    model_config = ConfigDict(populate_by_name=True)

    rubric_id: str = Field(
        ...,
        description="Unique rubric item ID (e.g., 'RUB-01').",
    )
    criterion: str = Field(
        ...,
        description="Evaluation criterion statement.",
    )
    weight: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Weight proportion of this criterion (0.0 to 1.0).",
    )
    expected_performance: str = Field(
        ...,
        description="Description of expected performance to meet standard.",
    )
    pass_condition: str = Field(
        ...,
        description="Condition required to achieve a passing grade for this rubric.",
    )


class Assessment(BaseModel):
    """Comprehensive knowledge or practical assessment (SRS Step 23, 24)."""

    model_config = ConfigDict(populate_by_name=True)

    assessment_id: str = Field(
        ...,
        description="Unique assessment ID (e.g., 'ASM-WK1').",
    )
    title: str = Field(
        ...,
        description="Assessment title.",
    )
    assessment_type: AssessmentType = Field(
        default=AssessmentType.KNOWLEDGE,
        description="Type of assessment.",
    )
    description: str = Field(
        ...,
        description="Overview of assessment scope and guidelines.",
    )
    passing_score_percentage: float = Field(
        default=80.0,
        ge=50.0,
        le=100.0,
        description="Minimum score percentage required to pass.",
    )
    rubrics: List[AssessmentRubric] = Field(
        default_factory=list,
        description="Structured rubrics for evaluating practical submissions.",
    )
    requirement_id: str = Field(
        default="REQ-ASM-01",
        description="Mapped requirement ID.",
    )
    source_citations: List[SourceCitation] = Field(
        default_factory=list,
        description="Source citations grounding the assessment.",
    )


class OnboardingModule(BaseModel):
    """Chronologically sequenced module grouping weekly tasks, checklists, scenarios, and quizzes (SRS Step 14-15)."""

    model_config = ConfigDict(populate_by_name=True)

    module_id: str = Field(
        ...,
        description="Unique module identifier (e.g., 'MOD-WK1', 'MOD-WK2').",
    )
    week_number: int = Field(
        ...,
        ge=1,
        le=12,
        description="Chronological week index for the module (1 through 12).",
    )
    stage: OnboardingStage = Field(
        default=OnboardingStage.WEEK_1,
        description="Corresponding multi-stage onboarding period.",
    )
    title: str = Field(
        ...,
        description="Thematic module title indicating focus area.",
    )
    purpose: str = Field(
        default="Establish baseline role compliance and operational skills.",
        description="High-level purpose statement of the module.",
    )
    learning_objectives: List[str] = Field(
        default_factory=list,
        description="Specific measurable learning objectives for this module.",
    )
    key_concepts: List[str] = Field(
        default_factory=list,
        description="Key corporate policies and domain concepts covered.",
    )
    estimated_duration_hours: float = Field(
        default=10.0,
        ge=1.0,
        le=80.0,
        description="Total estimated hours required to complete module.",
    )
    completion_criteria: str = Field(
        default="Complete all tasks, checklist items, scenarios, and pass quizzes with >= 80%.",
        description="Module completion criteria.",
    )
    checklists: List[ChecklistItem] = Field(
        default_factory=list,
        description="Onboarding checklist items associated with this module.",
    )
    tasks: List[LearningTask] = Field(
        ...,
        min_length=1,
        description="List of actionable learning tasks required for this module.",
    )
    scenarios: List[ScenarioActivity] = Field(
        default_factory=list,
        description="Practical scenario-based activities.",
    )
    quizzes: List[QuizQuestion] = Field(
        default_factory=list,
        description="Knowledge validation quizzes mapped directly to module learning materials.",
    )
    assessments: List[Assessment] = Field(
        default_factory=list,
        description="Formal assessments and practical rubrics for the module.",
    )


class OnboardingPlanResponse(BaseModel):
    """Root response model encapsulating a full role-specific onboarding plan (SRS Step 12, 37)."""

    model_config = ConfigDict(populate_by_name=True)

    plan_id: str = Field(
        default="PLAN-DEFAULT",
        description="Unique identifier for the generated onboarding plan.",
    )
    role_id: str = Field(
        ...,
        description="Unique identifier of the target role (e.g., 'ROLE-DEVOPS-01').",
    )
    target_role: str = Field(
        ...,
        description="Official title of the target job role (e.g., 'DevOps Engineer').",
    )
    department: str = Field(
        default="Engineering",
        description="Department of the employee role.",
    )
    experience_level: str = Field(
        default="Junior / Mid-Level",
        description="Target experience level of the employee.",
    )
    total_duration_days: int = Field(
        ...,
        ge=1,
        description="Calculated total onboarding timeline in calendar days.",
    )
    stages_included: List[OnboardingStage] = Field(
        default_factory=lambda: [OnboardingStage.DAY_1, OnboardingStage.WEEK_1, OnboardingStage.FIRST_30_DAYS],
        description="List of stages configured in this plan.",
    )
    modules: List[OnboardingModule] = Field(
        ...,
        min_length=1,
        description="Chronologically ordered sequence of onboarding modules.",
    )
    raw_generation_metadata: GenerationMetadata = Field(
        default_factory=GenerationMetadata,
        description="Audit telemetry: model name, latency, token metrics, timestamp, prompt version.",
    )
