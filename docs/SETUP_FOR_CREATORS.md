# Setup For Creators

This guide is for adapting the starter to your own channel.

## 1. Fork Or Use As Template

Use the GitHub template button or fork the repo. Keep your fork private while adding credentials.

## 2. Install

```powershell
git clone https://github.com/YOUR_NAME/aethermoore-youtube-automation.git
cd aethermoore-youtube-automation
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## 3. Configure

```powershell
copy .env.example .env
```

Fill:

```text
CHANNEL_NAME=Your Channel
CHANNEL_HANDLE=@yourhandle
DEFAULT_TAGS=tag one,tag two,tag three
YOUTUBE_DEFAULT_PRIVACY=unlisted
```

Do not commit `.env`.

## 4. Review A Video Package

Edit `examples/video_package.example.json`, then run:

```powershell
python -m aether_youtube_automation review examples\video_package.example.json
```

The score is intentionally conservative. The goal is to catch weak metadata before upload.

## 5. Pull A Transcript

```powershell
python -m aether_youtube_automation transcript "https://www.youtube.com/watch?v=VIDEO_ID" --json --output artifacts\transcripts\video.json
```

Use transcripts for research and note extraction. Do not republish copyrighted transcript text unless you have rights.

## 6. Future Uploads

Upload support should remain gated:

- authenticate locally
- upload as `private` or `unlisted`
- require a confirmation flag for `public`

