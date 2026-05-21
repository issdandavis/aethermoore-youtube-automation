import json

from aether_youtube_automation.cli import main


def test_cli_transcript_dry_run(capsys):
    code = main(["transcript", "https://youtu.be/dQw4w9WgXcQ", "--dry-run", "--json"])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["video_id"] == "dQw4w9WgXcQ"
    assert payload["dry_run"] is True

