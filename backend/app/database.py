import os
from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import load_environment


load_environment()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+pysqlite:///./data/ai_content_studio.db")

if DATABASE_URL.startswith("sqlite") and ":///" in DATABASE_URL and ":memory:" not in DATABASE_URL:
    sqlite_path = DATABASE_URL.split(":///", 1)[1]
    Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
