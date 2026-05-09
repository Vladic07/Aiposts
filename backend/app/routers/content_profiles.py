from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import ContentProfile
from app.routers.utils import apply_updates, current_user_id, not_found
from app.schemas import (
    AnalyzeDescriptionRequest,
    ContentProfileCreate,
    ContentProfileRead,
    ContentProfileUpdate,
)


router = APIRouter(prefix="/api/content-profiles", tags=["content profiles"])


@router.get("", response_model=list[ContentProfileRead])
def list_profiles(session: Session = Depends(get_session)) -> list[ContentProfile]:
    user_id = current_user_id(session)
    return list(session.scalars(select(ContentProfile).where(ContentProfile.user_id == user_id).order_by(ContentProfile.updated_at.desc())))


@router.post("", response_model=ContentProfileRead, status_code=status.HTTP_201_CREATED)
def create_profile(payload: ContentProfileCreate, session: Session = Depends(get_session)) -> ContentProfile:
    profile = ContentProfile(user_id=current_user_id(session), **payload.model_dump())
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.get("/{profile_id}", response_model=ContentProfileRead)
def get_profile(profile_id: int, session: Session = Depends(get_session)) -> ContentProfile:
    profile = session.get(ContentProfile, profile_id)
    if not profile:
        raise not_found("Content profile")
    return profile


@router.put("/{profile_id}", response_model=ContentProfileRead)
def update_profile(profile_id: int, payload: ContentProfileUpdate, session: Session = Depends(get_session)) -> ContentProfile:
    profile = session.get(ContentProfile, profile_id)
    if not profile:
        raise not_found("Content profile")
    apply_updates(profile, payload.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(profile)
    return profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int, session: Session = Depends(get_session)) -> None:
    profile = session.get(ContentProfile, profile_id)
    if not profile:
        raise not_found("Content profile")
    session.delete(profile)
    session.commit()


@router.post("/analyze-description", response_model=ContentProfileRead, status_code=status.HTTP_201_CREATED)
def analyze_description(payload: AnalyzeDescriptionRequest, session: Session = Depends(get_session)) -> ContentProfile:
    description = payload.description.strip()
    if not description:
        raise HTTPException(status_code=422, detail="Description is required")
    profile = ContentProfile(
        user_id=current_user_id(session),
        name=description[:80],
        profile_type="custom profile",
        source_description=description,
        niche=description[:160],
        description=f"Structured profile draft based on: {description}",
        audience="People interested in this topic",
        tone="specific, clear, practical",
        goals="Create useful social content consistently",
        platforms=["instagram", "facebook", "x", "linkedin"],
        language=payload.language,
        positioning="Practical voice with concrete examples",
        content_pillars=["ideas", "examples", "lessons", "practical tips"],
        platform_strategy={
            "instagram": "visual captions and carousel ideas",
            "x": "short hooks and concise observations",
            "linkedin": "structured expert posts",
        },
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.post("/improve", response_model=ContentProfileRead)
def improve_profile(payload: ContentProfileUpdate, session: Session = Depends(get_session)) -> ContentProfile:
    if not payload.name:
        raise HTTPException(status_code=422, detail="Profile name is required")
    profile = ContentProfile(
        user_id=current_user_id(session),
        name=payload.name,
        profile_type=payload.profile_type or "custom profile",
        source_description=payload.source_description,
        niche=payload.niche,
        description=payload.description or "Improved profile draft",
        audience=payload.audience or "Defined target audience",
        tone=payload.tone or "clear and concrete",
        goals=payload.goals or "Create consistent social content",
        platforms=payload.platforms or ["instagram", "facebook", "x"],
        language=payload.language or "ru",
        positioning=payload.positioning or "Specific, useful perspective",
        content_pillars=payload.content_pillars or ["practical ideas", "examples", "lessons"],
        platform_strategy=payload.platform_strategy or {},
        favorite_words=payload.favorite_words,
        forbidden_words=payload.forbidden_words,
        avoid_topics=payload.avoid_topics,
        additional_notes=payload.additional_notes,
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
