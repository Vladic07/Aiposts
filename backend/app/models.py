from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, select
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    profiles: Mapped[list[ContentProfile]] = relationship(back_populates="user", cascade="all, delete-orphan")


class ContentProfile(Base, TimestampMixin):
    __tablename__ = "content_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(160))
    profile_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    niche: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    offer_or_focus: Mapped[str | None] = mapped_column(Text, nullable=True)
    audience: Mapped[str | None] = mapped_column(Text, nullable=True)
    geography: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tone: Mapped[str | None] = mapped_column(Text, nullable=True)
    goals: Mapped[str | None] = mapped_column(Text, nullable=True)
    platforms: Mapped[list[str]] = mapped_column(JSON, default=list)
    language: Mapped[str] = mapped_column(String(32), default="ru")
    positioning: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_pillars: Mapped[list[str]] = mapped_column(JSON, default=list)
    platform_strategy: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    favorite_words: Mapped[str | None] = mapped_column(Text, nullable=True)
    forbidden_words: Mapped[str | None] = mapped_column(Text, nullable=True)
    avoid_topics: Mapped[str | None] = mapped_column(Text, nullable=True)
    additional_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User] = relationship(back_populates="profiles")
    text_styles: Mapped[list[TextStyle]] = relationship(back_populates="profile")
    image_styles: Mapped[list[ImageStyle]] = relationship(back_populates="profile")


class TextStyle(Base, TimestampMixin):
    __tablename__ = "text_styles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("content_profiles.id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    rules: Mapped[str | None] = mapped_column(Text, nullable=True)
    examples: Mapped[list[str]] = mapped_column(JSON, default=list)
    emoji_level: Mapped[str] = mapped_column(String(32), default="low")
    post_length: Mapped[str] = mapped_column(String(32), default="medium")
    cta_style: Mapped[str] = mapped_column(String(64), default="soft")

    profile: Mapped[ContentProfile | None] = relationship(back_populates="text_styles")


class ImageStyle(Base, TimestampMixin):
    __tablename__ = "image_styles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("content_profiles.id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    colors: Mapped[list[str]] = mapped_column(JSON, default=list)
    mood: Mapped[str | None] = mapped_column(Text, nullable=True)
    composition: Mapped[str | None] = mapped_column(Text, nullable=True)
    avoid: Mapped[str | None] = mapped_column(Text, nullable=True)
    prompt_addon: Mapped[str | None] = mapped_column(Text, nullable=True)

    profile: Mapped[ContentProfile | None] = relationship(back_populates="image_styles")


class GenerationSession(Base, TimestampMixin):
    __tablename__ = "generation_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("content_profiles.id"), nullable=True, index=True)
    mode: Mapped[str] = mapped_column(String(32), default="auto")
    topic: Mapped[str] = mapped_column(Text)
    platforms: Mapped[list[str]] = mapped_column(JSON, default=list)
    current_step: Mapped[str] = mapped_column(String(64), default="completed")
    topic_analysis: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    expanded_angles: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    hooks: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    selected_hook: Mapped[str | None] = mapped_column(Text, nullable=True)
    drafts: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    revision_requests: Mapped[list[str]] = mapped_column(JSON, default=list)
    final_content: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    image_prompts: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    platform_analysis: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("content_profiles.id"), nullable=True, index=True)
    text_style_id: Mapped[int | None] = mapped_column(ForeignKey("text_styles.id"), nullable=True)
    image_style_id: Mapped[int | None] = mapped_column(ForeignKey("image_styles.id"), nullable=True)
    generation_session_id: Mapped[int | None] = mapped_column(ForeignKey("generation_sessions.id"), nullable=True)
    topic: Mapped[str] = mapped_column(Text)
    goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    platforms: Mapped[list[str]] = mapped_column(JSON, default=list)
    generation_mode: Mapped[str] = mapped_column(String(32), default="auto")
    input_request: Mapped[str | None] = mapped_column(Text, nullable=True)
    generated_content: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    image_prompt: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_used: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="draft")
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    score: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    analysis: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class Settings(Base, TimestampMixin):
    __tablename__ = "settings"
    __table_args__ = (UniqueConstraint("user_id", name="uq_settings_user_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    provider: Mapped[str] = mapped_column(String(64), default="openai")
    text_model: Mapped[str] = mapped_column(String(120), default="gpt-5-mini")
    fast_model: Mapped[str] = mapped_column(String(120), default="gpt-5-mini")
    quality_model: Mapped[str] = mapped_column(String(120), default="gpt-5.2")
    image_model: Mapped[str] = mapped_column(String(120), default="gpt-image-1.5")
    api_key_encrypted_or_env: Mapped[str] = mapped_column(String(64), default="env")
    daily_generation_limit: Mapped[int] = mapped_column(default=100)
    default_language: Mapped[str] = mapped_column(String(32), default="ru")


def ensure_default_user(session: Session) -> User:
    user = session.scalar(select(User).where(User.email == "local@ai-content-studio"))
    if user:
        return user
    user = User(email="local@ai-content-studio", password_hash=None)
    session.add(user)
    session.flush()
    session.add(Settings(user_id=user.id))
    session.commit()
    session.refresh(user)
    return user


def get_default_user(session: Session) -> User:
    return ensure_default_user(session)
