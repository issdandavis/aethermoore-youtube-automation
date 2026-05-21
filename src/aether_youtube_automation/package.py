from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class VideoPackage:
    title: str
    description: str
    tags: tuple[str, ...]
    script: str = ""
    privacy: str = "unlisted"


def load_video_package(path: Path) -> VideoPackage:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("video package must be a JSON object")
    tags_raw = data.get("tags", [])
    if isinstance(tags_raw, str):
        tags = tuple(tag.strip() for tag in tags_raw.split(",") if tag.strip())
    elif isinstance(tags_raw, list):
        tags = tuple(str(tag).strip() for tag in tags_raw if str(tag).strip())
    else:
        tags = ()
    return VideoPackage(
        title=str(data.get("title", "")).strip(),
        description=str(data.get("description", "")).strip(),
        tags=tags,
        script=str(data.get("script", "")).strip(),
        privacy=str(data.get("privacy", "unlisted")).strip() or "unlisted",
    )


def to_jsonable(package: VideoPackage) -> dict[str, Any]:
    return {
        "title": package.title,
        "description": package.description,
        "tags": list(package.tags),
        "script": package.script,
        "privacy": package.privacy,
    }

