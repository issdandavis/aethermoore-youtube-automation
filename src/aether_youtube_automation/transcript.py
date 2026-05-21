from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse


YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


@dataclass(frozen=True)
class TranscriptSegment:
    text: str
    start: float = 0.0
    duration: float = 0.0


def extract_video_id(target: str) -> str:
    value = target.strip()
    if YOUTUBE_ID_RE.match(value):
        return value
    parsed = urlparse(value)
    host = parsed.netloc.lower()
    if host in {"youtu.be"}:
        candidate = parsed.path.strip("/").split("/", 1)[0]
        if YOUTUBE_ID_RE.match(candidate):
            return candidate
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        query_id = parse_qs(parsed.query).get("v", [""])[0]
        if YOUTUBE_ID_RE.match(query_id):
            return query_id
        for prefix in ("/shorts/", "/live/", "/embed/"):
            if parsed.path.startswith(prefix):
                candidate = parsed.path[len(prefix) :].split("/", 1)[0]
                if YOUTUBE_ID_RE.match(candidate):
                    return candidate
    raise ValueError(f"could not extract YouTube video id from: {target}")


def fetch_transcript(video_id: str, languages: tuple[str, ...] = ("en",)) -> list[TranscriptSegment]:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("youtube-transcript-api is not installed") from exc

    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        rows = YouTubeTranscriptApi.get_transcript(video_id, languages=list(languages))
    else:
        rows = YouTubeTranscriptApi().fetch(video_id, languages=list(languages))
    return [
        TranscriptSegment(
            text=str(row.get("text", "")),
            start=float(row.get("start", 0.0)),
            duration=float(row.get("duration", 0.0)),
        )
        for row in rows
    ]


def transcript_text(segments: list[TranscriptSegment]) -> str:
    return "\n".join(segment.text for segment in segments if segment.text).strip()

