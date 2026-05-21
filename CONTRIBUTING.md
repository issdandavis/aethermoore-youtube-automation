# Contributing

This project is meant to stay useful for many creators, not just one channel.

## Good Contributions

- new dry-run automations
- review checks for metadata, scripts, thumbnails, and descriptions
- safer upload gates
- examples that do not contain private channel data
- tests for URL parsing, package validation, and review scoring

## Rules

- Do not commit OAuth tokens, `.env` files, client secrets, downloaded videos, or private analytics exports.
- New upload or publishing behavior must default to dry-run or private/unlisted.
- Networked features should be optional and testable without live credentials.
- Keep creator-specific behavior behind config files or plugins.

## Local Checks

```powershell
python -m pip install -e ".[dev]"
ruff check .
python -m pytest
```

