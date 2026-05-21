from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import load_config
from .package import load_video_package, to_jsonable
from .review import review_video_package
from .transcript import extract_video_id, fetch_transcript, transcript_text


def _cmd_config(_: argparse.Namespace) -> int:
    cfg = load_config()
    print(
        json.dumps(
            {
                "youtube_default_privacy": cfg.youtube_default_privacy,
                "channel_name": cfg.channel_name,
                "channel_handle": cfg.channel_handle,
                "default_tags": list(cfg.default_tags),
                "has_client_secret_file": bool(cfg.youtube_client_secret_file),
                "has_token_file": bool(cfg.youtube_token_file),
            },
            indent=2,
        )
    )
    return 0


def _cmd_transcript(args: argparse.Namespace) -> int:
    video_id = extract_video_id(args.target)
    if args.dry_run:
        payload = {"video_id": video_id, "dry_run": True}
    else:
        segments = fetch_transcript(video_id, tuple(args.language))
        payload = {
            "video_id": video_id,
            "segments": [segment.__dict__ for segment in segments],
            "text": transcript_text(segments),
        }
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(
            json.dumps(payload, indent=2) if args.json else payload.get("text", ""),
            encoding="utf-8",
        )
    print(json.dumps(payload, indent=2) if args.json else payload.get("text", video_id))
    return 0


def _cmd_review(args: argparse.Namespace) -> int:
    package = load_video_package(Path(args.package))
    report = review_video_package(package)
    payload = {
        "package": to_jsonable(package),
        "score": report.score,
        "findings": [finding.__dict__ for finding in report.findings],
    }
    print(json.dumps(payload, indent=2))
    return 1 if any(f.severity == "fail" for f in report.findings) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reusable YouTube automation starter kit")
    sub = parser.add_subparsers(dest="cmd", required=True)

    config = sub.add_parser("config", help="Show safe config summary")
    config.set_defaults(func=_cmd_config)

    transcript = sub.add_parser("transcript", help="Pull or inspect a YouTube transcript")
    transcript.add_argument("target", help="YouTube URL or 11-character video id")
    transcript.add_argument("--language", action="append", default=["en"])
    transcript.add_argument("--json", action="store_true")
    transcript.add_argument("--dry-run", action="store_true")
    transcript.add_argument("--output", default="")
    transcript.set_defaults(func=_cmd_transcript)

    review = sub.add_parser("review", help="Review a video package JSON file")
    review.add_argument("package")
    review.set_defaults(func=_cmd_review)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

