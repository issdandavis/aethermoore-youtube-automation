from __future__ import annotations

from dataclasses import dataclass

from .package import VideoPackage


@dataclass(frozen=True)
class ReviewFinding:
    severity: str
    field: str
    message: str


@dataclass(frozen=True)
class ReviewReport:
    score: int
    findings: tuple[ReviewFinding, ...]


def review_video_package(package: VideoPackage) -> ReviewReport:
    findings: list[ReviewFinding] = []
    score = 100

    title_len = len(package.title)
    if title_len < 25:
        findings.append(ReviewFinding("warn", "title", "Title is probably too short."))
        score -= 10
    if title_len > 100:
        findings.append(ReviewFinding("warn", "title", "Title may be truncated by YouTube."))
        score -= 10
    if not package.description:
        findings.append(ReviewFinding("fail", "description", "Description is empty."))
        score -= 25
    elif len(package.description) < 80:
        findings.append(ReviewFinding("warn", "description", "Description is thin."))
        score -= 10
    if len(package.tags) < 3:
        findings.append(ReviewFinding("warn", "tags", "Use at least three useful tags."))
        score -= 8
    if package.privacy not in {"private", "unlisted", "public"}:
        findings.append(ReviewFinding("fail", "privacy", "Privacy must be private, unlisted, or public."))
        score -= 25
    if package.privacy == "public":
        findings.append(ReviewFinding("warn", "privacy", "Public uploads should require manual approval."))
        score -= 5
    if package.script and len(package.script.split()) < 40:
        findings.append(ReviewFinding("warn", "script", "Script is very short for a standalone video."))
        score -= 8

    return ReviewReport(score=max(0, score), findings=tuple(findings))

