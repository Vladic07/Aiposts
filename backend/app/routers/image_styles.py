from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import ImageStyle
from app.routers.utils import apply_updates, current_user_id, not_found
from app.schemas import ImageStyleCreate, ImageStyleRead, ImageStyleUpdate


router = APIRouter(prefix="/api/image-styles", tags=["image styles"])


@router.get("", response_model=list[ImageStyleRead])
def list_image_styles(session: Session = Depends(get_session)) -> list[ImageStyle]:
    user_id = current_user_id(session)
    return list(session.scalars(select(ImageStyle).where(ImageStyle.user_id == user_id).order_by(ImageStyle.updated_at.desc())))


@router.post("", response_model=ImageStyleRead, status_code=status.HTTP_201_CREATED)
def create_image_style(payload: ImageStyleCreate, session: Session = Depends(get_session)) -> ImageStyle:
    style = ImageStyle(user_id=current_user_id(session), **payload.model_dump())
    session.add(style)
    session.commit()
    session.refresh(style)
    return style


@router.put("/{style_id}", response_model=ImageStyleRead)
def update_image_style(style_id: int, payload: ImageStyleUpdate, session: Session = Depends(get_session)) -> ImageStyle:
    style = session.get(ImageStyle, style_id)
    if not style:
        raise not_found("Image style")
    apply_updates(style, payload.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(style)
    return style


@router.delete("/{style_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image_style(style_id: int, session: Session = Depends(get_session)) -> None:
    style = session.get(ImageStyle, style_id)
    if not style:
        raise not_found("Image style")
    session.delete(style)
    session.commit()
