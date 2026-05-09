from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_environment(env_path: Path | None = None) -> None:
    load_dotenv(dotenv_path=env_path or PROJECT_ROOT / ".env", override=False)
