from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal, engine
from app.models import Base, ensure_default_user
from app.routers import content_profiles, generation_sessions, image_styles, posts, settings, text_styles


def init_database() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        ensure_default_user(session)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    init_database()
    yield


app = FastAPI(title="AI Content Studio API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(content_profiles.router)
app.include_router(text_styles.router)
app.include_router(image_styles.router)
app.include_router(posts.router)
app.include_router(generation_sessions.router)
app.include_router(settings.router)
