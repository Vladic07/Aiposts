from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import TextStyle
from app.routers.utils import apply_updates, current_user_id, not_found
from app.schemas import TextStyleCreate, TextStyleRead, TextStyleUpdate


router = APIRouter(prefix="/api/text-styles", tags=["text styles"])


@router.get("", response_model=list[TextStyleRead])
def list_text_styles(session: Session = Depends(get_session)) -> list[TextStyle]:
    user_id = current_user_id(session)
    return list(session.scalars(select(TextStyle).where(TextStyle.user_id == user_id).order_by(TextStyle.updated_at.desc())))


@router.post("", response_model=TextStyleRead, status_code=status.HTTP_201_CREATED)
def create_text_style(payload: TextStyleCreate, session: Session = Depends(get_session)) -> TextStyle:
    style = TextStyle(user_id=current_user_id(session), **payload.model_dump())
    session.add(style)
    session.commit()
    session.refresh(style)
    return style


@router.put("/{style_id}", response_model=TextStyleRead)
def update_text_style(style_id: int, payload: TextStyleUpdate, session: Session = Depends(get_session)) -> TextStyle:
    style = session.get(TextStyle, style_id)
    if not style:
        raise not_found("Text style")
    apply_updates(style, payload.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(style)
    return style


@router.delete("/{style_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_text_style(style_id: int, session: Session = Depends(get_session)) -> None:
    style = session.get(TextStyle, style_id)
    if not style:
        raise not_found("Text style")
    session.delete(style)
    session.commit()


@router.post("/analyze-examples", response_model=TextStyleRead, status_code=status.HTTP_201_CREATED)
def analyze_examples(payload: TextStyleCreate, session: Session = Depends(get_session)) -> TextStyle:
    examples = payload.examples
    rules = payload.rules or "Write in the same rhythm as the examples. Keep concrete nouns and avoid generic claims."
    if examples:
        rules = f"{rules}\nUse patterns from {len(examples)} saved examples."
    style = TextStyle(user_id=current_user_id(session), **payload.model_copy(update={"rules": rules}).model_dump())
    session.add(style)
    session.commit()
    session.refresh(style)
    return style
