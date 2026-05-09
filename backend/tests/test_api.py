from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_session
from app.main import app
from app.models import Base, ensure_default_user


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)

    def override_get_session() -> Generator[Session, None, None]:
        with TestingSessionLocal() as session:
            ensure_default_user(session)
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_health_reports_ok(client: TestClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_content_profile_crud(client: TestClient) -> None:
    payload = {
        "name": "AI notes",
        "profile_type": "personal AI blog",
        "source_description": "Short practical posts about AI tools.",
        "niche": "AI tools",
        "audience": "builders",
        "platforms": ["x", "linkedin"],
        "language": "en",
    }

    created = client.post("/api/content-profiles", json=payload)
    assert created.status_code == 201
    profile = created.json()
    assert profile["id"] > 0
    assert profile["name"] == "AI notes"
    assert profile["platforms"] == ["x", "linkedin"]

    listed = client.get("/api/content-profiles")
    assert listed.status_code == 200
    assert [item["name"] for item in listed.json()] == ["AI notes"]

    updated = client.put(
        f"/api/content-profiles/{profile['id']}",
        json={"name": "Sharper AI notes", "tone": "direct"},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Sharper AI notes"
    assert updated.json()["tone"] == "direct"


def test_fallback_generation_creates_post(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    profile = client.post(
        "/api/content-profiles",
        json={
            "name": "Coffee lab",
            "profile_type": "local cafe",
            "audience": "regular guests",
            "tone": "warm and concrete",
            "platforms": ["instagram", "facebook"],
            "language": "en",
        },
    ).json()

    response = client.post(
        "/api/posts/generate",
        json={
            "profile_id": profile["id"],
            "topic": "Weekend cold brew offer",
            "goal": "Bring people into the shop",
            "platforms": ["instagram", "facebook", "x"],
            "generation_mode": "auto",
            "language": "en",
            "save_to_history": True,
        },
    )

    assert response.status_code == 201
    post = response.json()
    assert post["topic"] == "Weekend cold brew offer"
    assert post["status"] == "draft"
    assert "instagram" in post["generated_content"]
    assert post["image_prompt"]["prompt"]
    assert post["analysis"]["clarity_score"] >= 1

    history = client.get("/api/posts")
    assert history.status_code == 200
    assert len(history.json()) == 1


def test_post_status_and_tags_can_be_updated(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    profile = client.post(
        "/api/content-profiles",
        json={"name": "Founder notes", "profile_type": "expert profile"},
    ).json()
    post = client.post(
        "/api/posts/generate",
        json={"profile_id": profile["id"], "topic": "Why simple workflows win"},
    ).json()

    response = client.put(
        f"/api/posts/{post['id']}",
        json={"status": "liked", "tags": ["workflow", "ai"], "notes": "Reuse this angle"},
    )

    assert response.status_code == 200
    updated = response.json()
    assert updated["status"] == "liked"
    assert updated["tags"] == ["workflow", "ai"]
    assert updated["notes"] == "Reuse this angle"


def test_text_style_update_and_delete(client: TestClient) -> None:
    created = client.post(
        "/api/text-styles",
        json={
            "name": "Direct style",
            "description": "Short practical writing",
            "rules": "Use concrete nouns.",
            "examples": ["First example"],
        },
    )
    assert created.status_code == 201
    style_id = created.json()["id"]

    updated = client.put(
        f"/api/text-styles/{style_id}",
        json={"name": "Sharper style", "examples": ["First example", "Second example"], "emoji_level": "none"},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Sharper style"
    assert updated.json()["examples"] == ["First example", "Second example"]
    assert updated.json()["emoji_level"] == "none"

    deleted = client.delete(f"/api/text-styles/{style_id}")
    assert deleted.status_code == 204
    assert client.get("/api/text-styles").json() == []


def test_image_style_update_and_delete(client: TestClient) -> None:
    created = client.post(
        "/api/image-styles",
        json={
            "name": "Clean product",
            "description": "Bright product visuals",
            "colors": ["white", "green"],
            "mood": "calm",
        },
    )
    assert created.status_code == 201
    style_id = created.json()["id"]

    updated = client.put(
        f"/api/image-styles/{style_id}",
        json={"name": "Studio product", "colors": ["white", "black"], "avoid": "clutter"},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Studio product"
    assert updated.json()["colors"] == ["white", "black"]
    assert updated.json()["avoid"] == "clutter"

    deleted = client.delete(f"/api/image-styles/{style_id}")
    assert deleted.status_code == 204
    assert client.get("/api/image-styles").json() == []


def test_settings_can_be_updated(client: TestClient) -> None:
    response = client.put(
        "/api/settings",
        json={
            "provider": "openai",
            "text_model": "gpt-4.1-mini",
            "fast_model": "gpt-4.1-mini",
            "quality_model": "gpt-4.1",
            "image_model": "gpt-image-1",
            "daily_generation_limit": 25,
            "default_language": "en",
        },
    )

    assert response.status_code == 200
    settings = response.json()
    assert settings["daily_generation_limit"] == 25
    assert settings["default_language"] == "en"

    loaded = client.get("/api/settings")
    assert loaded.status_code == 200
    assert loaded.json()["daily_generation_limit"] == 25


def test_generation_session_create_list_and_delete(client: TestClient) -> None:
    profile = client.post(
        "/api/content-profiles",
        json={"name": "Guided profile", "profile_type": "expert"},
    ).json()

    created = client.post(
        "/api/generation-sessions",
        json={"profile_id": profile["id"], "mode": "guided", "topic": "Guided workflow", "platforms": ["x"]},
    )
    assert created.status_code == 201
    session_id = created.json()["id"]
    assert created.json()["current_step"] == "completed"

    listed = client.get("/api/generation-sessions")
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [session_id]

    deleted = client.delete(f"/api/generation-sessions/{session_id}")
    assert deleted.status_code == 204
    assert client.get("/api/generation-sessions").json() == []


def test_generation_with_unknown_profile_returns_404(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    response = client.post(
        "/api/posts/generate",
        json={"profile_id": 9999, "topic": "Missing profile"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Content profile not found"
