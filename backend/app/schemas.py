from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


PostStatus = Literal["draft", "liked", "planned", "published", "archived"]
GenerationMode = Literal["auto", "guided"]


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ContentProfileBase(BaseModel):
    name: str | None = None
    profile_type: str | None = None
    source_description: str | None = None
    niche: str | None = None
    description: str | None = None
    offer_or_focus: str | None = None
    audience: str | None = None
    geography: str | None = None
    tone: str | None = None
    goals: str | None = None
    platforms: list[str] = Field(default_factory=list)
    language: str = "ru"
    positioning: str | None = None
    content_pillars: list[str] = Field(default_factory=list)
    platform_strategy: dict[str, Any] = Field(default_factory=dict)
    favorite_words: str | None = None
    forbidden_words: str | None = None
    avoid_topics: str | None = None
    additional_notes: str | None = None


class ContentProfileCreate(ContentProfileBase):
    name: str


class ContentProfileUpdate(BaseModel):
    name: str | None = None
    profile_type: str | None = None
    source_description: str | None = None
    niche: str | None = None
    description: str | None = None
    offer_or_focus: str | None = None
    audience: str | None = None
    geography: str | None = None
    tone: str | None = None
    goals: str | None = None
    platforms: list[str] | None = None
    language: str | None = None
    positioning: str | None = None
    content_pillars: list[str] | None = None
    platform_strategy: dict[str, Any] | None = None
    favorite_words: str | None = None
    forbidden_words: str | None = None
    avoid_topics: str | None = None
    additional_notes: str | None = None


class ContentProfileRead(ContentProfileBase, ORMModel):
    id: int
    user_id: int
    name: str
    created_at: datetime
    updated_at: datetime


class AnalyzeDescriptionRequest(BaseModel):
    description: str
    language: str = "ru"


class TextStyleBase(BaseModel):
    profile_id: int | None = None
    name: str | None = None
    description: str | None = None
    rules: str | None = None
    examples: list[str] = Field(default_factory=list)
    emoji_level: str = "low"
    post_length: str = "medium"
    cta_style: str = "soft"


class TextStyleCreate(TextStyleBase):
    name: str


class TextStyleUpdate(BaseModel):
    profile_id: int | None = None
    name: str | None = None
    description: str | None = None
    rules: str | None = None
    examples: list[str] | None = None
    emoji_level: str | None = None
    post_length: str | None = None
    cta_style: str | None = None


class TextStyleRead(TextStyleBase, ORMModel):
    id: int
    user_id: int
    name: str
    created_at: datetime
    updated_at: datetime


class ImageStyleBase(BaseModel):
    profile_id: int | None = None
    name: str | None = None
    description: str | None = None
    colors: list[str] = Field(default_factory=list)
    mood: str | None = None
    composition: str | None = None
    avoid: str | None = None
    prompt_addon: str | None = None


class ImageStyleCreate(ImageStyleBase):
    name: str


class ImageStyleUpdate(BaseModel):
    profile_id: int | None = None
    name: str | None = None
    description: str | None = None
    colors: list[str] | None = None
    mood: str | None = None
    composition: str | None = None
    avoid: str | None = None
    prompt_addon: str | None = None


class ImageStyleRead(ImageStyleBase, ORMModel):
    id: int
    user_id: int
    name: str
    created_at: datetime
    updated_at: datetime


class GeneratePostRequest(BaseModel):
    profile_id: int
    text_style_id: int | None = None
    image_style_id: int | None = None
    topic: str
    goal: str | None = None
    platforms: list[str] = Field(default_factory=lambda: ["instagram", "facebook", "x"])
    generation_mode: GenerationMode = "auto"
    input_request: str | None = None
    format: str = "post"
    length: str = "medium"
    language: str = "ru"
    model: str | None = None
    variants: int = Field(default=1, ge=1, le=5)
    save_to_history: bool = True


class PostUpdate(BaseModel):
    status: PostStatus | None = None
    tags: list[str] | None = None
    notes: str | None = None
    generated_content: dict[str, Any] | None = None


class PostRead(ORMModel):
    id: int
    user_id: int
    profile_id: int | None
    text_style_id: int | None
    image_style_id: int | None
    generation_session_id: int | None
    topic: str
    goal: str | None
    platforms: list[str]
    generation_mode: str
    input_request: str | None
    generated_content: dict[str, Any]
    image_prompt: dict[str, Any]
    image_url: str | None
    model_used: str | None
    status: str
    tags: list[str]
    notes: str | None
    score: dict[str, Any]
    analysis: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class GenerationSessionCreate(BaseModel):
    profile_id: int | None = None
    mode: GenerationMode = "guided"
    topic: str
    platforms: list[str] = Field(default_factory=list)


class GenerationSessionRead(ORMModel):
    id: int
    user_id: int
    profile_id: int | None
    mode: str
    topic: str
    platforms: list[str]
    current_step: str
    topic_analysis: dict[str, Any]
    expanded_angles: list[dict[str, Any]]
    hooks: list[dict[str, Any]]
    selected_hook: str | None
    drafts: list[dict[str, Any]]
    revision_requests: list[str]
    final_content: dict[str, Any]
    image_prompts: list[dict[str, Any]]
    platform_analysis: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class SettingsUpdate(BaseModel):
    provider: str | None = None
    text_model: str | None = None
    fast_model: str | None = None
    quality_model: str | None = None
    image_model: str | None = None
    daily_generation_limit: int | None = None
    default_language: str | None = None


class SettingsRead(ORMModel):
    id: int
    user_id: int
    provider: str
    text_model: str
    fast_model: str
    quality_model: str
    image_model: str
    api_key_encrypted_or_env: str
    daily_generation_limit: int
    default_language: str
    created_at: datetime
    updated_at: datetime


class GeneratedImagePrompt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: str
    negative_prompt: str = ""
    text_on_image: str = ""


class PlatformContent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    post: str = ""
    cta: str = ""
    format_notes: str = ""


class StoryFrame(BaseModel):
    model_config = ConfigDict(extra="forbid")

    screen: int
    text: str
    visual_idea: str


class ReelContent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    idea: str = ""
    script: str = ""
    shot_list: list[str] = Field(default_factory=list)


class GeneratedHook(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    why_it_can_work: str


class GeneratedAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hook_score: int = Field(ge=0, le=10)
    clarity_score: int = Field(ge=0, le=10)
    originality_score: int = Field(ge=0, le=10)
    platform_fit_score: int = Field(ge=0, le=10)
    viral_potential_score: int = Field(ge=0, le=10)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    improvement_suggestions: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)


class GeneratedResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instagram: PlatformContent = Field(default_factory=PlatformContent)
    facebook: PlatformContent = Field(default_factory=PlatformContent)
    x: PlatformContent = Field(default_factory=PlatformContent)
    linkedin: PlatformContent = Field(default_factory=PlatformContent)
    stories: list[StoryFrame] = Field(default_factory=list)
    reels: ReelContent = Field(default_factory=ReelContent)
    image_prompt: GeneratedImagePrompt
    hooks: list[GeneratedHook] = Field(default_factory=list)
    analysis: GeneratedAnalysis
