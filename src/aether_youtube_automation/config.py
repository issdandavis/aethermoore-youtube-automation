from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    youtube_client_secret_file: str = ""
    youtube_token_file: str = ""
    youtube_default_privacy: str = "unlisted"
    channel_name: str = ""
    channel_handle: str = ""
    default_tags: tuple[str, ...] = ()


def load_dotenv(path: Path = Path(".env")) -> dict[str, str]:
    """Load a simple local .env file without overriding existing environment values."""
    loaded: dict[str, str] = {}
    if not path.exists():
        return loaded
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        clean = value.strip().strip("\"'")
        os.environ[key] = clean
        loaded[key] = clean
    return loaded


def load_config(*, dotenv_path: Path = Path(".env")) -> AppConfig:
    load_dotenv(dotenv_path)
    tags = tuple(
        tag.strip()
        for tag in os.getenv("DEFAULT_TAGS", "").split(",")
        if tag.strip()
    )
    return AppConfig(
        youtube_client_secret_file=os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "").strip(),
        youtube_token_file=os.getenv("YOUTUBE_TOKEN_FILE", "").strip(),
        youtube_default_privacy=os.getenv("YOUTUBE_DEFAULT_PRIVACY", "unlisted").strip()
        or "unlisted",
        channel_name=os.getenv("CHANNEL_NAME", "").strip(),
        channel_handle=os.getenv("CHANNEL_HANDLE", "").strip(),
        default_tags=tags,
    )

