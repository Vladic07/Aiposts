from pathlib import Path

from app.config import load_environment


def test_load_environment_reads_project_env_without_overwriting_existing_values(tmp_path, monkeypatch) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text("OPENAI_API_KEY=from-file\nDEFAULT_TEXT_MODEL=gpt-5-mini\n", encoding="utf-8")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("DEFAULT_TEXT_MODEL", "already-set")

    load_environment(env_path)

    assert "OPENAI_API_KEY" in __import__("os").environ
    assert __import__("os").environ["DEFAULT_TEXT_MODEL"] == "already-set"
