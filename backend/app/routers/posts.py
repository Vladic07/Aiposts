from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai_service import generate_post_content
from app.database import get_session
from app.models import ContentProfile, GenerationSession, ImageStyle, Post, TextStyle
from app.routers.utils import apply_updates, current_user_id, not_found
from app.schemas import GeneratePostRequest, PostRead, PostUpdate


router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("", response_model=list[PostRead])
def list_posts(session: Session = Depends(get_session)) -> list[Post]:
    user_id = current_user_id(session)
    return list(session.scalars(select(Post).where(Post.user_id == user_id).order_by(Post.created_at.desc())))


@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, session: Session = Depends(get_session)) -> Post:
    post = session.get(Post, post_id)
    if not post:
        raise not_found("Post")
    return post


@router.post("/generate", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def generate_post(payload: GeneratePostRequest, session: Session = Depends(get_session)) -> Post:
    user_id = current_user_id(session)
    profile = session.get(ContentProfile, payload.profile_id)
    if not profile:
        raise not_found("Content profile")
    text_style = session.get(TextStyle, payload.text_style_id) if payload.text_style_id else None
    image_style = session.get(ImageStyle, payload.image_style_id) if payload.image_style_id else None

    result, model_used = generate_post_content(payload, profile, text_style, image_style)
    result_dict = result.model_dump()

    generation_session = GenerationSession(
        user_id=user_id,
        profile_id=profile.id,
        mode=payload.generation_mode,
        topic=payload.topic,
        platforms=payload.platforms,
        current_step="completed",
        hooks=result_dict["hooks"],
        final_content=result_dict,
        image_prompts=[result_dict["image_prompt"]],
        platform_analysis=result_dict["analysis"],
    )
    session.add(generation_session)
    session.flush()

    post = Post(
        user_id=user_id,
        profile_id=profile.id,
        text_style_id=payload.text_style_id,
        image_style_id=payload.image_style_id,
        generation_session_id=generation_session.id,
        topic=payload.topic,
        goal=payload.goal,
        platforms=payload.platforms,
        generation_mode=payload.generation_mode,
        input_request=payload.input_request,
        generated_content={key: value for key, value in result_dict.items() if key not in {"image_prompt", "analysis"}},
        image_prompt=result_dict["image_prompt"],
        model_used=model_used,
        status="draft",
        score={
            "hook_score": result.analysis.hook_score,
            "clarity_score": result.analysis.clarity_score,
            "platform_fit_score": result.analysis.platform_fit_score,
        },
        analysis=result_dict["analysis"],
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.put("/{post_id}", response_model=PostRead)
def update_post(post_id: int, payload: PostUpdate, session: Session = Depends(get_session)) -> Post:
    post = session.get(Post, post_id)
    if not post:
        raise not_found("Post")
    apply_updates(post, payload.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: Session = Depends(get_session)) -> None:
    post = session.get(Post, post_id)
    if not post:
        raise not_found("Post")
    session.delete(post)
    session.commit()
