# Security Policy

## Secrets

Never commit:

- Google OAuth client secret files
- YouTube refresh/access tokens
- `.env` files
- exported channel analytics with private account data
- generated videos that include private material

Use `.env.example` as the template and keep real files local.

## Publishing Safety

This project should prefer:

- dry-run first
- `private` or `unlisted` before `public`
- explicit confirmation flags for upload/publish commands
- local review reports before any live mutation

Report security issues privately through GitHub Security Advisories when available.

