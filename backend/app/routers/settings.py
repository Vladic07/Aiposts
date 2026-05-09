from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Settings
from app.routers.utils import apply_updates, current_user_id
from app.schemas import SettingsRead, SettingsUpdate


router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("", response_model=SettingsRead)
def get_settings(session: Session = Depends(get_session)) -> Settings:
    user_id = current_user_id(session)
    settings = session.scalar(select(Settings).where(Settings.user_id == user_id))
    if settings is None:
        settings = Settings(user_id=user_id)
        session.add(settings)
        session.commit()
        session.refresh(settings)
    return settings


@router.put("", response_model=SettingsRead)
def update_settings(payload: SettingsUpdate, session: Session = Depends(get_session)) -> Settings:
    settings = get_settings(session)
    apply_updates(settings, payload.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(settings)
    return settings
