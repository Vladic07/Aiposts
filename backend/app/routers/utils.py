from typing import Any, TypeVar

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import get_default_user


ModelT = TypeVar("ModelT")


def current_user_id(session: Session) -> int:
    return get_default_user(session).id


def apply_updates(instance: Any, values: dict[str, Any]) -> Any:
    for key, value in values.items():
        setattr(instance, key, value)
    return instance


def not_found(name: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{name} not found")
