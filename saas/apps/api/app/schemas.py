from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

JobKind = Literal["solution_video", "hybrid_lesson"]
JobStatus = Literal["draft", "queued", "running", "succeeded", "failed", "cancelled"]
StageName = Literal["extract", "script", "render_manim", "render_prologue", "render_svg", "compose", "upload"]
StepStatus = Literal["pending", "running", "succeeded", "failed", "skipped"]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class User(BaseModel):
    id: UUID
    email: str
    plan: str
    limits: dict[str, Any]


class RenderOptions(BaseModel):
    languages: list[str]
    kinds: list[dict[str, Any]]
    detail_levels: list[str]
    resolutions: list[str]
    target_seconds: dict[str, int]
    limits: dict[str, int]
    voices: list[str]


class UploadInitRequest(Strict):
    filename: str = Field(min_length=1, max_length=255)
    size_bytes: int = Field(gt=0)
    sha256: str = Field(pattern=r"^[0-9a-fA-F]{64}$")


class UploadInitResponse(BaseModel):
    file_id: UUID
    upload_url: str
    method: Literal["PUT"] = "PUT"
    headers: dict[str, str]
    expires_at: datetime


class UploadCompleteResponse(BaseModel):
    file_id: UUID
    status: Literal["analyzed"]
    page_count: int
    has_text_layer: bool
    ocr_required: bool
    sha256: str


class JobConfig(Strict):
    language: str = "es"
    detail_level: str = "standard"
    target_seconds: int = Field(gt=0)
    resolution: str = "720p"
    include_prologue: bool = False


class EstimateRequest(Strict):
    pdf_file_id: UUID
    kind: JobKind
    config: JobConfig


class JobEstimate(BaseModel):
    estimate_id: UUID
    estimate_hash: str
    kind: JobKind
    estimated_credits: int
    max_credits: int
    estimated_seconds: int
    breakdown: dict[str, Any]
    pricing_version: str
    expires_at: datetime
    available_credits: int
    sufficient_credits: bool


class CreateJobRequest(Strict):
    estimate_id: UUID
    estimate_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    max_authorized_credits: int = Field(gt=0)


class Stage(BaseModel):
    stage: StageName
    status: StepStatus
    attempt: int = 1
    started_at: datetime | None = None
    finished_at: datetime | None = None


class SceneItem(BaseModel):
    label: str
    engine: Literal["manim", "threejs", "svg"]
    status: StepStatus
    planned_seconds: float


class Scenes(BaseModel):
    total: int
    by_status: dict[str, int]
    items: list[SceneItem]


class VideoInfo(BaseModel):
    duration_seconds: float
    width: int
    height: int
    fps: int
    size_bytes: int


class Job(BaseModel):
    id: UUID
    kind: JobKind
    status: JobStatus
    current_stage: StageName | None
    progress_pct: int
    include_prologue: bool
    config: dict[str, Any]
    estimated_credits: int | None
    max_authorized_credits: int | None
    reserved_credits: int
    final_credits: int | None
    cancel_requested: bool
    error_code: str | None
    error_message: str | None
    created_at: datetime
    queued_at: datetime | None
    started_at: datetime | None
    finished_at: datetime | None
    stages: list[Stage]
    scenes: Scenes
    video: VideoInfo | None


class JobPage(BaseModel):
    items: list[Job]
    next_cursor: str | None


class JobAssets(BaseModel):
    video_url: str
    share_url: str | None
    expires_in_seconds: int


class CreditsBalance(BaseModel):
    available: int
    held: int
    total: int


class LedgerEntry(BaseModel):
    id: int
    entry_type: str
    delta: int
    job_id: UUID | None
    reason: str | None
    created_at: datetime


class LedgerPage(BaseModel):
    items: list[LedgerEntry]
    next_cursor: str | None
