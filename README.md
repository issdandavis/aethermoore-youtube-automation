# AetherMoore YouTube Automation

Reusable, local-first YouTube automation tooling for creators who want safer content workflows:

- collect public transcripts for research and repurposing
- review titles, descriptions, tags, and scripts before upload
- plan video packages with thumbnails, metadata, and descriptions
- keep uploads manual or explicitly gated
- run everything with dry-run defaults

This repo is designed as a starter kit other people can fork for their own channels.

## Guardrails

- No secrets in git.
- Upload/publish actions must be explicit.
- Default privacy should be `private` or `unlisted`.
- Do not copy copyrighted transcripts into generated content unless you have rights.
- Treat transcripts as research inputs, not as text to republish verbatim.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
copy .env.example .env
python -m aether_youtube_automation --help
python -m aether_youtube_automation transcript "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --json
python -m aether_youtube_automation review examples/video_package.example.json
```

## Configuration

Copy `.env.example` to `.env` and fill only what you need.

For uploads, use OAuth credentials owned by your own Google/YouTube account. This starter does not include OAuth tokens.

## Project Shape

```text
src/aether_youtube_automation/
  cli.py              command line interface
  config.py           env/config loading
  transcript.py       public transcript pull helpers
  review.py           metadata/script review scoring
  package.py          video package schema helpers
examples/
  channel.example.json
  video_package.example.json
tests/
```

## Roadmap

- OAuth upload module with explicit `--confirm-upload`
- thumbnail checklist and local image validation
- batch review reports
- subtitles/SRT generation helpers
- creator-specific plugin folder
- GitHub Actions smoke checks

