from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import GenerationSession
from app.routers.utils import current_user_id, not_found
from app.schemas import GenerationSessionCreate, GenerationSessionRead


router = APIRouter(prefix="/api/generation-sessions", tags=["generation sessions"])


@router.get("", response_model=list[GenerationSessionRead])
def list_generation_sessions(session: Session = Depends(get_session)) -> list[GenerationSession]:
    user_id = current_user_id(session)
    return list(session.scalars(select(GenerationSession).where(GenerationSession.user_id == user_id).order_by(GenerationSession.created_at.desc())))


@router.post("", response_model=GenerationSessionRead, status_code=status.HTTP_201_CREATED)
def create_generation_session(payload: GenerationSessionCreate, session: Session = Depends(get_session)) -> GenerationSession:
    item = GenerationSession(user_id=current_user_id(session), **payload.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/{session_id}", response_model=GenerationSessionRead)
def get_generation_session(session_id: int, session: Session = Depends(get_session)) -> GenerationSession:
    item = session.get(GenerationSession, session_id)
    if not item:
        raise not_found("Generation session")
    return item


@router.post("/{session_id}/next-step", response_model=GenerationSessionRead)
def next_generation_step(session_id: int, session: Session = Depends(get_session)) -> GenerationSession:
    item = session.get(GenerationSession, session_id)
    if not item:
        raise not_found("Generation session")
    item.current_step = "finalization" if item.current_step != "finalization" else "completed"
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_generation_session(session_id: int, session: Session = Depends(get_session)) -> None:
    item = session.get(GenerationSession, session_id)
    if not item:
        raise not_found("Generation session")
    session.delete(item)
    session.commit()
